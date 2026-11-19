-- Query 6: Combined Inpatient History and Hospital Stay Analysis

WITH patient_groups AS (
    SELECT
        CASE
            WHEN number_inpatient = 0 THEN '0 visits'
            WHEN number_inpatient BETWEEN 1 AND 2 THEN '1-2 visits'
            ELSE '3+ visits'
        END AS inpatient_history,

        CASE
            WHEN time_in_hospital <= 3 THEN '1-3 days'
            WHEN time_in_hospital <= 7 THEN '4-7 days'
            ELSE '8-14 days'
        END AS stay_length,

        readmitted_30_days
    FROM hospital_analysis
)

SELECT
    inpatient_history,
    stay_length,
    COUNT(*) AS total_encounters,
    SUM(readmitted_30_days) AS total_readmissions,
    ROUND(
        AVG(readmitted_30_days) * 100,
        2
    ) AS readmission_rate_percent
FROM patient_groups
GROUP BY inpatient_history, stay_length
ORDER BY
    CASE inpatient_history
        WHEN '0 visits' THEN 1
        WHEN '1-2 visits' THEN 2
        ELSE 3
    END,
    CASE stay_length
        WHEN '1-3 days' THEN 1
        WHEN '4-7 days' THEN 2
        ELSE 3
    END;