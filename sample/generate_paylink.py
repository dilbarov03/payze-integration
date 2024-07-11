import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

headers = {
    'Content-Type': 'application/json',
    'Authorization': os.getenv('PAYZE_AUTH_TOKEN') #API_KEY:API_SECRET 
}


request_data = {
    "source": "Card",
    "amount": 15000,
    "currency": "USD",
    "language": "UZ",
    "hooks": {
      "webhookGateway": "https://domain.com/",
      "successRedirectGateway": "https://google.com",
      "errorRedirectGateway": "https://yandex.com"
    },
    "metadata": {
      "Order": {
        "OrderId": "99",
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

print(response_data)

payment_url = response_data['data']['payment']['paymentUrl']
 
print(payment_url)   