from rest_framework import serializers
from .models import Coin,CoinCurrentData


class CoinCurrentDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoinCurrentData
        fields = ["id", "coin", "price", "market_cap", "total_volume","price_change_percentage_24h", "timestamp"]
        
class CoinListSerializer(serializers.ModelSerializer):
    current_data = CoinCurrentDataSerializer(read_only=True) 
    price_24h_ago = serializers.ReadOnlyField()
    change_percent = serializers.FloatField(read_only=True)
    
    class Meta:
        model = Coin
        fields = ["id", "image_url", "gecko_id", "name", "symbol", "max_supply", "is_active", "current_data", "price_24h_ago","change_percent"]
        
class CoinDetailSerializer(serializers.ModelSerializer):
    current_data = CoinCurrentDataSerializer(read_only=True) 
    class Meta:
        model = Coin
        fields = "__all__"