# Allison Sibrian - Challenge 1 Analysis

## Overview
 This project analyzes whether weather patterns can predict the types of questions farmers ask. By translating farmer SMS messages from local languages (Swahili, Luganda, and Runyankole) and combining them with ERA5 weather data, I built a model to predict spikes in farmer inquiries.

Note: Due to the massive dataset size (21M rows), this analysis was conducted on a stratified 0.5% sample.

## Research Questions
- Question 1: Do specific weather events trigger predictable spikes in farmer questions?
- Question 2: Is there a temporal lag between the weather event and the farmer's question (e.g., biological pest lifecycles)?
- Question 3: Can machine learning models predict the volume of farmers' questions based solely on country-level weather data?

## Methodology

### Data Sources
- Producers Direct Dataset: Obtained de-duplicated farmer questions split by language (English, Swahili, Luganda, Runyankole).
- ERA5 Climate Reanalysis Data: Monthly aggregates for Total Precipitation (prcp), Maximum Temperature (tasmax), and Minimum Temperature (tasmin) for Kenya, Uganda, and Tanzania.
- Global Historical Climatology Network daily (GHCNd): Ground station data (GHCNd) was explored during the initial phase but excluded from the final analysis. EDA revealed that weather stations for the countries would stop recording data. To ensure consistent and reliable data I opted to use ERA5 data in my analysis.

### Approach
1. **Step 1**: Data processing, loading, and initial exploration
2. **Step 2**: Stratified Sampling and Translation 
3. **Step 3**: Cleaning and Topic Categorization
4. **Step 4**: Aggregation & Feature Engineering
5. **Step 5**: Visualizations and Predictive Modeling

### Tools and Technologies
- **Programming Language**: Python 3.11
- **Key Libraries**: pandas, numpy, duckdb, matplotlib, seaborn, nltk, scikit-learn, etc. 

## Use of Generative AI

### Tools Used
- **Gemini (Google's AI model).**: Used to preprocess the 21M row raw dataset, ghcnd_all.tar.gzfile, handle the stratified sampling logic in Google Colab, and perform batch translation of local languages. Also utilized to refine the Random Forest TimeSeriesSplit validation strategy.
- **Human-Created**: All analysis logic, interpretation of visualizations, validation, and final strategic conclusions.

## Key Findings

### Lagged Rainfall (1 Month) is One of the Leading Predictors for 'Pest & Disease' Questions 
The model identified 1-Month Lagged Rainfall as significantly more predictive than current rainfall. As current rain triggers vegetation growth, farmer's tend to notice pests afterwards.

**Implications for Producers Direct:**
- To create a pest alert system following this analysis, it would be best to send alerts 3-4 weeks after heavy rainfall events.
- To improve on this pest and disease alert system, this model can be refined to use weekly aggregations, and intake more data if there are no computational constraints for analysis.

### Strong Predictive Success for 'Pests & Disease' and 'Market' Topics
The model for "Pests & Disease" questions achieved a positive R^2 score (0.18) and a "Strong" performance rating, meaning that test RMSE was lower than the standard deviation of the test set

'Pest & Disease' RMSE: 18.90
'Market' RMSE: 22.31

**Implications for Producers Direct:**
- There is a strong confidence in using the model for predicting these topics, and this model can be used to further refine this model by incorporating weekly aggregation and regional data, which can eventually used for future automated systems.
-  Livestock and Crop questions showed higher variance, suggesting they are driven by other factors.

## Visualizations

###  
http://localhost:8888/lab/tree/Challenge%201%20_Weather%20Patterns/allisonsibrian/ug_weather_topic_trends.png

**Interpretation**: 
Although hard to tell, both big and smaller peaks for 'Pests & Disease' questions tend to occur when there is a high rainfall the month before in Uganda.

### Feature Importance for 'Pests & Disease' Questions
http://localhost:8888/lab/tree/Challenge%201%20_Weather%20Patterns/allisonsibrian/feature_importances.png

**Interpretation**: 
This chart shows the model's validation and prediction logic 
- Year and Month set the baseline volume, meaning that the primary drivers are users using the platform and the seasonal farming calendar.
- 1-Month Lagged Rainfall and 1-Month Lagged Heat follow showing that vegetation growth and heat creates an incubation period for pests, which could sit at ~ 1 month or less. 

## Limitations and Challenges

### Data Limitations
- Weather and Questions were averaged at the country level. Averaging to country level leaves out of micro-climates, and limits the model's ability to predict the exact volume of topic question count.
- Training on aggregated monthly data points limited the model's ability to learn non-linear patterns.

### Technical Challenges
- Translating 21.5 million rows was not possible due to computational constraints. I used a 0.5% sampling strategy per language group as it was a necessary trade-off between translation quality and processing time.
- Some translations resulted in hallucinations (e.g., "Attorney General"). This required implementing keyword filtering to obtain usable data. 

## Next Steps and Recommendations

### For Further Analysis
1. To expand and create a robust pest and disease alert system, it would be best to move from monthly to weekly aggregation. A weekly model would likely increase the R^2 score significantly.
2. To expand this analysis, incorporating user location would allow for better forecasting as this country-level analysis is masking micro-climates that occur in a country.
3. Splitting and further specifying topic questions would help (i.e., 'Crops') as different crops have different weather sensitivities.

### For Producers Direct
Utilizing the prediction model to create a robust alert or high-risk month or market campaigns can be done by specifying feature attributes and incorporating seasonal farming calendars as Month was a big predictor in predicting 'Pest & Disease' questions. 

I recommend incorporating regional data in the model, aggregating at a weekly-level and specifying questions to create a stronger model.

## Contact and Collaboration

**Author**: Allison Sibrian
**GitHub**: @allisonsibrian

**Collaboration Welcome**: 
- Open to feedback and suggestions
- Happy to collaborate on related analyses
- Available to answer questions about this approach

## Acknowledgments
- Thanks to Bashir Alsuty for the de-duplicated data split by language files, and Steven Yan for the Comet Scores on translation models for Swahili, Luganda, and Runyankole, as they were used in my pre-processing stage.
---

**Last Updated**: November 28th, 2025
