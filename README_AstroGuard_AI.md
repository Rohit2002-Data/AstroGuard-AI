# AstroGuard AI — NASA Inspiration4 Edition

AstroGuard AI is a research and hackathon prototype that explores publicly available astronaut biological measurements and flags statistically unusual biomarker patterns for human review.

> **Important limitation:** AstroGuard AI is an exploratory analysis tool. Its anomaly flags are not medical diagnoses, do not establish illness, and are not a validated system for predicting astronaut medical emergencies.

## Table of Contents

- [Project Overview](#project-overview)
- [Real Public Dataset](#real-public-dataset)
- [What the Project Does](#what-the-project-does)
- [Machine-Learning Approach](#machine-learning-approach)
- [Important Scientific Limitations](#important-scientific-limitations)
- [Requirements](#requirements)
- [Installation](#installation)
- [Get the NASA OSD-575 Data](#get-the-nasa-osd-575-data)
- [Run the Dashboard](#run-the-dashboard)
- [Analysis Workflow](#analysis-workflow)
- [Run Tests](#run-tests)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)
- [Data Use and Attribution](#data-use-and-attribution)
- [Future Improvements](#future-improvements)

## Project Overview

Spaceflight can be associated with physiological changes, making careful analysis of astronaut biological measurements an interesting research area. AstroGuard AI provides a reproducible workflow for inspecting selected biomarker tables, understanding their structure, visualizing numeric measurements, and flagging unusual records for further review.

The project is designed to support **exploratory data analysis and human review**, not to replace medical professionals or operational flight-medicine systems.

## Real Public Dataset

This project is inspired by **NASA Open Science Data Repository (OSDR), study OSD-575**:

**Study:** *SpaceX Inspiration4 Blood Serum Metabolic Panel and Immune/Cardiac Cytokine Arrays*  
**Official study page:** https://osdr.nasa.gov/bio/repo/data/studies/OSD-575

- **Mission:** Inspiration4, a four-person civilian crew mission that flew for approximately three days in September 2021.
- **Measurements described by the study:** serum comprehensive metabolic panel (CMP) and immune/cardiovascular cytokine-array biomarkers.
- **Reported sampling time points:** pre-flight L-92, L-44, and L-3; post-flight R+1, R+45, and R+82. Confirm the definitions and availability of each time point in the relevant study metadata before comparing records.
- **Study license:** the OSD-575 study page identifies CC0-1.0. Review the official page and individual file metadata for the applicable terms.
- **Access:** processed astronaut-derived data are publicly accessible; some raw or sequence data may require controlled access.

This is **real spaceflight astronaut data**, not simulated data. However, the exact files available through the study may differ, and not every file necessarily contains all biomarkers or time points.

**Dataset scope matters:** OSD-575 is a small biological sample study. It is not a continuous stream of live heart rate, oxygen saturation (SpO₂), or wearable telemetry. Do not describe it as real-time astronaut monitoring.

## What the Project Does

Depending on the table selected and its columns, AstroGuard AI can:

1. Load a supported CSV, TSV, or Excel table from `data/raw/`, or accept a table through the dashboard's upload control.
2. Inspect data shape, column names, numeric fields, and missing values.
3. Visualize distributions and relationships between numeric measurements.
4. Prepare numeric features using median imputation and feature scaling.
5. Apply an unsupervised Isolation Forest model to flag records that look unusual relative to the selected data.
6. Display or export results containing:
   - `anomaly_flag`: `1` means the record was flagged; `0` means it was not flagged.
   - `anomaly_score`: the model's anomaly score. In the current workflow, more negative values indicate records that the model considers more unusual.

The available features and outputs depend on the actual file and the implementation in the repository. Always inspect the source data and metadata before interpreting results.

## Machine-Learning Approach

### Primary model: Isolation Forest

**Isolation Forest is the current primary approach** because the uploaded OSD-575 table does not appear to provide an obvious, verified health-outcome target suitable for supervised learning.

Isolation Forest is an unsupervised anomaly-detection algorithm. It attempts to isolate observations that differ from the broader data pattern. It does not learn whether a person is healthy or ill.

The documented pipeline includes:

1. Selecting appropriate numeric biomarker columns.
2. Excluding identifiers and categorical fields from model features.
3. Imputing missing numeric values using the median.
4. Scaling numeric features.
5. Fitting Isolation Forest and generating anomaly flags and scores.

Review the code and configuration for the exact preprocessing and model settings used in a particular run.

### Optional future approach: Random Forest

Random Forest is **not the primary model for the current OSD-575 workflow**. It may be considered only if a suitable dataset includes a verified target:

- **Classifier:** requires a trustworthy categorical outcome label.
- **Regressor:** requires a meaningful numeric outcome.

Do not invent labels, manufacture health labels from `RANGE_MIN` or `RANGE_MAX`, or treat Isolation Forest predictions as ground-truth outcomes. If a valid target is established later, an optional utility such as `src/random_forest.py` may be used to evaluate a supervised model. Any reported performance must be described accurately and must not be presented as clinical validation.

## Important Scientific Limitations

- **Exploratory flags only:** an anomaly means a record is unusual relative to the model's fitted data and settings. It does not mean the person is sick.
- **Small study:** the dataset has a limited number of participants and samples; findings may not generalize to other astronauts or populations.
- **No validated emergency target:** this project does not establish a clinically verified label for a medical emergency.
- **Not continuous telemetry:** the dataset should not be represented as live heart-rate, SpO₂, or wearable data unless a separate verified source provides those measurements.
- **Metadata is essential:** units, assay details, sample identifiers, collection times, and measurement context must be checked before interpretation.
- **Time-point comparisons need evidence:** compare pre-flight and post-flight records only when the study metadata supports the mapping and the records can be matched appropriately.
- **No clinical validation claim:** do not report model accuracy as medical accuracy without a suitable labelled dataset, rigorous validation, and appropriate clinical oversight.

## Requirements

- Python 3.10 or a compatible Python version supported by the packages in `requirements.txt`
- `pip`
- Git (optional, for cloning and version control)
- A supported browser to view the Streamlit dashboard
- NASA OSDR data files downloaded from the official study or through the project's downloader

Install the project's actual dependencies from `requirements.txt`. This README does not replace that file.

## Installation

Open a terminal in the project root directory.

### 1. Create a virtual environment

**Windows (Command Prompt):**

```bash
python -m venv .venv
.venv\Scripts\activate
```

**Windows (PowerShell):**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS/Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If activation is blocked by your system's PowerShell policy, use Command Prompt or follow your organization's approved Python environment instructions.

## Get the NASA OSD-575 Data

From the project root, run:

```bash
python scripts/download_osdr_inspiration4.py
```

The downloader is intended to query NASA's public OSDR data-file API for study OSD-575 and download files exposed by the API.

**API endpoint used by the project:**

https://osdr.nasa.gov/osdr/data/osd/files/575/?page=0&size=25

**Official OSDR study page:**

https://osdr.nasa.gov/bio/repo/data/studies/OSD-575

NASA's API response and file layout may change. If automatic discovery or downloading fails:

1. Open the official OSD-575 study page.
2. Review the study metadata and **Files** panel.
3. Download the appropriate publicly available processed data and metadata.
4. Extract files as needed.
5. Place supported CSV, TSV, or Excel files in `data/raw/`.

The downloader's exact behavior depends on its current implementation and the API response. Verify downloaded files rather than assuming that every file listed by the study has been downloaded.

### Suggested raw-data location

```text
data/
└── raw/
    ├── your_downloaded_table.csv
    └── relevant_metadata_file.csv
```

Use the actual filenames you downloaded; the filenames above are examples.

## Run the Dashboard

From the project root, with the virtual environment activated and dependencies installed:

```bash
streamlit run app.py
```

In the dashboard:

1. Select a downloaded table from `data/raw/` or upload a supported file.
2. Check the columns, data types, missing values, and available numeric measurements.
3. Review the visualizations before running anomaly detection.
4. Confirm that only appropriate numeric biomarker features are used.
5. Review the flagged records and scores alongside the source metadata.

The dashboard is intended to support exploration and review. Its output should not be used on its own to make medical or operational decisions.

## Analysis Workflow

1. **Verify the source:** record the OSDR study identifier, source file, and relevant metadata.
2. **Inspect the schema:** review column names, units, data types, missingness, identifiers, and collection time points.
3. **Understand the measurements:** consult the data dictionary and assay metadata before interpreting a numeric value.
4. **Prepare features:** exclude identifiers, labels that should not be features, and categorical columns unless a justified encoding strategy is implemented.
5. **Handle missing data:** inspect missingness and apply the documented preprocessing approach.
6. **Run anomaly detection:** fit Isolation Forest to suitable numeric biomarker features.
7. **Review results:** treat flags as candidates for human review, not as health outcomes.
8. **Compare time points cautiously:** do so only when the metadata supports the comparison and the sample mapping is valid.
9. **Document limitations:** record the dataset version, selected features, preprocessing, model settings, and known limitations for reproducibility.

## Run Tests

From the project root, run:

```bash
pytest -q
```

This executes the tests available in the repository. A passing test suite checks the tested software behavior; it does not validate the model clinically or establish that anomaly flags identify illness.

## Project Structure

The intended project layout is:

```text
AstroGuard-AI-NASA-OSD575/
├── app.py
├── requirements.txt
├── README.md
├── data/
│   └── raw/                         # Downloaded data; usually not committed
├── scripts/
│   └── download_osdr_inspiration4.py
├── src/
│   ├── data_processing.py
│   ├── anomaly_detection.py
│   └── random_forest.py              # Optional, if present
├── notebooks/
│   └── 01_osd575_exploration.py
└── tests/
    └── test_anomaly_detection.py
```

The exact files may differ from this outline. For example, `src/random_forest.py` is optional and should only be listed if it actually exists in your repository.

## Troubleshooting

### The downloader fails

- Confirm that you have an internet connection.
- Open the official OSD-575 study page and check whether the files are still available.
- Inspect the API response and the downloader's error message.
- Download the appropriate processed files manually if necessary.

### No numeric columns are available

- Confirm that you selected the correct data table.
- Check whether measurements are stored as text or in a separate table.
- Review the data dictionary before converting values; do not blindly convert identifiers or categorical codes into numeric features.

### The dashboard shows too many or too few anomalies

- Review the selected features and missing-value handling.
- Check the Isolation Forest configuration, including its contamination setting, if specified.
- Remember that anomaly thresholds are model settings, not clinical thresholds.
- Compare results across reasonable settings as an exploratory sensitivity check.

### Tests cannot find a module

Run commands from the project root and confirm that dependencies are installed in the active environment. Review the repository's package/import configuration if a module still cannot be found.

## Data Use and Attribution

- Dataset source: NASA Open Science Data Repository, study OSD-575.
- Official study page: https://osdr.nasa.gov/bio/repo/data/studies/OSD-575
- API endpoint used by the downloader: https://osdr.nasa.gov/osdr/data/osd/files/575/?page=0&size=25
- The study page identifies the license as **CC0-1.0**; check the current study page and each file's metadata for details and any access restrictions.
- Do not upload controlled-access files, credentials, personal information, or data you are not authorized to redistribute.
- Keep downloaded datasets out of Git where possible if they are large or unnecessary for reproducing the code. Provide instructions for obtaining them instead.

## Future Improvements

- Add schema checks and clearer messages for unsupported files.
- Record preprocessing and model settings for reproducible runs.
- Add data-quality summaries and anomaly-review exports.
- Test the downloader against current OSDR API responses.
- Add supervised Random Forest evaluation only if a suitable, verified outcome target becomes available.
- Consider appropriate validation and domain-expert review before any higher-stakes application.

---

**Disclaimer:** AstroGuard AI is a research/hackathon prototype for exploratory analysis. It is not a medical device, does not provide medical advice, and is not validated for diagnosis, astronaut health monitoring, or emergency prediction.
