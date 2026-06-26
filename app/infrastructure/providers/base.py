from abc import ABC, abstractmethod
from typing import List
from ...domain.candle import Candle
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type

class ProviderError(Exception):
    pass

class BaseProvider(ABC):
    @abstractmethod
    async def fetch_candles(self, symbol: str, timeframe: str, limit: int) -> List[Candle]:
        pass

    def validate_and_fill_gaps(self, candles: List[Candle], timeframe_minutes: int) -> List[Candle]:
        # Implementation for gap filling
        if not candles:
            return []
        
        filled_candles = [candles[0]]
        for i in range(1, len(candles)):
            prev = filled_candles[-1]
            curr = candles[i]
            diff = (curr.timestamp - prev.timestamp).total_seconds() / 60
            
            if diff > 2 * timeframe_minutes:
                # Fill gap with flat candle
                pass # Logic to be implemented
            filled_candles.append(curr)
        return filled_candles
