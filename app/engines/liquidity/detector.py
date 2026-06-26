from collections import deque
from typing import List
from ...domain.candle import Candle
from ...domain.liquidity import LiquidityZone, ZoneType

class EfficientLiquidityDetector:
    def __init__(self):
        self.zones: List[LiquidityZone] = []
        self.recent_candles = deque(maxlen=200)

    def update(self, candles: List[Candle]):
        for candle in candles:
            self.recent_candles.append(candle)
            self._detect_pivots()
            self._check_sweeps(candle)
            self._detect_fvg()

    def _detect_pivots(self):
        if len(self.recent_candles) < 3:
            return
        
        c1, c2, c3 = list(self.recent_candles)[-3:]
        
        # BSL (Buy Side Liquidity) - Pivot High
        if c2.high > c1.high and c2.high > c3.high:
            self.zones.append(LiquidityZone(
                price_level=c2.high,
                zone_type=ZoneType.BSL,
                strength=self._calc_strength(c2.high)
            ))
            
        # SSL (Sell Side Liquidity) - Pivot Low
        if c2.low < c1.low and c2.low < c3.low:
            self.zones.append(LiquidityZone(
                price_level=c2.low,
                zone_type=ZoneType.SSL,
                strength=self._calc_strength(c2.low)
            ))

    def _check_sweeps(self, candle: Candle):
        for zone in self.zones:
            if not zone.swept:
                if zone.zone_type == ZoneType.BSL and candle.high > zone.price_level:
                    zone.swept = True
                elif zone.zone_type == ZoneType.SSL and candle.low < zone.price_level:
                    zone.swept = True

    def _detect_fvg(self):
        if len(self.recent_candles) < 3:
            return
        c1, c2, c3 = list(self.recent_candles)[-3:]
        
        # Bullish FVG
        if c1.high < c3.low:
            self.zones.append(LiquidityZone(
                price_level=(c1.high + c3.low) / 2,
                zone_type=ZoneType.FVG,
                strength=0.8
            ))
        # Bearish FVG
        if c1.low > c3.high:
            self.zones.append(LiquidityZone(
                price_level=(c1.low + c3.high) / 2,
                zone_type=ZoneType.FVG,
                strength=0.8
            ))

    def _calc_strength(self, price: float) -> float:
        # Simplified strength calculation
        return 0.7

    def get_active_zones(self) -> List[LiquidityZone]:
        return [z for z in self.zones if not z.swept]
