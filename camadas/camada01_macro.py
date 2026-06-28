from datetime import datetime
from meta.contracts.layer_output import LayerOutput

class Camada01Macro:
    def __init__(self):
        self.name = "MacroContext"

    def run(self, context: dict) -> LayerOutput:
        # Entrada: dados macroeconômicos (DXY, VIX, yields)
        dxy_trend = context.get("dxy_trend", 0)
        vix = context.get("vix", 20)
        if dxy_trend > 0 and vix > 25:
            regime = "Risk-Off"
        elif dxy_trend < 0 and vix < 20:
            regime = "Risk-On"
        else:
            regime = "Neutral"
        bias = "bearish" if regime == "Risk-Off" else "bullish"
        return LayerOutput(
            id=f"macro_{datetime.now().timestamp()}",
            timestamp=datetime.now(),
            layer_name=self.name,
            semantic_type="MacroContext",
            confidence=0.9,
            valid=True,
            evidence=[f"DXY trend {dxy_trend}, VIX {vix}"],
            payload={"regime": regime, "bias": bias, "dxy": dxy_trend, "vix": vix}
        )
