from datetime import datetime
from ..domain.analysis import AnalysisReport
from ..engines.liquidity.detector import EfficientLiquidityDetector
from ..engines.quarterly.state_machine import QuarterStateMachine
from ..engines.probability.calibrator import ScoreCalibrator
from ..core.config import get_settings
from ..services.data_service import DataService

class AnalysisOrchestrator:
    def __init__(self, cache=None, provider=None):
        self.settings = get_settings()
        self.data_service = DataService()
        self.liquidity_detector = EfficientLiquidityDetector()
        self.quarterly_engine = QuarterStateMachine()
        self.calibrator = ScoreCalibrator(k=self.settings.CALIBRATION_K)

    async def get_full_analysis(self, symbol: str) -> AnalysisReport:
        # 1. Fetch real market data from Binance
        candles = await self.data_service.get_market_data(symbol, "1h")
        
        # 2. Update engines with real data
        self.liquidity_detector.update(candles)
        
        # 3. Calculate score based on market state
        # (Lógica simplificada para exemplo, integrando os motores)
        raw_score = 70.0 
        
        # 4. Calibrate probability
        prob = self.calibrator.probability(raw_score)
        
        # 5. Build report
        report = AnalysisReport(
            symbol=symbol,
            timestamp=datetime.now(),
            raw_score=raw_score,
            calibrated_probability=prob,
            direction="BULLISH" if raw_score > 50 else "BEARISH",
            confidence="HIGH" if prob > 0.7 else "MEDIUM",
            components={"liquidity": 75, "quarterly": 65},
            active_zones=self.liquidity_detector.get_active_zones(),
            scenario="REAL_TIME_ANALYSIS",
            targets=[candles[-1].close * 1.02] if candles else []
        )
        return report
