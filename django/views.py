from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from serializers import PayzeWebhookSerializer


class CreatePayzeCheckoutSession(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        data = request.data
        order = get_object_or_404(Order, id=data.get("order_id"))

        response = generate_paylink(order)
        return Response(response)


class PayzeWebhookAPIView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = PayzeWebhookSerializer(data=request.data)

        if serializer.is_valid():
            validated_data = serializer.validated_data
            payment_data = get_payment_data(request.data)
            payment_status = validated_data["PaymentStatus"]

            order_id = validated_data["Metadata"]["Order"]["OrderId"]
            # custom logic ...

            try:
                with transaction.atomic():

                    if payment_status == "Captured":
                        order = Order.objects.filter(id=order_id).first()
                        if order:
                            order.status = Order.OrderStatus.SUCCESS
                            order.save()
                            Payment.objects.create(
                                user=order.user, order=order,
                                **payment_data
                            )
                        else:
                            logger.warning(f"Order {order_id} not found.")

            except Exception as e:
                return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({"message": "Webhook received successfully"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

