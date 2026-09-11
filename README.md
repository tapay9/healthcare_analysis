# Healthcare Readmission Analysis

## Project Overview

This project analyzes a synthetic healthcare dataset to explore factors related to patient health, hospital utilization, healthcare costs, and 30-day hospital readmissions.

The project demonstrates an end-to-end data analytics workflow using Python, including data cleaning, exploratory data analysis (EDA), data visualization, correlation analysis, feature engineering, and predictive modeling.

## Tools & Technologies

- Python
- Pandas
- NumPy
- Matplotlib
- Scikit-learn
- Jupyter Notebook
- Git & GitHub

## Project Workflow

### Data Cleaning
- Inspected the dataset for missing values and incorrect data types
- Standardized inconsistent categorical values
- Removed duplicate records
- Corrected formatting inconsistencies
- Converted columns to appropriate data types
- Created a cleaned dataset for analysis

### Exploratory Data Analysis
- Analyzed patient age and gender distributions
- Examined smoking status distribution
- Compared average cholesterol levels by smoking status
- Analyzed diabetes in relation to 30-day readmissions
- Examined the relationship between length of stay and hospital cost

### Correlation Analysis
- Created a correlation matrix for numerical variables
- Visualized correlations using a heatmap
- Identified strong relationships among several patient and hospital variables

### Feature Engineering
Created additional features to support analysis and predictive modeling:

- Age_Group
- BMI_Category
- High_Risk

### Predictive Modeling

A Logistic Regression model was developed to predict whether a patient would be readmitted within 30 days.

The dataset was divided into training and testing sets, and the model was evaluated using multiple classification metrics.

## Model Performance

- Accuracy: 1.00
- Precision: 1.00
- Recall: 1.00
- F1 Score: 1.00

The model correctly classified all observations in the test set. However, these results should be interpreted cautiously because the dataset is synthetic and contains only 50 observations. The small sample size and strong relationships built into the synthetic data may make the prediction task easier than it would be with real-world healthcare data.

## Key Findings

- Current smokers had higher average cholesterol levels than former and never smokers in the dataset.
- Patients with diabetes showed higher 30-day readmission rates.
- Weight and BMI had a strong positive correlation.
- Age showed strong positive relationships with medication count, hospital visits, length of stay, and total hospital cost.
- Feature engineering provided additional patient characteristics that could support further analysis and modeling.

## Recommendations

- Provide additional follow-up and monitoring for patients with chronic conditions such as diabetes and hypertension.
- Consider additional discharge planning for patients with multiple risk factors.
- Monitor factors associated with longer hospital stays and increased healthcare costs.
- Use larger and more diverse datasets for future predictive modeling.

## Limitations

This project uses a small synthetic dataset of 50 patients. Therefore, the findings and model performance should not be generalized to real-world patient populations. The predictive model is intended to demonstrate the machine learning workflow rather than provide a clinically deployable prediction system.

## Future Improvements

- Analyze a larger healthcare dataset
- Compare Logistic Regression with additional classification models
- Perform additional feature selection and engineering
- Use cross-validation for more reliable model evaluation
- Explore additional visualizations and healthcare risk factors

## Project Status

✅ Data Cleaning  
✅ Exploratory Data Analysis  
✅ Data Visualization  
✅ Correlation Analysis  
✅ Feature Engineering  
✅ Predictive Modeling  
✅ Model Evaluation  
✅ Key Findings & Recommendations  

**Project Complete**
