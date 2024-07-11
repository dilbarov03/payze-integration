from rest_framework import serializers


class RefundSerializer(serializers.Serializer):
    RefundId = serializers.CharField(allow_null=True, required=False)
    Status = serializers.CharField(allow_null=True, required=False)
    Refundable = serializers.BooleanField()
    Amount = serializers.FloatField(allow_null=True, required=False)
    RequestedAmount = serializers.FloatField(allow_null=True, required=False)
    RejectReason = serializers.CharField(allow_null=True, required=False)
    RefundDate = serializers.DateTimeField(allow_null=True, required=False)
    RefundDateIso = serializers.DateTimeField(allow_null=True, required=False)
    Revisions = serializers.ListField(child=serializers.DictField(), required=False)


class UzRegulatoryOrderDetailsSerializer(serializers.Serializer):
    Latitude = serializers.FloatField(allow_null=True, required=False)
    Longitude = serializers.FloatField(allow_null=True, required=False)
    TaxiVehicleNumber = serializers.CharField(allow_null=True, required=False)
    TaxiTin = serializers.CharField(allow_null=True, required=False)
    TaxiPinfl = serializers.CharField(allow_null=True, required=False)


class AddressSerializer(serializers.Serializer):
    FirstName = serializers.CharField(allow_null=True, required=False)
    LastName = serializers.CharField(allow_null=True, required=False)
    City = serializers.CharField(allow_null=True, required=False)
    Country = serializers.CharField(allow_null=True, required=False)
    Line1 = serializers.CharField(allow_null=True, required=False)
    Line2 = serializers.CharField(allow_null=True, required=False)
    PostalCode = serializers.CharField(allow_null=True, required=False)
    State = serializers.CharField(allow_null=True, required=False)
    PhoneNumber = serializers.CharField(allow_null=True, required=False)


class OrderSerializer(serializers.Serializer):
    OrderId = serializers.CharField()
    OrderItems = serializers.ListField(child=serializers.DictField(), required=False)
    UzRegulatoryOrderDetails = UzRegulatoryOrderDetailsSerializer()
    BillingAddress = AddressSerializer()
    ShippingAddress = AddressSerializer()


class ExtraAttributeSerializer(serializers.Serializer):
    Key = serializers.CharField()
    Value = serializers.CharField()
    Description = serializers.CharField(allow_null=True, required=False)


class MetadataSerializer(serializers.Serializer):
    Channel = serializers.CharField(allow_null=True, required=False)
    Order = OrderSerializer()
    ExtraAttributes = serializers.ListField(child=ExtraAttributeSerializer(), required=False)


class PayerSerializer(serializers.Serializer):
    Phone = serializers.CharField(allow_null=True, required=False)
    FullName = serializers.CharField(allow_null=True, required=False)


class PayzeWebhookSerializer(serializers.Serializer):
    Source = serializers.CharField()
    IdempotencyKey = serializers.CharField(allow_null=True, required=False)
    PaymentId = serializers.CharField()
    Type = serializers.CharField()
    Sandbox = serializers.BooleanField()
    PaymentStatus = serializers.CharField()
    Amount = serializers.FloatField()
    FinalAmount = serializers.FloatField(allow_null=True, required=False)
    Currency = serializers.CharField()
    RRN = serializers.CharField(allow_null=True, required=False)
    Commission = serializers.FloatField(allow_null=True, required=False)
    Preauthorized = serializers.BooleanField()
    CanBeCaptured = serializers.BooleanField()
    CreateDate = serializers.IntegerField()
    CreateDateIso = serializers.DateTimeField()
    CaptureDate = serializers.IntegerField(allow_null=True, required=False)
    CaptureDateIso = serializers.DateTimeField(allow_null=True, required=False)
    BlockDate = serializers.IntegerField(allow_null=True, required=False)
    BlockDateIso = serializers.DateTimeField(allow_null=True, required=False)
    Token = serializers.CharField(allow_null=True, required=False)
    CardMask = serializers.CharField(allow_null=True, required=False)
    CardOrigination = serializers.CharField(allow_null=True, required=False)
    CardOwnerEntityType = serializers.CharField(allow_null=True, required=False)
    CardBrand = serializers.CharField(allow_null=True, required=False)
    CardCountry = serializers.CharField(allow_null=True, required=False)
    CardHolder = serializers.CharField(allow_null=True, required=False)
    ExpirationDate = serializers.CharField(allow_null=True, required=False)
    SecureCardId = serializers.CharField(allow_null=True, required=False)
    RejectionReason = serializers.CharField(allow_null=True, required=False)
    Refund = RefundSerializer()
    Splits = serializers.ListField(child=serializers.DictField(), allow_null=True, required=False)
    Metadata = MetadataSerializer()
    Payer = PayerSerializer()

