import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from .data_processing import numeric_columns


def detect_anomalies(df: pd.DataFrame, selected_features=None, contamination=0.08):
    """Run exploratory unsupervised ML; flags are not health diagnoses."""
    result = df.copy()
    features = selected_features or numeric_columns(result)
    features = [c for c in features if c in result.columns]
    usable = result[features].copy() if features else pd.DataFrame(index=result.index)
    for col in usable.columns:
        usable[col] = pd.to_numeric(usable[col], errors="coerce")
    usable = usable.replace([np.inf, -np.inf], np.nan)
    result["anomaly_flag"] = 0
    result["anomaly_score"] = np.nan
    if not features:
        return result, [], "No numeric biomarker columns were found. Choose a measurement table."
    valid = usable.notna().any(axis=1)
    n_valid = int(valid.sum())
    if n_valid < 10:
        return result, features, (f"Only {n_valid} usable records found. At least 10 are required for this exploratory "
                                  "Isolation Forest run. No records were flagged.")
    contamination = float(np.clip(contamination, 0.01, 0.20))
    pipeline = make_pipeline(SimpleImputer(strategy="median"), StandardScaler(),
        IsolationForest(n_estimators=200, contamination=contamination, random_state=42))
    pipeline.fit(usable.loc[valid])
    predictions = pipeline.predict(usable.loc[valid])
    scores = pipeline.decision_function(usable.loc[valid])
    result.loc[valid, "anomaly_flag"] = (predictions == -1).astype(int)
    result.loc[valid, "anomaly_score"] = scores
    flagged_count = int((predictions == -1).sum())
    note = (f"Unsupervised ML: Isolation Forest trained on {n_valid} usable records and {len(features)} selected numeric "
            f"feature(s). It flagged {flagged_count} record(s). More negative anomaly scores indicate more unusual records. "
            "These are exploratory statistical flags—not diagnoses, clinical risk scores, or validated emergency predictions.")
    return result, features, note
