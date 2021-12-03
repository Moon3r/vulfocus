from rest_framework import serializers
from frp.models import FrpUtils, FrpConfig


class FrpUtilsSerializer(serializers.ModelSerializer):

    class Meta:
        model = FrpUtils
        fields = '__all__'


class FrpConfigSerializer(serializers.ModelSerializer):

    class Meta:
        model = FrpConfig
        fields = '__all__'
