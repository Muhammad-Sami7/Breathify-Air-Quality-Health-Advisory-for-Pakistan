# Breathify  
AI-Powered Air Quality Monitoring and Health Advisory System for Pakistan.
Breathify is an AI-driven air quality monitoring and Air Quality Index (AQI) prediction system designed specifically for Pakistan. The application combines machine learning with real-time environmental data to assess air pollution levels and provide clear, actionable health guidance.

The system predicts standardized AQI categories and presents health advisories in both English and Urdu, supporting public awareness and informed decision-making related to environmental and health risks.

# Key Features
- Real-time air quality monitoring using external environmental APIs  
- AI-based AQI classification across standardized pollution levels  
- Trained on Pakistan-specific historical air quality data  
- Health impact guidance in English and Urdu  
- Bilingual audio output for AQI interpretation (output only)  
- Class imbalance handling using SMOTE for reliable predictions  
- High prediction stability suitable for real-time applications  

# Air Quality Index (AQI) Categories
The AQI categories used in this system are aligned with widely accepted air quality standards and are defined as follows:

| AQI Level | Category     | Health Interpretation |
|---------:|--------------|-----------------------|
| 1 | Good | Air quality is satisfactory and poses little or no health risk. |
| 2 | Fair | Air quality is acceptable; individuals with respiratory sensitivity may experience minor discomfort. |
| 3 | Moderate | Sensitive groups may experience health effects; the general population is unlikely to be affected. |
| 4 | Poor | Increased likelihood of adverse health effects for all individuals, particularly vulnerable groups. |
| 5 | Very Poor | Serious health risks may occur; prolonged or outdoor exposure should be avoided. |

---

# Machine Learning Methodology
- **Model:** LightGBM Classifier  
- **Task:** Multi-class AQI classification  
- **Data Strategy:** Class imbalance mitigation using Synthetic Minority Over-sampling Technique (SMOTE)  

The model was trained on historical air quality data collected from Pakistan. SMOTE was applied to improve predictive performance for underrepresented AQI categories and ensure balanced classification behavior.

#Class Imbalance Handling
The original dataset showed significant class imbalance across AQI categories.  
To address this, **SMOTE (Synthetic Minority Over-sampling Technique)** was applied:

- **Before SMOTE:**  
  `{5: 41555, 4: 18821, 3: 16379, 2: 8256, 1: 1182}`

- **After SMOTE:**  
  `{1: 41555, 2: 41555, 3: 41555, 4: 41555, 5: 41555}`

This improved the model’s ability to correctly predict minority AQI classes.

## Model Performance Summary
- Achieves approximately **91% validation accuracy** on unseen data  
- Demonstrates balanced performance across all AQI categories  
- Prediction errors are primarily limited to adjacent AQI levels, reflecting gradual changes in air pollution  
- High average prediction confidence, supporting real-time health advisory use cases  

Detailed evaluation metrics and visual analysis are available in the model training notebook.


## Application Functionality
- Retrieves real-time air quality data via an external API  
- Predicts AQI category using a trained machine learning model  
- Displays health guidance alongside AQI results  
- Supports bilingual output in English and Urdu  
- Audio output is supported for AQI interpretation; voice input is not supported  

