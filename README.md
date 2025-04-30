# Student Mental Health ML

A machine learning approach to predicting anxiety and depression in undergraduate students using the StudentLife dataset.

## Project Overview

This repository contains the code and analysis for predicting depression severity (PHQ-9 scores) in undergraduate students based on lifestyle, academic, and behavioral factors. Using the 2013 StudentLife longitudinal dataset, we applied various machine learning models to identify key predictors of mental health outcomes and develop actionable insights for intervention strategies.

## Key Findings

- Our XGBoost model achieved an R² of 0.896, demonstrating strong predictive power for depression scores
- Key predictors identified include GPA, self-reported sadness, openness to experience, and routine regularity
- Academic performance (GPA) was found to be the strongest protective factor against depression
- Establishing even minimal daily routines was associated with lower depression risk
- Extreme openness to experience correlated with higher predicted depression risk

## Dataset

The StudentLife dataset comprises daily records from 48 undergraduate and graduate students collected over a 10-week period. This dataset includes:

- Behavioral patterns (activity levels, sleep duration, physical exercise)
- Academic engagement (class attendance, assignment deadlines, GPA)
- Mental states (mood, stress, anxiety)
- PHQ-9 scores (depression severity)

After data cleaning and preprocessing, the final dataset included approximately 2,560 usable samples.

## Methodology

### Data Preprocessing

- Cleaned and handled missing values
- Aggregated ecological momentary assessment (EMA) variables weekly by user ID and datetime
- Forward- and backward-filled missing values within user-week blocks
- Dropped rows with over 70% missing data
- Re-encoded key EMA items into increasing ordinal scales

### Model Development

We implemented and compared several machine learning approaches:

1. **Linear Regression (Baseline)**: Simple, interpretable model to establish baseline performance
2. **Random Forest**: Ensemble method to capture non-linear relationships
3. **XGBoost (Best Performer)**: Gradient boosted trees to optimize prediction accuracy

### Model Evaluation

Models were evaluated using:
- Mean Squared Error (MSE)
- R² and Adjusted R² scores
- Learning curves
- Predicted vs. actual plots

### Explainability Analysis

We conducted extensive explainability analyses to understand model predictions:
- Feature importance rankings
- SHAP (SHapley Additive exPlanations) values
- Partial dependence plots

## Experiments

1. **Model Comparison**: Compared performance of linear regression, Random Forest, and XGBoost
2. **Model Explainability**: Identified key predictors and their relationships with depression scores
3. **Class Imbalance Sensitivity**: Evaluated model performance under different sampling strategies
4. **Noise Robustness**: Assessed model resilience to feature noise

## Results

- XGBoost achieved the lowest MSE (3.38) and highest R² (0.896)
- GPA showed the strongest protective effect, with significant reduction in predicted depression when raising GPA from ~2.4 to 2.8
- Sadness demonstrated a nearly linear relationship with depression scores
- Openness to experience showed a threshold effect at high levels
- Minimal routine was sufficient for mental health benefits, with additional structure showing diminishing returns
- XGBoost was the most robust to class imbalances and noise

## Recommendations

Based on our findings, we recommend:

1. Focusing academic coaching and support resources on students with GPAs below 2.8
2. Implementing regular mood check-ins to catch small increases in sadness before they lead to clinical depression
3. Developing low-barrier routine structures for all students, particularly those reporting chaotic daily patterns
4. Providing tailored resilience-building resources for highly "experiential" learners

## Installation

Clone this repository:
```bash
git clone https://github.com/fanxu30/student_mental_health_ml.git
cd student_mental_health_ml
```

## Contributors

- Fan Xu
- Nakiyah Dhariwala
- Jiaxin Gao
- Syed Huma Shah

## References

1. Wang, R., Chen, F., Chen, Z., Li, T., Harari, G., Tignor, S., Zhou, X., Ben-Zeev, D., & Campbell, A. T. (2014). "StudentLife: Assessing Mental Health, Academic Performance and Behavioral Trends of College Students using Smartphones." In Proceedings of the ACM Conference on Ubiquitous Computing.

2. Srividya, M., Mohanavalli, S. & Bhalaji, N. (2018). "Behavioral Modeling for Mental Health using Machine Learning Algorithms." Journal of Medical Systems, 42, 88.

3. Pfizer Inc. (2008). "Patient Health Questionnaire-9 (PHQ-9)." Retrieved from https://med.stanford.edu/fastlab/research/imapp/msrs/_jcr_content/main/accordion/accordion_content3/download_256324296/file.res/PHQ9%20id%20date%2008.03.pdf

## License

This project is licensed under the MIT License - see the LICENSE file for details.
