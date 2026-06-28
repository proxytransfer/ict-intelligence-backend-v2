from sklearn.linear_model import LogisticRegression
from .base_ml import BaseSpecialist

class MetaModel(BaseSpecialist):
    def __init__(self):
        super().__init__()
        self.model = LogisticRegression(random_state=42)
        
    def fit(self, X, y):
        self.model.fit(X, y)
        
    def predict_proba(self, X):
        return self.model.predict_proba(X)[:, 1]
