# SQL Analysis — Healthcare Readmissions

## Overview

This folder contains seven SQL queries investigating patterns associated with 30-day hospital readmissions.

The analysis uses the UCI Diabetes 130-US Hospitals dataset (1999–2008), containing 101,766 hospital encounters.

SQLite was used to calculate readmission rates, compare patient groups, and examine relationships between hospital utilization characteristics.

## SQL Query Overview

| File | Analytical Purpose |
|---|---|
| 01_readmission_overview.sql | Calculate overall 30-day readmission statistics |
| 02_readmission_by_age.sql | Compare readmission rates across age groups |
| 03_readmission_by_inpatient_visits.sql | Analyze previous inpatient utilization |
| 04_readmission_by_hospital_stay.sql | Compare readmission rates by hospital length of stay |
| 05_readmission_by_medications.sql | Examine readmission rates across medication-count groups |
| 06_combined_risk_analysis.sql | Investigate previous inpatient visits alongside hospital stay duration |
| 07_age_inpatient_analysis.sql | Compare readmission patterns across age and inpatient history groups |

## Key SQL Findings

### 1. Overall Readmission Rate

**Query:** `01_readmission_overview.sql`

| Metric | Result |
|---|---:|
| Total Hospital Encounters | 101,766 |
| Readmissions Within 30 Days | 11,357 |
| Encounters Without 30-Day Readmission | 90,409 |
| Readmission Rate | 11.16% |

Approximately 11.16% of hospital encounters were associated with readmission within 30 days.

### 2. Readmissions by Age

**Query:** `02_readmission_by_age.sql`

- Ages 20–30 had the highest observed readmission rate: 14.24%.
- Ages 70–80 accounted for the largest number of readmissions: 3,069.
- Ages 80–90 had a readmission rate of 12.08%.

These results demonstrate why both readmission rates and encounter volumes should be considered when comparing patient groups.

### 3. Previous Inpatient Utilization

**Query:** `03_readmission_by_inpatient_visits.sql`

| Previous Inpatient Visits | Readmission Rate |
|---|---:|
| 0 | 8.44% |
| 1 | 12.92% |
| 2 | 17.43% |
| 3–4 | 21.36% |
| 5+ | 36.41% |

Readmission rates increased across the previous inpatient utilization categories.

This suggests that inpatient history is an important characteristic for further investigation.

### 4. Hospital Length of Stay

**Query:** `04_readmission_by_hospital_stay.sql`

Selected results:

| Hospital Stay | Readmission Rate |
|---|---:|
| 1 day | 8.18% |
| 4 days | 11.81% |
| 7 days | 12.83% |
| 10 days | 14.35% |
| 14 days | 12.96% |

Longer hospital stays were often associated with higher readmission rates, although the relationship was not consistently increasing.

### 5. Medication Count

**Query:** `05_readmission_by_medications.sql`

| Medication Count | Readmission Rate |
|---|---:|
| 0–5 | 7.48% |
| 6–10 | 9.45% |
| 11–15 | 10.91% |
| 16–20 | 12.17% |
| 21+ | 12.78% |

Higher medication-count categories had higher observed readmission rates.

Medication count may reflect differences in patient complexity, but these results do not establish causation.

### 6. Combined Utilization Analysis

**Query:** `06_combined_risk_analysis.sql`

| Previous Inpatient Visits | Hospital Stay | Readmission Rate |
|---|---|---:|
| 0 | 1–3 days | 7.16% |
| 0 | 4–7 days | 9.39% |
| 1–2 | 4–7 days | 14.68% |
| 3+ | 1–3 days | 25.39% |
| 3+ | 4–7 days | 27.17% |
| 3+ | 8–14 days | 23.31% |

Encounters involving patients with three or more previous inpatient visits consistently showed elevated readmission rates across the hospital stay categories.

### 7. Age and Previous Inpatient History

**Query:** `07_age_inpatient_analysis.sql`

Selected results:

| Age Group | Previous Inpatient Visits | Readmission Rate |
|---|---|---:|
| 20–30 | 0 | 5.49% |
| 20–30 | 1–2 | 20.87% |
| 20–30 | 3+ | 41.57% |
| 70–80 | 0 | 9.56% |
| 70–80 | 3+ | 23.54% |

The 20–30 age group showed a particularly large difference across inpatient history categories.

These findings support investigating patient age and previous utilization together rather than examining each characteristic independently.

## SQL Skills Demonstrated

The analysis demonstrates:

- Aggregate functions including COUNT, SUM, and AVG
- Percentage calculations and rounding
- GROUP BY and ORDER BY
- Conditional grouping using CASE expressions
- Multi-variable subgroup analysis
- Interpretation of healthcare utilization patterns


## Running the SQL Queries

The SQL analysis uses SQLite and a table named `hospital_analysis`.

The database is generated locally using `create_database.py` and is not included in the GitHub repository.

### 1. Prepare the Dataset

Download the Diabetes 130-US Hospitals dataset from the UCI Machine Learning Repository:

https://archive.ics.uci.edu/dataset/296/diabetes+130+us+hospitals+for+years+1999+2008

Place `diabetic_data.csv` inside:

`data/raw/`

Run `01_data_cleaning.ipynb` to generate:

`data/processed/diabetes_cleaned.csv`

### 2. Create the SQLite Database

From the project's root directory, run:

```bash
python sql/create_database.py
```

This script:
- Loads the cleaned healthcare dataset.
- Selects the 18 columns used in SQL analysis.
- Creates the `hospital_analysis` table.
- Populates the SQLite database.
- Verifies the total encounters, readmissions, and readmission rate.

Expected results:

| Metric | Result |
|---|---:|
| Total Encounters | 101,766 |
| 30-Day Readmissions | 11,357 |
| Readmission Rate | 11.16% |

The database will be created at:

`sql/healthcare.db`

**Note:** Running the script again replaces the existing `hospital_analysis` table.

### 3. Run an Individual SQL Query

From the project root:

```bash
sqlite3 -header -column sql/healthcare.db < sql/01_readmission_overview.sql
```

### 4. Run All Seven SQL Queries

```bash
for file in sql/*.sql; do
    echo ""
    echo "Running: $(basename "$file")"
    sqlite3 -header -column sql/healthcare.db < "$file"
done
```

All seven queries were tested successfully against the database recreated by `create_database.py`.

### 5. Review the Findings

[View Detailed Analytical Findings](../ANALYSIS_FINDINGS.md)
