from datetime import datetime
from ..domain.analysis import AnalysisReport
from ..engines.liquidity.detector import EfficientLiquidityDetector
from ..engines.quarterly.state_machine import QuarterStateMachine
from ..engines.probability.calibrator import ScoreCalibrator
from ..core.config import get_settings

class AnalysisOrchestrator:
    def __init__(self, cache, provider):
        self.cache = cache
        self.provider = provider
        self.liquidity_detector = EfficientLiquidityDetector()
        self.quarterly_engine = QuarterStateMachine()
        self.settings = get_settings()
        self.calibrator = ScoreCalibrator(k=self.settings.CALIBRATION_K)

    async def get_full_analysis(self, symbol: str) -> AnalysisReport:
        # 1. Fetch candles
        candles = await self.provider.fetch_candles(symbol, "1h", 100)
        
        # 2. Update engines
        self.liquidity_detector.update(candles)
        
        # 3. Calculate score (simplified)
        raw_score = 65.0 # Example
        
        # 4. Calibrate probability
        prob = self.calibrator.probability(raw_score)
        
        # 5. Build report
        report = AnalysisReport(
            symbol=symbol,
            timestamp=datetime.now(),
            raw_score=raw_score,
            calibrated_probability=prob,
            direction="BULLISH" if raw_score > 0 else "BEARISH",
            confidence="HIGH" if prob > 0.7 else "MEDIUM",
            components={"liquidity": 70, "quarterly": 60},
            active_zones=self.liquidity_detector.get_active_zones(),
            scenario="BULLISH_EXPANSION",
            targets=[candle.close * 1.02 for candle in candles[-1:]]
        )
        return report
