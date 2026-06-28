from datetime import datetime
from meta.contracts.layer_output import LayerOutput

class Camada04DrawOnLiquidity:
    def __init__(self):
        self.name = "DrawOnLiquidity"

    def run(self, dealing_range: LayerOutput, quarterly: LayerOutput) -> LayerOutput:
        if not dealing_range.valid:
            return LayerOutput(
                id=f"draw_{datetime.now().timestamp()}",
                timestamp=datetime.now(), layer_name=self.name,
                semantic_type="DrawOnLiquidity",
                confidence=0, valid=False, evidence=["Invalid dealing range"]
            )
        bias = quarterly.payload.get('bias', 'bullish')
        direction = "buy_side" if bias == "bullish" else "sell_side"
        level = dealing_range.payload['high'] if direction == "buy_side" else dealing_range.payload['low']
        return LayerOutput(
            id=f"draw_{datetime.now().timestamp()}",
            timestamp=datetime.now(), layer_name=self.name,
            semantic_type="DrawOnLiquidity",
            confidence=0.9,
            valid=True,
            evidence=[f"Draw on {direction} at {level}"],
            payload={"direction": direction, "level": level}
        )
