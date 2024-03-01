from rest_framework import serializers
from .models import AvaliacaoFDMP

class AvaliacaoFDMPSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvaliacaoFDMP
        fields = '__all__'
