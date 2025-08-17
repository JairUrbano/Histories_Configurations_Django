from rest_framework import serializers
from mi_app.models.predetermined_price import PredeterminedPrice

class PredeterminedPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PredeterminedPrice
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')
