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

| AQI Level | Category   
| 1         | Good
| 2         | Fair 
| 3         | Moderate 
| 5         | Very Poor

---

# Machine Learning Methodology
- **Model:** LightGBM Classifier  
- **Task:** Multi-class AQI classification  
- **Data Strategy:** Class imbalance mitigation using Synthetic Minority Over-sampling Technique (SMOTE)  

The model was trained on historical air quality data collected from Pakistan. SMOTE was applied to improve predictive performance for underrepresented AQI categories and ensure balanced classification behavior.


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

