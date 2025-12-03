# Clustering of 2.7 Million Farmer Queries

### Uncovering Agricultural Trends in East Africa using NLP & Unsupervised Learning

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Scikit-Learn](https://img.shields.io/badge/Library-Scikit--Learn-orange)
![Plotly](https://img.shields.io/badge/Library-Plotly-green)

##  Project Overview
This project analyzes a massive dataset of **over 11 million farmer queries** from Producers Direct to understand the critical challenges faced by smallholder farmers in Kenya, Uganda, and Tanzania.

By filtering for the **2.7 million English-language queries**, this analysis uses **Unsupervised Machine Learning** to categorize unstructured text into actionable topics. The goal was to move beyond simple keyword counting to discover semantic themes (e.g., "Yield Optimization," "Livestock Symptoms") and map them against seasonal and geographical patterns.

**Key Challenge:** The dataset size required memory-efficient streaming techniques (MiniBatch K-Means) to process millions of rows on local hardware.

---

##  Methodology & Technical Architecture

### 1. Data Ingestion & Preprocessing
* **Volume:** Processed ~2.7 million unique English queries (Kenya: 1.56M, Uganda: 1.14M, Tanzania: negligible English input).
* **Cleaning:** Parsed complex `ISO8601` timestamps with microsecond precision to enable seasonal analysis.
* Explicitly noted the dominance of English queries from Kenya and Uganda, framing the absence of Tanzanian English data as a crucial geolinguistic finding rather than a data error.

### 2. Feature Extraction (The "Typos" Solution)
* **Algorithm:** `HashingVectorizer` (Scikit-Learn).
* **Configuration:** `analyzer='char_wb'`, N-gram range `(3, 5)`.
* **Impact:** Analyzed character sequences instead of whole words. This allowed the model to cluster misspelled terms (e.g., "maize", "maiz") together without manual correction.

### 3. Clustering (Streaming Approach)
* **Algorithm:** `MiniBatchKMeans` (K=50 clusters).
* **Strategy:** Incremental learning (Partial Fit) on batches of 10,000 rows to overcome RAM limitations.
* **Interpretation:** Manually mapped cluster centroids to meaningful labels (e.g., Cluster 12 → "Disease Control") by analyzing random samples from each group.

### 4. Visualization
* **Dimensionality Reduction:** `TruncatedSVD` (Latent Semantic Analysis) to project sparse data into 2D space.
* **Tools:** `Matplotlib` for static distribution plots and `Plotly` for interactive, hover-based topic exploration.

---

##  Key Findings

### 1. Topic Dominance & Gaps
* **Top Concerns:** "Maize" (2.2M records) and "Beans" (732k records) are the dominant crop queries.
* **Livestock Health:** High engagement regarding specific symptoms (e.g., "bleeding," "pus"), indicating a reactive approach to animal health.
* **Niche Topics:** "Beekeeping," "Passionfruit," and "Seedling Management" averaged only ~16k queries, suggesting either high baseline knowledge or a need for specialized advisory channels.

### 2. Seasonal Patterns
* **Harvest Spike:** Crop-related queries peak between **June and September**, with the highest volume in **August**.
* **Insight:** The August surge correlates with the end of the harvest season in Kenya/Uganda, where farmers pivoted to "Yield Optimization" questions in preparation for the next planting cycle.
* **Year-Round Topics:** Animal rearing queries (medicine, disease control) remained consistent regardless of season.

### 3. Geographic & Linguistic Constraints
* **English Dominance:** Kenya and Uganda accounted for 99.9% of English queries. Tanzania's interaction was almost exclusively in Swahili, highlighting the need for future multi-lingual NLP models.

---

##  How to Run

1.  Clone the repository.
2.  Install dependencies:
    ```bash
    pip install pandas scikit-learn matplotlib plotly pyarrow openpyxl
    ```
3.  Run the Jupyter Notebook `Farmer_Questions_Clustering.ipynb`.
4.  View the output report in `Cluster_Summary.xlsx`.

---

## Gen-AI Disclosure
* **Gemini:** Used for optimizing `MiniBatchKMeans` code for large-scale datasets.
* **Copilot:** Assisted in structuring the final analytical report.

---

##  Author
**Jonathan Khabusi** 
*Climate Data Analyst*
