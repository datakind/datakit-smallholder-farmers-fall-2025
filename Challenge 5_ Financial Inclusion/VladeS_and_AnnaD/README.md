# Challenge 5: Financial Inclusion and Livelihood Analysis

## 👥 Authors

| Name | Slak Username | Role |
| :--- | :--- | :--- |
| **VladeS**	| Slack: @VladeS | Lead Analyst, Data Engineering
| **Anna D**	| Slack: @AnnaD | Model Developer, Report & Visualization Generator


---

## 🎯 Project Overview & Goal
This project analyzes **409,384 financial-related questions** submitted by smallholder farmers across **Kenya, Uganda, and Tanzania** using the Producers Direct WeFarm dataset. 

The objective was to uncover financial challenges, sentiment, seasonal patterns, and crop-specific trends while building a robust topic classification system. 
Our ultimate goal was to deliver an evidence-based communication strategy for Producers Direct.

---

## 🛠️ Approach and Methodology

### 1. Data Preparation & Engineering
* **Storage Format:** Initial .csv dataset was converted to **.parquet** for optimized performance.
* **Tooling:** We used **DuckDB** for dataset handling, initial analysis, cleaning, transformation, and enrichment.
* **Filtering:** Isolated financial inquiries using `fin_data = df[df.is_fin_question == 1]`.
* **Standardization:** The `question_sent` timestamp was standardized with `pd.to_datetime(errors="coerce")`, resolving microsecond and timezone inconsistencies.
* **Cleaning:** Extensive text cleaning removed noise and normalized punctuation.

### 2. Multi-Stage Categorization
* **Step 1: Keyword-Based Categorization (Indicative Analysis):** * Performed for both English and Swahili subsets. 
    * English keywords were chosen by category, then translated to Swahili using **Gemini (LLM)**. 
    * The LLM was prompted to account for **regional linguistic peculiarities and colloquial speech**.
* **Step 2: Machine Learning Classification:** * A **TF-IDF + LinearSVC classifier** was trained on over **320,000 labeled samples** with a vocabulary of ~115,000 features.
    * A **rule-based correction layer** was added to improve predictions for imbalanced classes (specifically *unknown* and *general* topics).

### 3. Future Work (Pending)
* **Vector Embeddings:** Our original plan included question embedding into a vector database for semantic analysis of the `is_fin_question` subset. 
Due to the project deadline, this remains undone. We are keen to continue with this if helpful for the project's long-term goals.

---

## 📈 Key Results & Insights

### Crop-Specific Trends
Topic-country pivot tables revealed the dominant crops per region:
* **Kenya:** Chicken (13,061 questions)
* **Uganda:** Maize (17,753 questions)
* **Tanzania:** Rice (39,209 questions)
* *Insight:* The top three crops represent **65–75%** of all crop-specific financial questions.

### Sentiment & Pain Points
Sentiment analysis using **VADER** identified primary negative-sentiment triggers:
* **Top Keywords:** *Price* (3,498), *Market* (2,396), and *Have* (2,312).
* These terms represent over **70% of financial concerns**.
* Distress is highly concentrated in staples (Chicken and Maize), accounting for ~70% of crop-related financial problems.

### Temporal Patterns
* **Seasonality:** Volume peaks in **March and October** (aligned with planting/harvest cycles).
* **Weekly Activity:** **Thursday** is the most active day (~20–30% of weekly volume).

---

## 💡 Strategic Recommendation
Based on our findings, we propose the following communication strategy:
> **Action:** Send targeted **Thursday SMS price alerts** focused on the top three crops per country. 
This strategy addresses over **70% of the financial barriers** currently faced by farmers in the network.

---

## ⚙️ Dependencies
* **Python 3.x**
* **Core Libraries:** `pandas`, `numpy`, `scikit-learn`, `duckdb`, `vaderSentiment`, `matplotlib`, `seaborn`