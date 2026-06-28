from enum import Enum

class NarrativePhase(Enum):
    ACCUMULATION = "accumulation"
    SWEEP = "sweep"
    REPRICING = "repricing"
    DELIVERY = "delivery"
    MITIGATION = "mitigation"
    CONTINUATION = "continuation"
    EXHAUSTION = "exhaustion"
    REVERSAL = "reversal"

class NarrativeIntent(Enum):
    BUY = "buy"
    SELL = "sell"
    NEUTRAL = "neutral"
