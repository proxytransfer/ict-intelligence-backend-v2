from typing import List, Dict
from app.infrastructure.providers.binance import BinanceProvider
from app.infrastructure.cache.local_cache import LocalCache
from app.domain.candle import Candle

class DataService:
    def __init__(self):
        self.provider = BinanceProvider()
        self.cache = LocalCache()

    async def get_market_data(self, symbol: str, timeframe: str) -> List[Candle]:
        cache_key = f"candles_{symbol}_{timeframe}"
        cached_data = self.cache.get(cache_key)
        
        if cached_data:
            return cached_data
            
        candles = await self.provider.fetch_candles(symbol, timeframe)
        self.cache.set(cache_key, candles, ttl=60) # Cache de 1 minuto para dados reais
        return candles
