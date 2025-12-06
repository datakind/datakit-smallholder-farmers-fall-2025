**Project Overview**:  
- **Name**: Producer Direct — Question Seasonality Analysis  
- **Purpose**: Analyze and visualize seasonal trends in farmers' questions across Producer Direct countries (Kenya, Uganda, Tanzania, etc.). The analysis classifies each question into a farming season (planting / harvest / off-season) and surfaces seasonal keyword patterns and visualizations.

**Dataset**:  
- Source: CSV exported from Producer Direct platform (example filename: `b0cd514b-b9cc-4972-a0c2-c91726e6d825.csv`).  
- Key fields used: `question_content`, `question_sent` (timestamp), `question_user_country_code`.  
- Note: Some countries have extremely imbalanced counts (e.g., KE and UG large, TZ) — interpret small-country results with caution.

**What I implemented**:  
- Seasonal classifier: assigns `farming_season` per row according to country-specific rules:
  - Kenya (KE): Long Rains (Mar–May) = Planting, Short Rains (Oct–Dec) = Planting, Harvest Period (Jun–Aug & Jan–Feb), Sept = off-season.
  - Uganda (UG): Season A (Mar–May planting, Jun–Aug harvest), Season B (Sep–Nov planting, Dec–Feb harvest).
  - Tanzania (TZ): Masika (Mar–May planting), Vuli (Oct–Dec planting in some regions), Harvest (Jun–Aug), else off-season.
- Added `farming_season` column to the dataset by applying the classifier to `question_sent` and `question_user_country_code`.
- Keyword extraction per country and per season (frequency counts, word clouds).
- Comparison table matching expected seasonal keywords with top observed keywords per season.

**Performance & optimization**:  
- The notebook originally used spaCy + sequential processing which was slow on large data. I added options to speed up processing:
  - Parallel batch processing with Python `multiprocessing` to process texts in parallel.
  - A faster regex-based cleaning function as an alternative to full lemmatization (recommended for keyword extraction where lemmatization is optional).
- Tip: Use TF-IDF or relative proportions (percent of season queries) to reduce dominance of very common tokens like `plant` or `grow`.

**Key Findings (example summary)**:  
- Kenya (KE): Dominated by `maize`, `plant`, `cow` — strong crop + livestock mix. Harvest-related words are not top-ranked during harvest in raw counts, suggesting either broad question themes or the masking effect of very frequent generic tokens.  
- Uganda (UG): Clear two-season patterns; `banana` and `coffee` appear strongly as country-specific crops.  
- Tanzania (TZ): Very small samples (TZ ~12) — treat observations as anecdotal.  
- Recommendation: Report proportions (share of season) or TF-IDF-weighted keywords to reveal seasonal-specific signals.

**Libraries**:
pandas
duckdb
matplotlib
seaborn
plotly
nltk
spacy
wordcloud
scikit-learn
scipy
missingno

**Suggested next analysis steps**:  
- Compute season-relative proportions for targeted keywords (e.g., `harvest`, `storage`, `pest`, `price`) and visualize as heatmap.  
- Run TF-IDF per season and per country to surface season-specific terms.  
- If geo subdivision exists (region / admin1), repeat analysis per region to uncover geographic timing differences.  
- For GB / TZ, collect more data before producing firm recommendations.

**How AI assisted this project**:  
- I used AI assistance (GitHub Copilot with GPT-5 mini) to:  
  - Draft and refine the seasonal classifier logic and country rules.  
  - Draft analysis helper code (TF-IDF examples, proportion calculations, heatmap code), and to help write explanatory text and README content.  
- Note: AI was used as an assistant — all final code decisions and interpretations were reviewed and adapted by the project author.

**Reproducibility / Notes**:  
- The notebook contains cells that:
  - Load a sample of the CSV via `duckdb` for efficient sampling and scanning.
  - Preprocess questions, build `question_content_cleaned`, and compute `farming_season`.
  - Generate per-country and per-season keyword tables and visualizations.

