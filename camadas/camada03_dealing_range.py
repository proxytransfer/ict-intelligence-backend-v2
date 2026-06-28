import pandas as pd
import numpy as np
from datetime import datetime
from meta.contracts.layer_output import LayerOutput

class Camada03DealingRange:
    def __init__(self):
        self.name = "DealingRange"

    def run(self, data: pd.DataFrame, quarterly_output: LayerOutput) -> LayerOutput:
        # data: OHLCV diário/H4
        if len(data) < 20:
            return LayerOutput(
                id=f"dr_{datetime.now().timestamp()}",
                timestamp=datetime.now(), layer_name=self.name,
                semantic_type="DealingRange",
                confidence=0, valid=False, evidence=["Insufficient data"]
            )
        # Identificar swings simples: pivots com 5 velas esq/dir
        highs = self._find_swing_highs(data, 5)
        lows = self._find_swing_lows(data, 5)
        if not highs or not lows:
            return LayerOutput(
                id=f"dr_{datetime.now().timestamp()}",
                timestamp=datetime.now(), layer_name=self.name,
                semantic_type="DealingRange",
                confidence=0, valid=False, evidence=["No swings found"]
            )
        range_high = max(highs[-1], highs[-2]) if len(highs) >= 2 else highs[-1]
        range_low = min(lows[-1], lows[-2]) if len(lows) >= 2 else lows[-1]
        mid = (range_high + range_low) / 2
        atr = self._atr(data, 20)
        valid = (range_high - range_low) > atr
        return LayerOutput(
            id=f"dr_{datetime.now().timestamp()}",
            timestamp=datetime.now(), layer_name=self.name,
            semantic_type="DealingRange",
            confidence=0.8 if valid else 0.3,
            valid=valid,
            evidence=[f"Range H:{range_high} L:{range_low} ATR:{atr}"],
            payload={"high": range_high, "low": range_low, "mid": mid, "atr": atr}
        )

    def _find_swing_highs(self, df, window):
        swings = []
        for i in range(window, len(df) - window):
            if df['high'].iloc[i] == df['high'].iloc[i-window:i+window+1].max():
                swings.append(df['high'].iloc[i])
        return swings

    def _find_swing_lows(self, df, window):
        swings = []
        for i in range(window, len(df) - window):
            if df['low'].iloc[i] == df['low'].iloc[i-window:i+window+1].min():
                swings.append(df['low'].iloc[i])
        return swings

    def _atr(self, df, period):
        high, low, close = df['high'], df['low'], df['close']
        tr = np.maximum(high - low, np.maximum(abs(high - close.shift()), abs(low - close.shift())))
        return tr.rolling(period).mean().iloc[-1]
