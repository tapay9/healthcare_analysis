# Healthcare Readmission Analysis — Key Findings

## Advanced Finding 1: Previous Inpatient Visits and Hospital Stay Length

This analysis examined how previous inpatient visits and hospital stay duration were associated with 30-day readmission rates across 101,766 hospital encounters.

The results showed that encounters involving patients with more previous inpatient visits generally had higher readmission rates across all hospital-stay categories.

The highest readmission rate (27.17%) occurred among encounters with three or more previous inpatient visits and hospital stays of 4–7 days. In comparison, encounters with no previous inpatient visits and stays of 1–3 days had the lowest readmission rate (7.16%).

Interestingly, among encounters involving three or more previous inpatient visits, the readmission rate decreased to 23.31% for hospital stays of 8–14 days.

These findings suggest that previous inpatient utilization may be a useful indicator of readmission risk, even when considering hospital stay duration. However, the observed associations do not establish causation, and additional factors such as illness severity and patient characteristics may influence the results.

**Key takeaway:** Previous inpatient history is associated with substantial differences in 30-day readmission rates across hospital-stay groups.

## Advanced Finding 2: Age Group and Previous Inpatient History

This analysis examined the relationship between age, previous inpatient visits, and 30-day hospital readmissions.

Across age groups, encounters involving patients with more previous inpatient visits generally had higher readmission rates. The largest observed rate was among patients aged 20–30 with three or more previous inpatient visits, where 41.57% of 255 encounters resulted in readmission within 30 days.

For the same age group, encounters with no previous inpatient visits had a readmission rate of only 5.49%. This substantial difference suggests that previous inpatient utilization may provide important information beyond age alone.

Interestingly, among encounters with three or more previous inpatient visits, the observed readmission rate was lower in older age groups, including 23.54% for ages 70–80 and 17.86% for ages 90–100.

However, these findings are descriptive and do not establish causation. Differences in sample sizes, underlying medical conditions, and repeated encounters involving the same patients may influence the results.

**Key takeaway:** Previous inpatient utilization is strongly associated with 30-day readmission rates across age groups, suggesting that combining patient characteristics and utilization history may provide more useful insights than examining age alone.

## Executive Summary

### Project Overview

This project analyzes 101,766 hospital encounters involving 71,518 unique patients from the UCI Diabetes 130-US Hospitals dataset (1999–2008). The objective is to identify patterns associated with hospital readmissions within 30 days of discharge and evaluate whether historical patient and hospitalization characteristics can support predictive modeling.

Using Python, Pandas, SQL, SQLite, Scikit-learn, and Streamlit, the project combines data cleaning, exploratory analysis, database querying, machine learning, and interactive visualization.

### Key Analytical Findings

**1. Previous Hospitalizations Are Strongly Associated with Readmissions**

Encounters involving patients with no previous inpatient visits had an 8.44% readmission rate, compared with 36.41% for those with five or more previous inpatient visits.

This suggests that previous hospital utilization is an important factor to investigate when identifying patients who may require additional support after discharge.

**2. Readmission Rates Vary Across Age Groups**

The 20–30 age group had the highest observed readmission rate at 14.24%, while the 70–80 age group accounted for the largest number of readmissions, with 3,069 encounters.

This distinction demonstrates why healthcare analysts should evaluate both percentages and patient volumes when interpreting population-level trends.

**3. Hospitalization Characteristics Show Additional Associations**

Readmission rates generally increased with medication counts, rising from 7.48% among encounters involving 0–5 medications to 12.78% among those involving 21 or more medications.

Hospital length of stay also showed an association with readmissions, although the relationship was not consistent across every duration.

These patterns may reflect differences in patient complexity and healthcare utilization rather than direct