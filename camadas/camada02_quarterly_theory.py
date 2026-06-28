import pandas as pd
from datetime import datetime
from meta.contracts.layer_output import LayerOutput

class Camada02QuarterlyTheory:
    def __init__(self):
        self.name = "QuarterlyTheory"

    def run(self, data: pd.DataFrame, macro_output: LayerOutput) -> LayerOutput:
        # data: OHLCV mensal/semanal com colunas 'open', 'high', 'low', 'close'
        if data.empty:
            return LayerOutput(
                id=f"qt_{datetime.now().timestamp()}",
                timestamp=datetime.now(), layer_name=self.name,
                semantic_type="QuarterlyPosition",
                confidence=0, valid=False, evidence=["No data"]
            )
        first_open = data.iloc[0]['open']
        last_close = data.iloc[-1]['close']
        bias = "bullish" if last_close > first_open else "bearish"
        quarter = (datetime.now().month - 1) // 3 + 1
        alignment = self._fractal_alignment(data, bias)
        return LayerOutput(
            id=f"qt_{datetime.now().timestamp()}",
            timestamp=datetime.now(),
            layer_name=self.name,
            semantic_type="QuarterlyPosition",
            confidence=alignment,
            valid=alignment > 0.5,
            evidence=[f"Q{quarter} bias {bias}, alignment {alignment:.2f}"],
            payload={"quarter": quarter, "bias": bias, "fractal_alignment": alignment}
        )

    def _fractal_alignment(self, data, bias):
        # Simples: verifica se últimos candles semanais concordam
        recent = data.tail(4)
        if bias == 'bullish':
            return sum(recent['close'] > recent['open']) / 4
        else:
            return sum(recent['close'] < recent['open']) / 4
