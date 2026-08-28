from rest_framework import serializers
from .models import Coin,CoinCurrentData


class CoinCurrentDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoinCurrentData
        fields = "id", "price", "market_cap", "total_volume","price_change_percentage_24h", "timestamp"
        
class CoinListSerializer(serializers.ModelSerializer):
    current_data = CoinCurrentDataSerializer(read_only=True) 
    class Meta:
        model = Coin
        fields = ["gecko_id", "name", "symbol", "max_supply", "is_active", "current_data"]
        
class CoinDetailSerializer(serializers.ModelSerializer):
    current_data = CoinCurrentDataSerializer(read_only=True) 
    class Meta:
        model = Coin
        fields = "__all__"