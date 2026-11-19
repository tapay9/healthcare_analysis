
import streamlit as st
import pandas as pd
import altair as alt


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Healthcare Readmission Analytics",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 Healthcare Readmission Analytics")

st.write(
    "Exploring hospital readmission patterns "
    "using Python, SQL, and machine learning."
)


# ==================================================
# LOAD DATA
# ==================================================

@st.cache_data
def load_data():
    return pd.read_csv(
        "data/processed/diabetes_cleaned.csv"
    )


df = load_data()


# ==================================================
# HELPER FUNCTIONS
# ==================================================

def categorize_inpatient_visits(visits):
    if visits == 0:
        return "0"
    elif visits == 1:
        return "1"
    elif visits == 2:
        return "2"
    elif visits <= 4:
        return "3-4"
    else:
        return "5+"


def categorize_medications(count):
    if count <= 5:
        return "0-5"
    elif count <= 10:
        return "6-10"
    elif count <= 15:
        return "11-15"
    elif count <= 20:
        return "16-20"
    else:
        return "21+"


# ==================================================
# SIDEBAR FILTERS
# ==================================================

st.sidebar.header("Dashboard Filters")

age_options = sorted(
    df["age"].dropna().unique()
)

selected_ages = st.sidebar.multiselect(
    "Select Age Groups",
    options=age_options,
    default=age_options
)

filtered_df = df[
    df["age"].isin(selected_ages)
].copy()

st.sidebar.caption(
    "Age filters update the overview metrics and exploratory charts. "
    "Key findings and model evaluation always describe the full dataset."
)


# ==================================================
# DASHBOARD TABS
# ==================================================

overview_tab, model_tab = st.tabs([
    "📊 Hospital Overview",
    "🤖 Model Performance"
])


# ==================================================
# TAB 1: HOSPITAL OVERVIEW
# ==================================================

with overview_tab:

    st.subheader("Hospital Readmission Overview")

    # ----------------------------------------------
    # SUMMARY METRICS
    # ----------------------------------------------

    filtered_encounters = len(filtered_df)

    filtered_rate = (
        filtered_df["readmitted_30_days"].mean() * 100
        if filtered_encounters else None
    )

    filtered_patients = filtered_df["patient_nbr"].nunique()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Encounters",
            f"{filtered_encounters:,}"
        )

    with col2:
        st.metric(
            "30-Day Readmission Rate",
            f"{filtered_rate:.2f}%"
            if filtered_rate is not None else "N/A"
        )

    with col3:
        st.metric(
            "Unique Patients",
            f"{filtered_patients:,}"
        )

    st.caption(
        "Data context: UCI Diabetes 130-US Hospitals dataset (1999–2008). "
        f"The full dataset contains {len(df):,} hospital encounters involving "
        f"{df['patient_nbr'].nunique():,} unique patients. "
        "The metrics above reflect the selected age groups, "
        "and readmission rates are calculated per encounter."
    )

    st.divider()

    st.caption(
        f"Showing {len(filtered_df):,} encounters "
        "in the interactive charts."
    )

    if filtered_df.empty:
        st.warning(
            "No age groups are selected. "
            "Choose at least one age group in the sidebar."
        )

    else:

        # ------------------------------------------
        # FIRST ROW: AGE AND INPATIENT VISITS
        # ------------------------------------------

        chart_col1, chart_col2 = st.columns(
            2,
            gap="large"
        )

        with chart_col1:

            st.subheader(
                "Readmission Rate by Age Group"
            )

            age_readmission = (
                filtered_df.groupby("age")[
                    "readmitted_30_days"
                ]
                .mean()
                .mul(100)
                .reset_index()
            )

            age_readmission.columns = [
                "Age Group",
                "Readmission Rate (%)"
            ]

            st.bar_chart(
                age_readmission,
                x="Age Group",
                y="Readmission Rate (%)"
            )

            st.caption(
                "Compare readmission rates across selected age groups. "
                "Smaller groups can have less stable rates."
            )

        with chart_col2:

            st.subheader(
                "Readmission Rate by Inpatient Visits"
            )

            inpatient_df = filtered_df.copy()

            inpatient_df["Inpatient Visit Group"] = (
                inpatient_df["number_inpatient"]
                .apply(categorize_inpatient_visits)
            )

            inpatient_readmission = (
                inpatient_df.groupby(
                    "Inpatient Visit Group"
                )["readmitted_30_days"]
                .mean()
                .mul(100)
                .reindex([
                    "0",
                    "1",
                    "2",
                    "3-4",
                    "5+"
                ])
                .reset_index()
            )

            inpatient_readmission.columns = [
                "Previous Inpatient Visits",
                "Readmission Rate (%)"
            ]

            inpatient_chart = (
                alt.Chart(inpatient_readmission)
                .mark_bar(color="#79B9E8")
                .encode(
                    x=alt.X(
                        "Previous Inpatient Visits:N",
                        sort=[
                            "0", "1", "2", "3-4", "5+"
                        ],
                        title="Previous Inpatient Visits"
                    ),
                    y=alt.Y(
                        "Readmission Rate (%):Q",
                        title="Readmission Rate (%)"
                    ),
                    tooltip=[
                        "Previous Inpatient Visits",
                        alt.Tooltip(
                            "Readmission Rate (%):Q",
                            format=".2f"
                        )
                    ]
                )
                .properties(height=350)
            )

            st.altair_chart(
                inpatient_chart,
                width="stretch"
            )

            st.caption(
                "Previous inpatient visits show an association "
                "with readmission. These comparisons are descriptive, "
                "not causal."
            )

        # ------------------------------------------
        # SECOND ROW: STAY AND MEDICATION COUNT
        # ------------------------------------------

        chart_col3, chart_col4 = st.columns(
            2,
            gap="large"
        )

        with chart_col3:

            st.subheader(
                "Readmission Rate by Hospital Stay"
            )

            stay_readmission = (
                filtered_df.groupby(
                    "time_in_hospital"
                )["readmitted_30_days"]
                .mean()
                .mul(100)
                .reset_index()
            )

            stay_readmission.columns = [
                "Days in Hospital",
                "Readmission Rate (%)"
            ]

            stay_chart = (
                alt.Chart(stay_readmission)
                .mark_line(
                    point=True,
                    color="#79B9E8"
                )
                .encode(
                    x=alt.X(
                        "Days in Hospital:Q",
                        title="Days in Hospital"
                    ),
                    y=alt.Y(
                        "Readmission Rate (%):Q",
                        title="Readmission Rate (%)",
                        scale=alt.Scale(zero=False)
                    ),
                    tooltip=[
                        "Days in Hospital",
                        alt.Tooltip(
                            "Readmission Rate (%):Q",
                            format=".2f"
                        )
                    ]
                )
                .properties(height=350)
            )

            st.altair_chart(
                stay_chart,
                width="stretch"
            )

            st.caption(
                "Readmission rates vary by length of stay. "
                "The relationship is not consistently increasing."
            )

        with chart_col4:

            st.subheader(
                "Readmission Rate by Medication Count"
            )

            medication_df = filtered_df.copy()

            medication_df["Medication Group"] = (
                medication_df["num_medications"]
                .apply(categorize_medications)
            )

            medication_readmission = (
                medication_df.groupby(
                    "Medication Group"
                )["readmitted_30_days"]
                .mean()
                .mul(100)
                .reindex([
                    "0-5",
                    "6-10",
                    "11-15",
                    "16-20",
                    "21+"
                ])
                .reset_index()
            )

            medication_readmission.columns = [
                "Medication Count",
                "Readmission Rate (%)"
            ]

            medication_chart = (
                alt.Chart(medication_readmission)
                .mark_bar(color="#79B9E8")
                .encode(
                    x=alt.X(
                        "Medication Count:N",
                        sort=[
                            "0-5",
                            "6-10",
                            "11-15",
                            "16-20",
                            "21+"
                        ],
                        title="Medication Count"
                    ),
                    y=alt.Y(
                        "Readmission Rate (%):Q",
                        title="Readmission Rate (%)"
                    ),
                    tooltip=[
                        "Medication Count",
                        alt.Tooltip(
                            "Readmission Rate (%):Q",
                            format=".2f"
                        )
                    ]
                )
                .properties(height=350)
            )

            st.altair_chart(
                medication_chart,
                width="stretch"
            )

            st.caption(
                "Medication counts may reflect patient complexity. "
                "The chart does not establish that medications "
                "cause readmissions."
            )

    # ----------------------------------------------
    # KEY ANALYTICAL FINDINGS
    # ----------------------------------------------

    st.divider()

    st.subheader("Key Analytical Findings")

    finding_col1, finding_col2, finding_col3 = (
        st.columns(3)
    )

    with finding_col1:

        st.metric(
            "Overall Readmission Rate",
            "11.16%"
        )

        st.write(
            "Approximately 11 out of every 100 "
            "hospital encounters resulted in "
            "readmission within 30 days."
        )

    with finding_col2:

        st.metric(
            "5+ Previous Inpatient Visits",
            "36.41%"
        )

        st.write(
            "Encounters involving patients with five "
            "or more previous inpatient visits had "
            "substantially higher readmission rates."
        )

    with finding_col3:

        st.metric(
            "Highest Age-Group Rate",
            "14.24%"
        )

        st.write(
            "The 20–30 age group had the highest "
            "observed readmission rate in the "
            "overall dataset."
        )

    st.caption(
        "Key findings represent the complete dataset "
        "and do not change with age filters."
    )

    st.info(
        "Key Insight: Previous inpatient visits "
        "showed a strong association with 30-day "
        "hospital readmissions."
    )


# ==================================================
# TAB 2: MODEL PERFORMANCE
# ==================================================

with model_tab:

    st.header("Machine Learning Performance")

    st.write(
        "Logistic Regression models were evaluated "
        "to predict whether a hospital encounter "
        "would result in readmission within 30 days. "
        "The results below are based on a held-out "
        "test dataset."
    )

    # ----------------------------------------------
    # BALANCED MODEL PERFORMANCE
    # ----------------------------------------------

    st.subheader("Balanced Logistic Regression")

    ml_col1, ml_col2, ml_col3, ml_col4 = (
        st.columns(4)
    )

    with ml_col1:
        st.metric(
            "Accuracy",
            "67.43%"
        )

    with ml_col2:
        st.metric(
            "Precision",
            "15.73%"
        )

    with ml_col3:
        st.metric(
            "Recall",
            "47.09%"
        )

    with ml_col4:
        st.metric(
            "ROC-AUC",
            "0.6281"
        )

    st.caption(
        "Balanced Logistic Regression was trained "
        "using class weighting to give greater "
        "importance to the less frequent "
        "30-day readmission outcome."
    )

    st.divider()

    # ----------------------------------------------
    # MODEL RETRAINING AND COMPARISON
    # ----------------------------------------------

    st.subheader("Why I Retrained the Model")

    st.write(
        "I initially trained a standard Logistic Regression model "
        "to predict 30-day readmissions. Although it achieved "
        "89.33% accuracy, its recall was only 0.88%, meaning "
        "it missed nearly all actual readmissions."
    )

    st.write(
        "To address this class-imbalance problem, I trained "
        "a second Logistic Regression model using balanced "
        "class weights. This increased recall to 47.09%, "
        "but reduced precision and accuracy. Both models "
        "were evaluated on the same held-out test set "
        "of 20,153 hospital encounters."
    )

    st.subheader("Model Comparison")

    comparison_df = pd.DataFrame({
        "Metric": [
            "Accuracy",
            "Precision",
            "Recall",
            "F1-score",
            "ROC-AUC"
        ],
        "Original Logistic Regression": [
            "89.33%",
            "50.00%",
            "0.88%",
            "0.0174",
            "0.6278"
        ],
        "Balanced Logistic Regression": [
            "67.43%",
            "15.73%",
            "47.09%",
            "0.2359",
            "0.6281"
        ]
    })

    st.dataframe(
        comparison_df,
        hide_index=True,
        width="stretch"
    )

    st.caption(
        "Both models were evaluated on the same "
        "patient-separated, held-out test set. "
        "Results are rounded from the modeling notebook."
    )

    st.info(
        "Modeling Takeaway: Retraining with balanced "
        "class weights substantially improved recall "
        "and the F1-score. However, the balanced model "
        "still generated many false positives and "
        "is not suitable for clinical use."
    )

    st.divider()

    # ----------------------------------------------
    # CONFUSION MATRIX
    # ----------------------------------------------

    st.subheader("Confusion Matrix")

    st.write(
        "The confusion matrix shows how the balanced "
        "model classified the 20,153 hospital encounters "
        "in the held-out test dataset."
    )

    confusion_df = pd.DataFrame({
        "Actual": [
            "No Readmission",
            "No Readmission",
            "Readmission",
            "Readmission"
        ],
        "Predicted": [
            "No Readmission",
            "Readmission",
            "No Readmission",
            "Readmission"
        ],
        "Count": [
            12576,
            5426,
            1138,
            1013
        ],
        "Outcome": [
            "True Negative",
            "False Positive",
            "False Negative",
            "True Positive"
        ]
    })

    confusion_chart = (
        alt.Chart(confusion_df)
        .mark_rect()
        .encode(
            x=alt.X(
                "Predicted:N",
                sort=[
                    "No Readmission",
                    "Readmission"
                ],
                title="Predicted Outcome"
            ),
            y=alt.Y(
                "Actual:N",
                sort=[
                    "No Readmission",
                    "Readmission"
                ],
                title="Actual Outcome"
            ),
            color=alt.Color(
                "Count:Q",
                scale=alt.Scale(
                    scheme="blues"
                ),
                legend=None
            ),
            tooltip=[
                "Actual",
                "Predicted",
                "Outcome",
                alt.Tooltip(
                    "Count:Q",
                    format=","
                )
            ]
        )
        .properties(height=320)
    )

    confusion_labels = (
        alt.Chart(confusion_df)
        .mark_text(
            fontSize=20,
            fontWeight="bold"
        )
        .encode(
            x=alt.X(
                "Predicted:N",
                sort=[
                    "No Readmission",
                    "Readmission"
                ]
            ),
            y=alt.Y(
                "Actual:N",
                sort=[
                    "No Readmission",
                    "Readmission"
                ]
            ),
            text=alt.Text(
                "Count:Q",
                format=","
            ),
            color=alt.condition(
                alt.datum.Count > 6000,
                alt.value("white"),
                alt.value("black")
            )
        )
    )

    st.altair_chart(
        confusion_chart + confusion_labels,
        width="stretch"
    )

    st.caption(
        "Rows represent actual outcomes and columns "
        "represent predicted outcomes."
    )

    outcome_col1, outcome_col2 = st.columns(2)

    with outcome_col1:

        st.metric(
            "True Positives",
            "1,013"
        )

        st.caption(
            "Actual readmissions correctly identified."
        )

        st.metric(
            "False Negatives",
            "1,138"
        )

        st.caption(
            "Actual readmissions the model missed."
        )

    with outcome_col2:

        st.metric(
            "True Negatives",
            "12,576"
        )

        st.caption(
            "Non-readmissions correctly identified."
        )

        st.metric(
            "False Positives",
            "5,426"
        )

        st.caption(
            "Non-readmissions incorrectly flagged."
        )

    st.divider()

    # ----------------------------------------------
    # BUSINESS INTERPRETATION
    # ----------------------------------------------

    st.subheader("What Do These Results Mean?")

    st.write(
        "The balanced model correctly identified "
        "47.09% of actual 30-day readmissions, "
        "compared with only 0.88% for the original model."
    )

    st.write(
        "However, its precision of 15.73% means "
        "that most encounters flagged as potential "
        "readmissions were false positives."
    )

    st.write(
        "This demonstrates an important tradeoff: "
        "improving the detection of readmissions "
        "can increase the number of false alarms."
    )

    st.info(
        "Analytical Takeaway: Class weighting improved "
        "the model's ability to identify readmissions, "
        "but the substantial false-positive burden "
        "limits its practical usefulness. "
        "Further model development and validation "
        "would be needed before operational use."
    )

    # ----------------------------------------------
    # MODEL INTERPRETATION
    # ----------------------------------------------

    st.subheader("Model Interpretation")

    st.write(
        "Previous inpatient visits showed a positive "
        "association with predicted readmission odds, "
        "consistent with the exploratory analysis. "
        "This association does not establish causation."
    )

    # ----------------------------------------------
    # MODEL LIMITATIONS
    # ----------------------------------------------

    st.subheader("Model Limitations")

    st.warning(
        "The dataset is historical (1999–2008), "
        "and the outcome is imbalanced. "
        "The balanced model has modest discriminative "
        "performance, produces many false positives, "
        "and misses some actual readmissions. "
        "It has not been externally or clinically "
        "validated and should not be used for "
        "clinical decision-making."
    )


# ==================================================
# SQL & DATA ANALYSIS METHODOLOGY
# ==================================================

st.divider()

st.subheader("SQL & Data Analysis Methodology")

st.markdown("""
SQL was used to investigate hospital readmission patterns across
101,766 hospital encounters.

The analysis includes:

- Overall 30-day readmission rates
- Readmission patterns across age groups
- Previous inpatient utilization
- Hospital length of stay and medication counts
- Combined utilization and demographic analyses

Seven SQL queries are documented in the GitHub repository.

[View SQL Analysis on GitHub](https://github.com/tapay9/healthcare_analysis/tree/healthcare-analysis-upgrade/sql)
""")


# ==================================================
# DASHBOARD FOOTER
# ==================================================

st.caption(
    "Data: UCI Diabetes 130-US Hospitals Dataset "
    "(1999–2008). Findings describe historical "
    "associations and do not establish causation."
)
