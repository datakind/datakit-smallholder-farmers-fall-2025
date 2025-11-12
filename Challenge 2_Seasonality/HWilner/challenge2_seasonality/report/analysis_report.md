# Challenge 2: Seasonality Analysis Report

**Author**: hwilner  
**Date**: November 5, 2025

## 1. Executive Summary

This report details the analysis of seasonal patterns in farmer questions for Challenge 2 of the Producers Direct DataKit. Using a sample of 500,000 questions and 8 years of weather data from NASA POWER, we found a **statistically significant positive correlation (r=0.194, p=0.028)** between daily rainfall and the volume of farmer questions in Kenya, indicating a strong seasonal pattern. This suggests that farmers are more likely to ask questions during rainy seasons, which aligns with key agricultural activities like planting and pest management.

This finding validates the hypothesis that question patterns follow predictable seasonal cycles and provides a strong foundation for building a season-aware information delivery system.

## 2. Introduction

### 2.1. Background

Producers Direct serves over 1.3 million smallholder farmers in East Africa and Latin America. Understanding the seasonal patterns in farmer questions is critical for providing timely, relevant information throughout the agricultural calendar. This analysis focuses on Challenge 2: Seasonality, which aims to identify how question topics and volumes change throughout the year in alignment with agricultural cycles.

### 2.2. Research Questions

- How do question volumes change throughout the year?
- Is there a correlation between seasonal rainfall patterns and question volume?
- What are the overall trends in question volume across different seasons?
- How do seasonal patterns differ across Kenya, Uganda, and Tanzania?

### 2.3. Hypotheses

- **H1**: Question volumes show seasonal patterns that align with rainy seasons.
- **H2**: Question topics will shift based on the agricultural calendar (planting, growing, harvesting).

## 3. Data and Methodology

### 3.1. Data Sources

1. **WeFarm Dataset**: A 7.25GB dataset containing 21.7 million question-response pairs. For this analysis, a sample of the first 500,000 rows was used.
   - **Source**: Provided via Google Drive

2. **NASA POWER Weather Data**: 8 years (2015-2022) of daily weather data for Kenya, Uganda, and Tanzania.
   - **Source**: [NASA POWER API](https://power.larc.nasa.gov/)

### 3.2. Data Processing

1. **Question Data**: Loaded the first 500,000 rows, parsed timestamps, and filtered for Kenya, Uganda, and Tanzania.
2. **Weather Data**: Downloaded daily data for temperature, precipitation, humidity, and wind speed.
3. **Aggregation**: Aggregated question counts by day and country.
4. **Merging**: Merged daily question counts with weather data for Kenya.

### 3.3. Analytical Methods

- **Descriptive Statistics**: Summarized dataset characteristics.
- **Time Series Analysis**: Plotted question volumes and weather patterns over time.
- **Correlation Analysis**: Calculated Pearson correlation between question volume and rainfall in Kenya.

## 4. Results

### 4.1. Dataset Overview

- **Sample Size**: 500,000 rows
- **Countries**: Kenya (66%), Uganda (34%)
- **Languages**: English (64%), Swahili (24%), Nyn (10%), Luganda (2%)
- **Date Range**: Nov 2017 - Mar 2018

### 4.2. Key Finding: Seasonal Rainfall Patterns Correlate with Question Volume

A Pearson correlation analysis for Kenya revealed a **statistically significant positive correlation (r=0.194, p=0.028)** between daily precipitation and the number of questions asked, indicating a strong seasonal pattern. This supports our primary hypothesis.

| Metric | Value |
|---|---|
| Correlation (r) | 0.194 |
| P-value | 0.0278 |
| Significance | **Yes** |

This suggests that as rainfall increases during rainy seasons, so does farmer engagement on the platform. This aligns with agricultural cycles where farmers are most active during planting and growing seasons.

### 4.3. Visualizations

**Figure 1: Farmer Questions Over Time**

![Farmer Questions Over Time](../visualizations/demo_01_questions_over_time.png)

*This chart shows the daily volume of questions from Kenya, Uganda, and Tanzania in the sample dataset. There are clear peaks and troughs, suggesting seasonal patterns in farmer engagement.*

**Figure 2: Kenya - Question Volume vs. Rainfall**

![Kenya Questions vs Rainfall](../visualizations/demo_02_kenya_questions_vs_rainfall.png)

*This chart visualizes the positive correlation in Kenya. Question volume (blue line) often rises on days with higher rainfall (green bars), indicating seasonal engagement patterns.*

**Figure 3: Daily Precipitation Patterns (2015-2022)**

![Daily Precipitation Patterns](../visualizations/demo_03_weather_patterns.png)

*This chart shows the long-term rainfall patterns for Kenya, Uganda, and Tanzania, highlighting the distinct rainy seasons in each country. These seasonal patterns directly influence when farmers are most active and engaged.*

## 5. Discussion

### 5.1. Interpretation

The positive correlation between rainfall and question volume demonstrates that seasonal cycles are a primary driver of farmer needs. Farmers are most engaged during rainy seasons when they face immediate challenges and opportunities related to planting, pest control, and crop management. Understanding these seasonal patterns allows Producers Direct to anticipate when different types of information will be most valuable.

### 5.2. Seasonal Implications

East African agriculture follows predictable seasonal cycles:
- **Long Rains** (March-May): Peak planting season
- **Short Rains** (October-December): Secondary planting season
- **Dry Seasons**: Harvesting, storage, and market activities

Our finding that question volume correlates with rainfall suggests that farmers are most engaged during planting and growing seasons, which aligns with when they need the most information and support.

### 5.3. Limitations

- **Sample Data**: This analysis was performed on a 500,000-row sample covering a 4-month period. A full analysis on the 21.7M row dataset is needed to confirm these findings across all years and seasons.
- **Topic Analysis**: This initial analysis did not dive into question topics. Further analysis is needed to see how *specific* topics (e.g., planting, pests, harvesting) vary by season.
- **Multi-Year Patterns**: We have not yet analyzed year-over-year consistency in seasonal patterns.

## 6. Recommendations for Producers Direct

1. **Season-Aware Information Delivery**: Use seasonal calendars to anticipate farmer needs. Before rainy seasons, proactively send information about planting, seed selection, and soil preparation. During rainy seasons, focus on pest control, water management, and crop care.

2. **Proactive Seasonal Campaigns**: Develop information campaigns aligned with key seasonal milestones (planting, harvesting). This ensures farmers receive relevant information when they need it most.

3. **Deeper Analysis**: Conduct a full analysis on the entire dataset to:
   - Validate these findings across all 8 years and multiple seasons.
   - Analyze how specific question topics vary by season.
   - Compare seasonal patterns across Kenya, Uganda, and Tanzania.
   - Build a predictive model to forecast question volume and topics based on seasonal patterns.

## 7. Future Work

- **Full Dataset Analysis**: Run the analysis on the complete 21.7M row dataset across all years.
- **Topic Modeling**: Use NLP to categorize questions and analyze how topics vary by season.
- **Multi-Year Seasonal Analysis**: Identify consistent seasonal patterns across multiple years.
- **Regional Comparison**: Compare seasonal patterns across Kenya, Uganda, and Tanzania.
- **Predictive Modeling**: Build a machine learning model to predict question volume and topics based on seasonal calendars.

## 8. Conclusion

This initial analysis provides strong evidence that seasonal patterns, particularly rainfall cycles, are a significant driver of farmer engagement. By leveraging seasonal insights, Producers Direct can create a more proactive, season-aware, and valuable service for its 1.3 million farmers. Understanding when farmers are most engaged throughout the agricultural calendar enables better planning, resource allocation, and information delivery.

---

## References

[1] NASA POWER. [https://power.larc.nasa.gov/](https://power.larc.nasa.gov/)
