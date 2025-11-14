# Yu-hui Lien
# Submission - 1

## Challenge 4 – Crop Questions (Traditional Method)

## 1. Executive Summary

This project utilizes a **Prioritized Lexical Classification** approach to categorize 11.5M rows of **English** farmer questions into predefined business concepts (e.g., Pest & Disease, Market & Finance).

The classification relies on finding keywords in the question text based on a **hierarchical priority structure**, ensuring consistency with business rules.

### Key Findings:

- The lexical approach provides rapid and interpretable topic assignments based on explicit keyword rules.
- This method requires meticulous maintenance of the keyword dictionary to remain effective.
- Preliminary results show an imbalance, with **66% Specific Questions** and **34% General Questions**.

## 2. Data

| Feature | Description | Status |
|--------|-------------|--------|
| **Source Data** | `parquet` file (Kaggle) | Loaded |
| **Target Column** | `question_content_cleaned` | Used |
| **Data Size** | ~11.5M rows | Processed |
| **Time Span** | Long-term dataset | Categorized |

## 3. Methodology: Prioritized Lexical Classification

The approach ensures high-priority topics (like immediate risks) are detected first.

### A. Data Preprocessing

- Basic cleaning: lowercasing, punctuation removal  
- Goal: maximize keyword match accuracy

### B. Prioritized Keyword Matching

Questions assigned to the **first matched category** using the priority order below:

1. **Immediate Action / Risk**  
2. **Foundational Management**  
3. **Farming Technique**  
4. **Conceptual**  
5. **Administrative / Vague**

### C. Tuning for Robustness

- Keyword dictionary requires regular updates.
- Unmatched questions → labeled **Unclassified**.

## 4. Results and Visualization

![Overall Topic Proportion](https://raw.githubusercontent.com/yhlien1221/datakit-smallholder-farmers-fall-2025/main/Challenge%204_%20Crop%20Questions/Yuhui_Lien/pictures/topic_proportion_overall.png)

![Topic proportion trend](https://github.com/yhlien1221/datakit-smallholder-farmers-fall-2025/blob/main/Challenge%204_%20Crop%20Questions/Yuhui_Lien/pictures/topic_proportion_trend.png)

![Distribution of general question into subtopics](https://github.com/yhlien1221/datakit-smallholder-farmers-fall-2025/blob/main/Challenge%204_%20Crop%20Questions/Yuhui_Lien/pictures/general_topic_breakdown_final_corrected.png)

### A. Topic Distribution (Overall)

Specific Questions: 66%  
General Questions: 34%

### B. Topic Distribution by Time

Convergence between categories observed around Aug–Sep 2021.

### C. Subtopic Breakdown for General Questions

- Unclassified/Other/Vague: **34.8%**  
- Farming Technique: **28.7%**  
- Concept & Definition: **15.5%**  
- Soil & Water Management: **6.9%**

## 5. Conclusion and Next Steps

Lexical classification is fast, interpretable, and effective for initial categorization, but maintaining the keyword dictionary is challenging.

### Output Columns:

- `question_content_cleaned`
- `broad_topic`

### Next Steps:

1. **Enhance Subtopic Classification with BERTopic**  
2. Improve classification of Unclassified questions.

---

# Submission - 2
# Project: Guided Topic Modeling for Smallholder Farmer Questions (Challenge 4)

## 1. Executive Summary

This project categorizes **100,000+ farmer questions** using **Guided BERTopic**, addressing stability problems from standard clustering.

Key improvements include deep text cleaning and semi-supervised clustering using business-defined seed topics.

### Key Findings:

- High-volume data requires strong filtering (`min_topic_size=1000`).
- Seed topics successfully distinguish ambiguous concepts (e.g., poultry vs. planting).
- Topic trends remained stable across the analyzed 3-day dataset.

## 2. Data

| Feature | Description | Status |
|--------|-------------|--------|
| **Source Data** | CSV or parquet | Loaded |
| **Target Column** | `question_content_cleaned` | Used |
| **Data Size** | 100k+ rows | Processed |
| **Time Span** | 3 days (2017-11-22 to 2017-11-24) | Analyzed |

## 3. Methodology: Guided BERTopic and Optimization

### A. Deep Preprocessing

Custom cleaning solved issues like `poutry → poultry`.

- Replacements using `replacement_map`
- `CountVectorizer` with custom stopwords  
- `min_df=0.001` to remove noise

### B. Guided Clustering

Seed topics enforce business logic:

1. Market & Finance  
2. Pest & Disease  
3. Livestock  
4. Farming Technique  

### C. Hyperparameter Tuning

| Parameter | Purpose | Value | Reason |
|----------|---------|-------|--------|
| `min_topic_size` | HDBSCAN | 1000 | Prevent noisy micro-topics |
| `n_neighbors` | UMAP | 75 | More stable embedding |
| `n_components` | UMAP | 5 | Simplify structure |

## 4. Results and Visualization

### A. Overall Topic Distribution

Model produces coherent topics aligned with business themes.

### B. Time-Based Topic Trends

Daily analysis shows emerging shifts in focus over the three-day window.

## 5. Conclusion and Next Steps

The Guided BERTopic pipeline resolves clustering instability for large-scale, noisy text.

### Key Output Columns:

- `BERTopic_Topic_ID`
- `BERTopic_Label`
- `Topic_Key_Label`

### Next Steps:

1. Run full dataset (3M rows)  
2. Visualize hierarchical structure  
