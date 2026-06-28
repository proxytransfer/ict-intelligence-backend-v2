import os
import pandas as pd
from ml_specialists.mss_quality_model import MSSQualityModel
from ml_specialists.smt_reliability_model import SMTReliabilityModel
from ml_specialists.fvg_efficiency_model import FVGEfficiencyModel
from ml_specialists.meta_model import MetaModel

def train_all_models():
    print("Training ML specialists...")
    
    # Simulate loading data from EventStore (Parquet)
    # X_train = pd.read_parquet('data/events/features.parquet')
    # y_train = pd.read_parquet('data/events/labels.parquet')
    
    # Mock data for demonstration purposes
    import numpy as np
    X_train = np.random.rand(100, 5)
    y_train = np.random.randint(0, 2, 100)
    
    # Train specialists
    mss_model = MSSQualityModel()
    mss_model.fit(X_train, y_train)
    mss_model.save('data/models/mss_model.pkl')
    
    smt_model = SMTReliabilityModel()
    smt_model.fit(X_train, y_train)
    smt_model.save('data/models/smt_model.pkl')
    
    fvg_model = FVGEfficiencyModel()
    fvg_model.fit(X_train, y_train)
    fvg_model.save('data/models/fvg_model.pkl')
    
    # Train meta model
    meta_model = MetaModel()
    
    # Generate predictions from specialists to train meta model
    preds_mss = mss_model.predict_proba(X_train)
    preds_smt = smt_model.predict_proba(X_train)
    preds_fvg = fvg_model.predict_proba(X_train)
    
    X_meta = np.column_stack((preds_mss, preds_smt, preds_fvg))
    meta_model.fit(X_meta, y_train)
    meta_model.save('data/models/meta_model.pkl')
    
    print("All models trained and saved to data/models/")

if __name__ == "__main__":
    os.makedirs('data/models', exist_ok=True)
    train_all_models()
