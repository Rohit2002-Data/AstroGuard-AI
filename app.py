from pathlib import Path
import streamlit as st
import plotly.express as px
from src.data_processing import load_table, numeric_columns, summarize
from src.anomaly_detection import detect_anomalies

st.set_page_config(page_title="AstroGuard AI", page_icon="🛰️", layout="wide")
st.title("🛰️ AstroGuard AI")
st.caption("Machine-learning prototype · NASA Inspiration4 OSD-575 · Isolation Forest anomaly detection")
st.warning("Research prototype only. OSD-575 contains biological sample measurements, not live vital signs. Anomaly flags are statistical outliers, not medical diagnoses or validated emergency predictions.")

with st.sidebar:
    st.header("Dataset")
    st.markdown("[NASA OSD-575 official study page](https://osdr.nasa.gov/bio/repo/data/studies/OSD-575)")
    data_dir = Path("data/raw")
    local_files = sorted([p for p in data_dir.iterdir() if p.is_file() and p.suffix.lower() in {".csv", ".tsv", ".txt", ".xlsx", ".xls"}]) if data_dir.exists() else []
    selected_source = st.selectbox("Choose a NASA dataset file", ["Upload a downloaded table"] + [str(p) for p in local_files])
    uploaded = st.file_uploader("Upload CSV, TSV, TXT, or Excel", type=["csv", "tsv", "txt", "xlsx", "xls"]) if selected_source == "Upload a downloaded table" else None
    contamination = st.slider("Approx. proportion of records to flag", 0.01, 0.20, 0.08, 0.01)

if selected_source == "Upload a downloaded table":
    if uploaded is None:
        st.info("Download a public OSD-575 measurement table from NASA and upload it here.")
        st.stop()
    source_obj = uploaded
else:
    source_obj = selected_source

try:
    df = load_table(source_obj)
except Exception as exc:
    st.error(f"Could not load this file: {exc}")
    st.stop()
if df.empty:
    st.error("This table has no rows.")
    st.stop()

nums = numeric_columns(df)
if not nums:
    st.warning("No numeric columns were detected. This may be a metadata file; choose a measurement table instead.")
    st.dataframe(df.head(100), use_container_width=True)
    st.stop()
with st.sidebar:
    chosen = st.multiselect("Numeric biomarker columns", nums, default=nums[:min(8, len(nums))])

df_model, used_features, model_note = detect_anomalies(df, chosen, contamination)
summary = summarize(df)
c1, c2, c3, c4 = st.columns(4)
c1.metric("Rows / samples", f"{summary['rows']:,}")
c2.metric("Columns", summary["columns"])
c3.metric("Numeric fields", len(nums))
c4.metric("ML-flagged records", int(df_model["anomaly_flag"].sum()))
overview, anomalies, quality, raw = st.tabs(["Biomarker overview", "Anomaly review", "Data quality", "Raw data"])
with overview:
    st.subheader("Distribution of selected measurements")
    if chosen:
        for col in chosen[:12]:
            st.plotly_chart(px.histogram(df_model, x=col, title=f"Distribution: {col}", marginal="box"), use_container_width=True)
        if len(chosen) >= 2:
            x_col = st.selectbox("X-axis", chosen, index=0)
            y_col = st.selectbox("Y-axis", chosen, index=1)
            plot = px.scatter(df_model, x=x_col, y=y_col, color=df_model["anomaly_flag"].astype(str), labels={"color": "Anomaly flag"}, title=f"{x_col} vs {y_col}")
            st.plotly_chart(plot, use_container_width=True)
    st.caption("Confirm each biomarker's meaning and units in NASA's metadata before interpretation.")
with anomalies:
    st.subheader("Machine-learning anomaly review")
    st.write(model_note)
    flagged = df_model[df_model["anomaly_flag"] == 1].sort_values("anomaly_score", ascending=True) if "anomaly_score" in df_model else df_model[df_model["anomaly_flag"] == 1]
    st.caption("Records are ordered from more unusual to less unusual when anomaly scores are available.")
    st.dataframe(flagged if not flagged.empty else df_model.iloc[0:0], use_container_width=True)
    st.download_button("Download analyzed table", df_model.to_csv(index=False).encode("utf-8"), "astroguard_osd575_analyzed.csv", "text/csv")
with quality:
    st.json({"rows": summary["rows"], "columns": summary["columns"], "numeric_columns": nums, "missing_values_by_column": {str(k): int(v) for k, v in df.isna().sum().items()}, "duplicate_rows": summary["duplicate_rows"]})
with raw:
    st.dataframe(df.head(500), use_container_width=True)
    st.caption(f"Loaded from: {selected_source if isinstance(selected_source, str) else uploaded.name}")
st.divider()
st.caption("Source: NASA OSDR OSD-575, Inspiration4 blood serum metabolic and immune/cardiac cytokine measurements.")
