import redis

import os
import requests
import math
from datetime import datetime, timezone, timedelta

REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))


def convert_to_uzs(amount):
    redis_connection = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)

    today = datetime.now().strftime("%Y-%m-%d")
    rate_cache = redis_connection.get("usd_rate")

    if rate_cache:
        rate_cache = rate_cache.decode("utf-8")
        if rate_cache.split(":")[0] == today:
            rate = float(rate_cache.split(":")[1])
            return math.floor(amount * rate)

    url = f"https://cbu.uz/oz/arkhiv-kursov-valyut/json/USD/{today}/"
    response = requests.get(url)
    data = response.json()
    rate = float(data[0]["Rate"])
    redis_connection.set("usd_rate", f"{today}:{rate}", ex=86400)

    return math.floor(amount * rate)


def generate_paylink(order):
    amount_uzs = convert_to_uzs(float(order.total_price))
    if order.currency == "UZS":
        payment_amount = amount_uzs
    else:
        payment_amount = float(order.total_price)

    headers = {
        "Content-Type": "application/json",
        "Authorization": os.getenv("PAYZE_AUTH_TOKEN")
    }

    request_data = {
        "source": "Card",
        "amount": payment_amount,
        "currency": order.currency,
        "language": "EN",
        "hooks": {
            "webhookGateway": os.getenv("PAYZE_WEBHOOK_URL"),
            "successRedirectGateway": os.getenv("PAYZE_ERROR_URL"),
            "errorRedirectGateway": os.getenv("PAYZE_SUCCESS_URL")
        },
        "metadata": {
            "Order": {
                "OrderId": str(order.id),
                "OrderItems": None,
                "BillingAddress": None
            },
            "extraAttributes": [
                {
                    "key": "RECEIPT_TYPE",
                    "value": "Sale",
                    "description": "OFD Receipt type"
                }
            ]
        }
    }

    response = requests.put(
        "https://payze.io/v2/api/payment",
        headers=headers,
        json=request_data
    )

    response_data = response.json()

    if response.status_code != 200:
        return {
            "error": response_data
        }

    payment_url = response_data['data']['payment']['paymentUrl']

    return {
        "pay_link": payment_url
    }


