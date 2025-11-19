# Yu-hui Lien

## challenge-4-crop-questions-traditional method.ipynb

## 1. Executive Summary

This notebook involves text data cleaning and preprocessing applied to 11.5M rows of English farmer questions, and then utilizes a Prioritized Lexical Classification approach to categorize general questions into predefined business concepts (e.g., Pest & Disease, Market & Finance).

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

# challenge-4-crop-questions-transformer.ipynb

## 1. Executive Summary

This project categorizes **~100k rows of English farmer questions** using **Guided BERTopic**, addressing stability problems from standard clustering.

Key improvements include deep text cleaning and semi-supervised clustering using business-defined seed topics.

### Key Findings:

- High-volume data requires strong filtering (`min_topic_size=1000`).
- Seed topics successfully distinguish ambiguous concepts (e.g., poultry vs. planting).

## 2. Data

| Feature | Description | Status |
|--------|-------------|--------|
| **Source Data** | parquet | Loaded |
| **Target Column** | `question_content_cleaned` | Used |
| **Data Size** | 100k+ rows | Processed |

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
![Subtopic Classification of General Questions using BERTopic](https://github.com/yhlien1221/datakit-smallholder-farmers-fall-2025/blob/main/Challenge%204_%20Crop%20Questions/Yuhui_Lien/pictures/bertopic_overall_distribution_full_label_final.png)

### A. Subtopic Classification of General Questions using BERTopic

This BERTopic distribution chart suggests that the current model parameters still require further optimization to achieve a balanced and coherent classification. The most notable issue is the dominant presence of generic and vague clusters, such as the 'what_where_you_how' topic at 17.3%, which indicates the model is failing to create highly specific or actionable groups. Furthermore, the top four topics account for over two-thirds of the data, with several categories being overly broad (e.g., 'animal_milk_animals_what' at 16.1%), preventing a clear, fine-grained understanding of the underlying farmer concerns. This imbalance signals the need for refining hyperparameters or utilizing a more restrictive set of seed topics.


### Key Output Columns:

- `BERTopic_Topic_ID`
- `BERTopic_Label`
- `Topic_Key_Label`

### Next Steps:

1. Run full dataset (3M rows)  
2. Visualize hierarchical structure 
Optimize Clustering Parameters: Refine BERTopic hyperparameters (e.g., min_topic_size, UMAP settings) to reduce the volume of vague or overly broad clusters and improve the specificity of subtopic assignments. 


## Challenge 4: Crop Question Analysis: Farmer Questioning and System Response Patterns

## 1. Executive Summary

### Key Findings:

* **Critical Mismatch (High Risk Area):** The topic **bird** exhibits the highest **Demand Complexity** ($\text{Rank 1}$) but receives disproportionately low **Supply Detail** ($\text{Rank 10}$ or lower), indicating a critical knowledge gap and high potential for negative farmer response (e.g., frustration, repeat queries).
* **Dominant Demand:** $\text{General\_Topic}$, $\text{cattle}$, and $\text{maize}$ consume the highest system bandwidth due to sheer volume ($\text{Report A}$).
* **Specialized User Behavior:** Farmers asking about niche, specialized crops ($\text{peach}$, $\text{pear}$) formulate the most complex, detailed questions, even though their volume is low ($\text{Report B}$).
* **Supply Efficiency:** The system's longest answers are concentrated on low-volume, specialized topics ($\text{rye}$, $\text{pigeon-pea}$), suggesting that knowledge scarcity, rather than user volume, drives resource allocation for detail.

---

## 2. Data

The analysis utilized the provided agricultural question-and-answer dataset (`bertopic.csv`).

| Column Used | Description | Purpose in Analysis |
| :--- | :--- | :--- |
| `question_topic` | Pre-existing classification of the question's subject (e.g., maize, poultry). | Primary grouping variable for all cross-analyses. |
| `question_content_cleaned` | Cleaned text of the farmer's question. | Used to derive **Demand Complexity** ($\text{Specificity Score}$). |
| `response_content` | Answer provided by the system or community. | Used to derive **Supply Detail** ($\text{Response Score}$). |

---

## 3. Methodology

The core of the analysis is a **Supply-Demand Mismatch Model** built on three key quantifiable metrics:

### 3.1 Feature Engineering (Quantification)
To allow for direct comparison, we used **Min-Max Normalization** to scale all metrics to a uniform $[0, 1]$ range.

* **Demand Complexity Score (Report B):** Calculated by normalizing the raw **Question Length** (word count) for *each individual question*, then taking the average score per topic. (Higher score = more detailed demand).
* **Supply Detail Score (Report C):** Calculated by normalizing the raw **Answer Length** (word count) for *each individual response*, then taking the average score per topic. (Higher score = more detailed supply).
* **Demand Volume (Report A):** Raw count of questions per topic.

### 3.2 Cross-Topic Analysis
Metrics were aggregated using `df.groupby('question_topic').agg()`. The analysis focused on identifying patterns where **Demand Complexity $\ne$ Supply Detail**.

---

## 4. Results and Visualization

The following reports quantify the relationship between farmer necessity and platform content flow.

### Report A: Demand Volume (Question Repetitiveness)
**Figure 1:** Total Demand Volume by Topic.
[IMAGE PLACEHOLDER: report\_a\_repetitiveness\_mpl.png - Demand Volume (Question Count)]
* **Takeaway:** The top 4 topics ($\text{General\_Topic}, \text{cattle}, \text{maize}, \text{chicken}$) represent the highest consumption of system capacity.

### Report B: Demand Complexity Ranking
**Figure 2:** Ranking of Topics by Average Farmer Question Complexity.
[IMAGE PLACEHOLDER: report\_b\_demand\_specificity\_mpl.png - Question Complexity Ranking]
* **Takeaway:** Farmer effort is highest for niche crops ($\text{peach}, \text{pear}$), indicating these specialized subjects require maximum user input for proper context.

### Report C: Knowledge Supply Detail Ranking
**Figure 3:** Ranking of Topics by Average Answer Detail (Supply).
[IMAGE PLACEHOLDER: report\_c\_supply\_detail\_mpl.png - Knowledge Supply Detail Ranking]
* **Takeaway:** The system's resource allocation for detail is highest for topics driven by **knowledge scarcity** ($\text{rye}, \text{pigeon-pea}$).

---

### Next Steps:

1.  **Mismatch Intervention:** Implement a content rule that automatically flags any **bird** or **poultry** answer that falls below the system's overall average response length for manual review before delivery.
2.  **Longitudinal Study:** Track the `Question_Count` over time for high-risk topics like `bird` to see if the demand volume changes following the content intervention.
3.  **User Feedback Integration:** Integrate a simple "Was this answer useful?" feedback mechanism to directly measure the farmer's **response**, allowing us to validate the quantitative Mismatch Model against actual satisfaction data.