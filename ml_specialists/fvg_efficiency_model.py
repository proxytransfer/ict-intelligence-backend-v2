from sklearn.ensemble import GradientBoostingClassifier
from .base_ml import BaseSpecialist

class FVGEfficiencyModel(BaseSpecialist):
    def __init__(self):
        super().__init__()
        self.model = GradientBoostingClassifier(n_estimators=100, max_depth=3, random_state=42)
        
    def fit(self, X, y):
        self.model.fit(X, y)
        
    def predict_proba(self, X):
        return self.model.predict_proba(X)[:, 1]
