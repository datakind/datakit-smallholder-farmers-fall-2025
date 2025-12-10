# Clustering of 2.7 Million Farmer Queries and Analysing 73 years of Ugandan Weather Patterns

### Uncovering Agricultural Trends in East Africa using NLP & Unsupervised Learning

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Scikit-Learn](https://img.shields.io/badge/Library-Scikit--Learn-orange)
![Plotly](https://img.shields.io/badge/Library-Plotly-green)

## Project Overview
This project analyses a massive dataset of **11 million farmer queries** from Producers Direct to understand the critical challenges faced by smallholder farmers in Kenya, Uganda, and Tanzania.

By filtering for the **2.7 million English-language queries**, this analysis uses Unsupervised Machine Learning to categorise unstructured text into actionable topics. The goal was to move beyond simple keyword counting to discover semantic themes and map them against seasonal, and geographical climate trends. 

The project further cross-references these linguistic trends with **historical climate data (1950–2023)** from the Climate Change Knowledge Portal to validate how rainfall variability impacts farming behavior.

**Key Challenge:** The dataset size required memory-efficient streaming techniques (MiniBatch K-Means) to process millions of rows on local hardware.

---

## Methodology & Technical Architecture

### 1. Data Standardisation & Preparation 
* **Strategic Subsetting for NLP:** Initiated the analysis by isolating **2.7 million unique English queries** from the 11M-row multilingual compilation. This action ensured a semantically consistent body, critical for successful topic modeling.
* **Time-Series Robustness:** Developed and implemented a robust parsing solution for the timestamp data, handling noisy, microsecond-level ISO8601 formats. This standardisation directly enabled the seasonal trend analysis.
* **Geographic Data Cleaning:** Explicitly noted the dominance of English queries from Kenya and Uganda, framing the absence of Tanzanian English data as a crucial geolinguistic finding.

### 2. Feature Extraction 
* **Algorithm:** `HashingVectorizer` (Scikit-Learn) with Character N-grams (`3, 5`).
* **Impact:** Created a robust feature set that automatically clusters misspelled words (e.g., "maize", "maiz") together, effectively handling dirty user-generated text.

### 3. Clustering (Streaming Approach)
* **Algorithm:** `MiniBatchKMeans` (K=50 clusters).
* **Strategy:** **Partial Fit** (incremental learning) on batches of 10,000 rows to overcome RAM limitations.
* **Interpretation:** Manually mapped cluster centroids to meaningful labels (e.g., Cluster 12 → "Disease Control") to create a verified, actionable taxonomy.

### 4. Visualisation
* **Dimensionality Reduction:** `TruncatedSVD` (Latent Semantic Analysis) reduced the feature space to 2D for plotting.
* **Tools:** `Matplotlib` for static plots and `Plotly` for interactive, hover-based topic exploration.
  
---

## Key Findings

### 1. Climate Vulnerability & Topic Synergy
This analysis cross-referenced farmer queries with rainfall/temperature data (1950-2023):
* **Quantified Rainfall Decline:** Climate data validated a **statistically significant decline** in rainfall during Uganda's critical March–May planting season (average reduction of **12.33 mm per decade**, Mann-Kendall $p=0.01$).
* **Flood Risk:** The analysis revealed that despite the overall decline, the onset of the rainy season is marked by short, **intense rainfall events**, increasing flood risks in mountainous areas (e.g., Mt. Elgon).
* **Warming Trend:** Uganda's mean surface air temperatures have risen from **21°C (1950s) to over 24°C (2020s)**.



### 2. Topic Dominance & Gaps
* **Staple Focus:** "Maize" (2.2M records) and "Beans" (732k records) remain the most discussed crops, indicating a prioritisation of core farming activities.
* **Reactive Health:** High volume of queries regarding specific livestock symptoms (e.g., "bleeding," "pus") highlights a need for preventative, rather than reactive, animal health advisory services.
* **Niche Gaps:** Topics like "Beekeeping" and "Passionfruit" generated low volume, suggesting specialised advisory services are needed for these complex, niche categories.
* **Livestock:** High engagement on "Cattle" and "Chicken." Notably, there is specific, high-value interest in "Kienyeji Chicken" (16k+ queries), a local breed, despite it being a niche topic.

### 3. Geographic & Linguistic Constraints
* **English Dominance:** Kenya and Uganda accounted for 99.9% of English queries. Tanzania's interaction was almost exclusively in Swahili, confirming a significant geolinguistic bias in the English subset and necessitating future multi-lingual NLP work..
* **Gender Gap:** Male farmers submitted ~113k queries compared to ~30k from female farmers, highlighting a digital gender divide.

### 4. Seasonal Behavioral Trends
* **Crop Cycle:** Crop-related queries peak between **June and September**, with the highest volume in **August**. This correlates with the end of the harvest season, where farmers pivot to inquiries about "Yield Optimisation" for the next cycle.
* **Livestock Consistency:** Unlike crops, animal health queries (disease control, medicine) remain consistent year-round, reflecting the non-seasonal nature of animal rearing.
  
## How to Run
1.  Clone the repository.
2.  Install dependencies:
    ```bash
    pip install pandas numpy scikit-learn matplotlib plotly pyarrow openpyxl
    ```
    **Challenge 4**
3.  Run the Jupyter Notebook `Question Topic.ipynb`.
4.  View the file `Cluster Summary.xlsx`

    **Challenge 1**
6.  Run the Jupyter Notebook `Weather Patterns.ipynb`
---

## Gen-AI Disclosure
* **Gemini:** Used for optimising `MiniBatchKMeans` code for large-scale datasets.
* **Copilot:** Assisted in structuring the final analytical report.
---


## Author
**Jonathan Khabusi**
*Climate Data Analyst*
