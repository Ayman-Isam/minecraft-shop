from rest_framework import serializers
from .models import Redeem

class RedeemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Redeem
        fields = '__all__'