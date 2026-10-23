# AstroGuard AI — NASA Inspiration4 edition

AstroGuard AI is a research/hackathon prototype that explores real astronaut biological measurements and flags statistically unusual biomarker patterns for human review.

## Real public dataset

**NASA Open Science Data Repository (OSDR), study OSD-575** — *SpaceX Inspiration4 Blood Serum Metabolic Panel and Immune/Cardiac Cytokine Arrays*.

- Official study page: https://osdr.nasa.gov/bio/repo/data/studies/OSD-575
- Mission: Inspiration4, a four-person civilian crew on a three-day spaceflight in September 2021.
- Measures: comprehensive metabolic panel and immune/cardiovascular cytokine biomarkers from serum.
- OSD-575 samples are described at pre-flight time points (L-92, L-44, L-3) and post-flight time points (R+1, R+45, R+82).
- License shown on the study page: CC0-1.0.
- NASA notes that processed astronaut-derived data are publicly accessible, while some raw/sequence data require controlled access.

This is **real spaceflight astronaut data**, not simulated data. Important limitation: OSD-575 is a small biological sample study, not continuous live heart-rate, SpO2, or wearable telemetry. AstroGuard AI therefore uses descriptive analysis and Isolation Forest for exploratory anomaly flagging; it cannot claim validated prediction of an astronaut medical emergency.

## Setup

```bash
python -m venv .venv
# Windows:
.venv\\Scripts\\activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
```

## Get NASA data

Run:

```bash
python scripts/download_osdr_inspiration4.py
```

The script queries NASA's public OSDR data-file API for study OSD-575 and downloads files exposed by the API. NASA's API/file layout can change. If automatic discovery fails, open the official OSD-575 study page and use its Files panel to download available data/metadata manually. Put extracted CSV/TSV/XLSX files into `data/raw/`.

API endpoint used: `https://osdr.nasa.gov/osdr/data/osd/files/575/?page=0&size=25`
Official API information: https://api.nasa.gov/ (Open Science Data Repository Public API).

## Run the dashboard

```bash
streamlit run app.py
```

In the sidebar, select a downloaded table from `data/raw/` or upload one. The dashboard identifies numeric columns, visualizes distributions and relationships, and uses an unsupervised scikit-learn Isolation Forest pipeline (median imputation, feature scaling, anomaly flags, and anomaly scores) to flag unusual records. The analyzed output includes `anomaly_flag` (1 = flagged, 0 = not flagged) and `anomaly_score` (more negative values indicate more unusual records for this model). These are exploratory flags, not medical diagnoses. It does not assume the data contain heart rate or oxygen saturation.

## Analysis workflow

1. Verify the source file and data dictionary/metadata.
2. Inspect column names, units, missingness, sample identifiers, and collection time points.
3. Keep identifiers and categorical columns out of the anomaly model.
4. Use numeric biomarker columns for exploratory anomaly detection.
5. Interpret flags as unusual values for review, not as illness or a diagnosis.
6. Compare time points only when the dataset's metadata explicitly supports the mapping.

## Run tests

```bash
pytest -q
```

## Project layout

```text
AstroGuard-AI-NASA-OSD575/
├── app.py
├── requirements.txt
├── README.md
├── data/raw/
├── scripts/download_osdr_inspiration4.py
├── src/data_processing.py
├── src/anomaly_detection.py
├── notebooks/01_osd575_exploration.py
└── tests/test_anomaly_detection.py
```


## Model choice: Isolation Forest now; Random Forest later if justified

**Current primary model: Isolation Forest.** The uploaded OSD-575 CMP table contains biomarker measurements and metadata, but no obvious verified health-outcome target. Isolation Forest can flag unusual combinations without requiring labelled outcomes. Its flags are exploratory and are not diagnoses.

**Random Forest is a future/optional model**, not the main model for this dataset. A Random Forest classifier requires a verified categorical target, and a regressor requires a meaningful numeric target. Do not invent labels, use `RANGE_MIN`/`RANGE_MAX` to manufacture health labels, or treat Isolation Forest flags as ground-truth outcomes. If a valid target is later established in a suitable dataset, `src/random_forest.py` provides an optional utility to evaluate a supervised model. Results must not be described as clinical validation.

