from sklearn.ensemble import RandomForestClassifier
from .base_ml import BaseSpecialist

class MSSQualityModel(BaseSpecialist):
    def __init__(self):
        super().__init__()
        self.model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
        
    def fit(self, X, y):
        self.model.fit(X, y)
        
    def predict_proba(self, X):
        return self.model.predict_proba(X)[:, 1]
