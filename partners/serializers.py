from rest_framework import serializers

from partners.models import PartnerConfig


class PartnerConfigSerializer(serializers.ModelSerializer):

    class Meta:
        model = PartnerConfig
        fields = '__all__'
