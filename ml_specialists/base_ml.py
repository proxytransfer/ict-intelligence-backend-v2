import joblib
from abc import ABC, abstractmethod

class BaseSpecialist(ABC):
    def __init__(self):
        self.model = None
        
    @abstractmethod
    def fit(self, X, y):
        pass
        
    @abstractmethod
    def predict_proba(self, X):
        pass
        
    def save(self, path):
        if self.model is not None:
            joblib.dump(self.model, path)
            
    def load(self, path):
        self.model = joblib.load(path)
