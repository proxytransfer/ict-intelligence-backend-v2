import httpx
from typing import List
from app.domain.candle import Candle
from app.infrastructure.providers.base import BaseDataProvider
from datetime import datetime

class BinanceProvider(BaseDataProvider):
    def __init__(self):
        self.base_url = "https://api.binance.com/api/v3"

    async def fetch_candles(self, symbol: str, timeframe: str, limit: int = 100) -> List[Candle]:
        # Converter timeframes comuns para o formato da Binance
        binance_interval = self._map_timeframe(timeframe)
        
        url = f"{self.base_url}/klines"
        params = {
            "symbol": symbol.upper(),
            "interval": binance_interval,
            "limit": limit
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
        candles = []
        for item in data:
            # Formato da Binance: [Open time, Open, High, Low, Close, Volume, ...]
            candles.append(Candle(
                timestamp=datetime.fromtimestamp(item[0] / 1000.0),
                open=float(item[1]),
                high=float(item[2]),
                low=float(item[3]),
                close=float(item[4]),
                volume=float(item[5])
            ))
        return candles

    def _map_timeframe(self, timeframe: str) -> str:
        mapping = {
            "1m": "1m", "5m": "5m", "15m": "15m", "1h": "1h", "4h": "4h", "1d": "1d"
        }
        return mapping.get(timeframe, "1h")
