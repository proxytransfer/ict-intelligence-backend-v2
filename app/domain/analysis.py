from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict
from .liquidity import LiquidityZone

@dataclass
class AnalysisReport:
    symbol: str
    timestamp: datetime
    raw_score: float
    calibrated_probability: float  # 0 a 1
    direction: str  # "BULLISH", "BEARISH", "NEUTRAL"
    confidence: str # "HIGH", "MEDIUM", "LOW"
    components: Dict # {quarterly: 82, liquidity: 68, ...}
    active_zones: List[LiquidityZone]
    scenario: str   # "BULLISH_EXPANSION"...
    targets: List[float]
