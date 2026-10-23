import pandas as pd
from src.anomaly_detection import detect_anomalies


def test_anomaly_detector_adds_flags_and_scores():
    df = pd.DataFrame({"biomarker_a": list(range(20)) + [1000], "biomarker_b": list(range(20)) + [-1000],
                       "sample_id": [f"S{i}" for i in range(21)]})
    result, features, note = detect_anomalies(df, ["biomarker_a", "biomarker_b"], contamination=0.05)
    assert "anomaly_flag" in result.columns and "anomaly_score" in result.columns
    assert set(result["anomaly_flag"].unique()).issubset({0, 1})
    assert result["anomaly_score"].notna().sum() == len(df)
    assert len(features) == 2 and "Isolation Forest" in note


def test_small_dataset_does_not_claim_model_was_run():
    result, features, note = detect_anomalies(pd.DataFrame({"biomarker": [1, 2, 3]}), ["biomarker"])
    assert result["anomaly_flag"].sum() == 0
    assert result["anomaly_score"].isna().all()
    assert "At least 10" in note
