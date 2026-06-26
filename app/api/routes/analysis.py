from fastapi import APIRouter, HTTPException
from ...services.analysis_orchestrator import AnalysisOrchestrator
from ...infrastructure.cache.local_cache import LocalCache
from ...infrastructure.providers.base import BaseProvider
from ...domain.candle import Candle
from datetime import datetime
from typing import List

router = APIRouter()

# Mock provider for implementation
class MockProvider(BaseProvider):
    async def fetch_candles(self, symbol: str, timeframe: str, limit: int) -> List[Candle]:
        return [
            Candle(datetime.now(), 100, 105, 95, 102, 1000, timeframe)
            for _ in range(limit)
        ]

cache = LocalCache("/tmp/cache.db")
provider = MockProvider()
orchestrator = AnalysisOrchestrator(cache, provider)

@router.get("/{symbol}")
async def get_analysis(symbol: str):
    try:
        report = await orchestrator.get_full_analysis(symbol)
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
