from fastapi import APIRouter, HTTPException
from ...services.analysis_orchestrator import AnalysisOrchestrator

router = APIRouter()

@router.get("/{symbol}")
async def get_analysis(symbol: str):
    try:
        # Agora o orquestrador usa o BinanceProvider internamente
        orchestrator = AnalysisOrchestrator()
        report = await orchestrator.get_full_analysis(symbol)
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
