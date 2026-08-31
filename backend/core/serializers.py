from rest_framework import serializers
from .models import Coin,CoinCurrentData,PriceHistory


class CoinCurrentDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoinCurrentData
        fields = ["id", "coin", "price", "market_cap", "total_volume","price_change_percentage_24h", "circulating_supply", "ath", "atl", "timestamp"]
        
class CoinListSerializer(serializers.ModelSerializer):
    current_data = CoinCurrentDataSerializer(read_only=True) 
    
    class Meta:
        model = Coin
        fields = ["id", "image_url", "gecko_id", "name", "symbol", "max_supply", "is_active", "current_data"]

class PriceHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceHistory
        fields = "__all__"

class CoinDetailSerializer(serializers.ModelSerializer):
    current_data = CoinCurrentDataSerializer(read_only=True) 
    history_data = PriceHistorySerializer(
        source="history_records",
        read_only=True,
        many=True
    )
    avg_price = serializers.DecimalField(source="stats.avg_price", max_digits=20, decimal_places=8, read_only=True)
    highest_price = serializers.DecimalField(source="stats.highest_price", max_digits=20, decimal_places=8, read_only=True)
    lowest_price = serializers.DecimalField(source="stats.lowest_price", max_digits=20, decimal_places=8, read_only=True)
    history_records_count = serializers.IntegerField(source="stats.history_records_count", read_only=True)
    first_recorded_at = serializers.DateTimeField(source="stats.first_recorded_at", read_only=True)
    last_updated_at = serializers.DateTimeField(source="stats.last_updated_at", read_only=True)
    class Meta:
        model = Coin
        fields = "__all__"