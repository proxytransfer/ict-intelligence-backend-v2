from typing import List
from app.infrastructure.providers.binance import BinanceProvider
from app.infrastructure.providers.yahoo import YahooFinanceProvider
from app.infrastructure.cache.local_cache import LocalCache
from app.domain.candle import Candle

class DataService:
    def __init__(self):
        self.binance = BinanceProvider()
        self.yahoo = YahooFinanceProvider()
        self.cache = LocalCache()

    async def get_market_data(self, symbol: str, timeframe: str) -> List[Candle]:
        cache_key = f"candles_{symbol}_{timeframe}"
        cached_data = self.cache.get(cache_key)
        
        if cached_data:
            return cached_data
            
        # Roteamento inteligente de ativos
        provider = self._get_provider_for_symbol(symbol)
        
        try:
            candles = await provider.fetch_candles(symbol, timeframe)
            self.cache.set(cache_key, candles, ttl=60)
            return candles
        except Exception as e:
            # Fallback para o Yahoo se a Binance falhar ou o ativo não existir lá
            if provider == self.binance:
                return await self.yahoo.fetch_candles(symbol, timeframe)
            raise e

    def _get_provider_for_symbol(self, symbol: str):
        symbol = symbol.upper()
        # Se termina com USDT ou é um par cripto comum, usa Binance
        if symbol.endswith("USDT") or symbol in ["BTCUSD", "ETHUSD"]:
            return self.binance
        # Caso contrário (Forex, Ouro, etc.), usa Yahoo
        return self.yahoo
