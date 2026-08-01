# Synthea patient analytical table

This workflow converts an already inspected local Synthea CSV snapshot into a deterministic one-row-per-patient table for BMB831 practice.

## Scientific boundary

The source records and every derived artifact remain synthetic. A successful build demonstrates reproducible data engineering, structural validity, temporal feature construction, and patient-level separation. It does not demonstrate epidemiological representativeness, clinical validity, clinical utility, absence of generator bias, or suitability as omics evidence.

## Required source files

The input directory must contain the four tables accepted by `cb-synthea-inspect`:

- `patients.csv`
- `encounters.csv`
- `conditions.csv`
- `observations.csv`

The builder runs the snapshot inspector first. Any error-level contract finding stops derivation before the output CSV is written.

## Build command

```powershell
cb-synthea-build-patient-table "D:\datasets\synthea\csv" `
  --output "artifacts\synthea_patient_table.csv" `
  --metadata "artifacts\synthea_patient_table.metadata.json" `
  --source-label "synthea-local-2026-08-01" `
  --window-days 365 `
  --train-percent 70 `
  --validation-percent 15 `
  --test-percent 15 `
  --split-salt "synthea-patient-table-v1"
```

Linux or macOS:

```bash
cb-synthea-build-patient-table data/synthea/csv \
  --output artifacts/synthea_patient_table.csv \
  --metadata artifacts/synthea_patient_table.metadata.json \
  --source-label synthea-local-2026-08-01 \
  --window-days 365 \
  --train-percent 70 \
  --validation-percent 15 \
  --test-percent 15 \
  --split-salt synthea-patient-table-v1
```

## Cohort and index definition

The current version uses a deliberately explicit teaching contract:

1. one candidate row begins with one unique patient from `patients.csv`;
2. the patient-specific index date is the latest `START` date in `encounters.csv`;
3. patients without a valid encounter-derived index date are excluded and counted in metadata;
4. the feature window is `[index_date - window_days, index_date)`;
5. events on the index date are excluded from every event-derived feature.

The strict upper boundary is intended to make temporal leakage visible. This table does not yet define a clinical outcome. Outcome construction, prediction horizons, censoring, and task-specific inclusion criteria belong to a later modelling contract.

## Derived variables

The output preserves a fixed column order and includes:

- patient identifier, birthdate, gender, index date, and age at index;
- feature-window boundaries;
- deterministic `train`, `validation`, or `test` assignment by patient ID;
- encounter count and number of encounter classes before index;
- condition-event count and number of unique condition codes before index;
- observation count and parseable numeric-observation count before index;
- latest pre-index BMI, systolic blood pressure, and diastolic blood pressure values with dates and units.

Target measurements use exact Synthea/LOINC codes:

| Measurement | Code |
|---|---|
| Body mass index | `39156-5` |
| Systolic blood pressure | `8480-6` |
| Diastolic blood pressure | `8462-4` |

The builder records units instead of silently assuming that all values use the same unit system. Unit harmonisation and plausibility ranges remain separate validation tasks.

## Patient-level split

Split assignment is calculated from a SHA-256 hash of the stable salt and patient ID. This provides:

- no encounter-level leakage across partitions;
- reproducible assignment when the same snapshot and salt are reused;
- no dependence on input row order or local file paths.

The current hash split does not guarantee class balance because no outcome exists yet. Once an outcome contract is defined, stratified or grouped resampling must be implemented without moving records from the same patient across partitions.

## Metadata and reproducibility

The metadata JSON records:

- source snapshot fingerprint;
- feature-window and split configuration;
- output CSV SHA-256;
- stable column contract;
- number of included patients;
- number excluded for lacking an index encounter;
- path-independent artifact fingerprint;
- synthetic-data and leakage-control statements.

Two builds from byte-identical source tables and the same configuration should produce the same output checksum and artifact fingerprint, even when stored in different directories.

## Current limitations

This first analytical table intentionally does not yet provide:

- a clinical outcome or prediction horizon;
- censoring or survival-time definitions;
- code-system harmonisation beyond three exact measurement codes;
- implausible-value detection;
- missing-data mechanism analysis or imputation;
- comorbidity groupers;
- medication or procedure features;
- longitudinal slopes or variability features;
- outcome-aware stratification;
- model fitting or performance evaluation;
- epidemiological or clinical claims.

These are subsequent priority-zero and BMB831 increments rather than hidden assumptions in the current table.
