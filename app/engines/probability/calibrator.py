import math
from typing import List

class ScoreCalibrator:
    def __init__(self, k: float = 20.0):
        self.k = k
        self.fitted = False

    def probability(self, score: float) -> float:
        # Logistic fallback: P = 1 / (1 + exp(-score / K))
        # score is expected to be between -100 and 100
        try:
            return 1 / (1 + math.exp(-score / self.k))
        except OverflowError:
            return 1.0 if score > 0 else 0.0

    def fit(self, scores: List[float], outcomes: List[int]):
        # To be implemented with IsotonicRegression if needed
        self.fitted = True
