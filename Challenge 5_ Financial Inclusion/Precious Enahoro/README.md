# Beyond Farming - Financial Inclusion and Livelihood Analysis

## Overview
This project explores how smallholder farmers discuss financial topics such as market prices, credit access, savings, and other non-farming livelihood concerns to better understand their economic realities, challenges, and opportunities for inclusion through financial tools, risk management information, and investments in productivity. This analysis would inform Producer Direct's support for farmer entrepreneurship, market access, and rural financial systems.

## Research Questions
- Question 1: What share of farmer questions relate to financial topics?
- Question 2: How do financial questions vary across seasons?
- Question 3: How do financial questions vary across regions?
- Question 4: How do farmers express financial challenges and opportunities?

## Key Findings

### Key Finding 1: Only 7.7% of all farmer questions are financial — and most of them center on one issue: market price transparency.
![Key Finding 1](https://github.com/PreciousEnahoro/datakit-smallholder-farmers-fall-2025/blob/main/Challenge%205_%20Financial%20Inclusion/Precious%20Enahoro/key-finding-vizzes/Key%20Finding%201.png)

Although fewer than 1 in 10 farmer questions are financial in nature, the majority of those inquiries focus on market price discovery and market access. Farmers consistently ask:

   - *“How much is X selling for?”*
   - *“What is the current market price?”*
   - *“Where can I sell?”*
     
**This shows that even within a small financial segment, market transparency is the dominant financial need, and price information remains a major friction point for farmers across crops and countries.**

**Implications for Producers Direct:**

Producers Direct should:
1. Expand coverage of price data across more markets, crops, and regions.
2. Work with local partners to verify and update prices more frequently.
3. Develop automated price-insight messages, e.g., price drops, best-selling locations, or price anomalies.
4. Include price trend visualizations or weekly summaries to reduce repeated questions.

### Key Finding 2: Financial questions rise during major farming cash-flow cycles—before/during planting (April) and during harvest/selling periods (July–Aug, Nov)
![Key Finding 2](https://github.com/PreciousEnahoro/datakit-smallholder-farmers-fall-2025/blob/main/Challenge%205_%20Financial%20Inclusion/Precious%20Enahoro/key-finding-vizzes/Seasonal%20Trends%20in%20Farmer%20Financial%20Questions.png)

Farmers' financial questions follow strong seasonal patterns:
- Jan–Feb & April: spikes in startup capital, loan access, investment evaluation, affordability concerns — farmers preparing for planting.
- July–August: largest spike in market price questions, driven by major harvest and selling season.
- November: a smaller second peak tied to the short-rains harvest and end-of-year financial pressure.

**Implications for Producers Direct:**

1. Seasonal peaks mean farmer needs are predictable, enabling the company to time educational content, nudges, or onboarding sequences around planting and harvest cycles. Hence, time financial products to farming cycles:
   - Jan–Apr: input loans + cost-saving tips
   - Jul–Aug: market-price tools + selling support
   - Nov: repayment flexibility + savings nudges

2. Prioritize price-discovery features during harvest, since this dominates financial questions.

### Key Finding 3: Ugandan farmers prioritize price discovery, while Kenyan farmers additionally seek credit and startup capital before planting seasons.
Ugandan farmers ask significantly more financial questions than Kenyan farmers, a difference confirmed by a chi-square test (p < 0.001).

Market price questions dominate financial needs in both countries, but **Uganda is far more reliant on price discovery**, with prices accounting for nearly 60% of all financial queries. **Kenyan farmers display a more diversified financial profile**, combining price discovery with strong demand for credit, startup capital, and investment evaluation. In general, seasonal patterns also mirror agricultural cycles.

**Implications for Producers Direct:**
1. Country patterns differ significantly, so localized strategies will be more effective than a uniform financial product.
2. Since price discovery remains essential in both countries, any price-related improvements could generate cross-market impact and create immediate, large-scale value.
3. Kenya’s pronounced demand for loans and startup capital suggests an opportunity for partnerships with lenders or lightweight credit-readiness tools.


## Next Steps 
### For Further Analysis
1. **Recommendation 1**: What could be explored next
2. **Recommendation 2**: How to deepen this analysis
3. **Recommendation 3**: Related questions to investigate

## Limitations and Challenges

### Data Limitations
- Missing data issues
- Data quality concerns
- Sample size or coverage limitations

### Methodological Limitations
- Assumptions made
- Simplifications required
- Alternative approaches not explored

### Technical Challenges
- Computational constraints
- Translation accuracy issues
- Other technical hurdles

## Methodology
### Data Source
- Producers Direct English Dataset

### Approach
**Step 1**: Data loading, cleaning, and preprocessing
   - Processed data efficiently using DuckDB for large-file handling.
   - Cleaned, normalized, and deduplicated raw question data and standardized country codes.  Data was deduplicated to remove multiple responses to a particular question, since the analysis focused only on questions. This reduced the final dataset to ~3M rows.
   - Built classification logic for financial categories and refined sub-themes for each category.
   - Generated binary financial flags, matched keywords, topic groupings, and normalized text fields by implementing regex-based topic extraction.
  
 **Step 2**: Analysis and statistics
   - Conducted chi-square tests to measure significant differences across countries and categories.
   - Performed time series analysis to detect seasonal spikes in financial behavior.
   - Compared product-level economic concerns (e.g., maize vs. poultry vs. tomatoes).
   - Evaluated cross-country patterns in credit needs, subsidies, savings culture, and hardship.
     
**Step 3**: Visualization, report, and interpretation
   - Designed Tableau dashboards to explore and visualize monthly trends, category flows, and country differences [Tableau Packaged Workbook Uploaded]
   - Produced summary insights focused on farmers’ real-world financial pain points.
   - Wrote interpretive narratives explaining behavioral patterns and regional variations.

### Tools and Technologies
- **Programming Language**: SQL
- **GenAI Tools Used**: ChatGPT
- **Other Tools**: Tableau, Excel.

## Use of Generative AI
### AI-Assisted vs. Human-Created
- **AI-Assisted**:
    - Generating SQL CASE WHEN blocks and regex patterns.
    - Debugging SQL/regex errors and restructuring complex logic.
    - Creating aggregation query templates and cleaning functions.
    - Providing statistical test outputs and helping phrase insight summaries.
    - Exploratory thought partner on financial taxonomy and figuring out edge cases.

- **Human-Created**
    - Designed the financial taxonomy and defined all category logic.
    - Cleaned, prepared, and deduplicated the raw farmer-question dataset.
    - Built and validated the final classification rules.
    - Created aggregated tables, trends, and chi-square analyses.
    - Interpreted patterns (seasonality, country differences, product-level insights).
    - Designed Tableau visuals and wrote the final analytical narrative.
    * All AI-generated SQL code and initial insight summaries were reviewed and tested for accuracy.*

## Files in This Contribution

```
your_name_analysis/
├── README.md (this file)
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_data_cleaning.ipynb
│   └── 03_analysis.ipynb
├── scripts/
│   ├── data_loader.py
│   ├── preprocessing.py
│   └── visualization.py
├── visualizations/
│   ├── viz1.png
│   ├── viz2.png
│   └── viz3.png
├── results/
│   ├── summary_statistics.csv
│   └── findings.md
└── data/ (if applicable - only small derived datasets)
    └── processed_sample.csv
```

## Dependencies

SQL code ran using DuckDB driver in DBeaver.
```

### Cleaning the Data and Running the Analysis --to be updated
# Open and run scripts in order:
# 1. 01_data_exploration.ipynb
# 2. 02_data_cleaning.ipynb
# 3. 03_analysis.ipynb
```

## Contact and Collaboration
- **Author**: Precious Enahoro
- **GitHub**: @PreciousEnahoro
- **Linkedin**: (https://www.linkedin.com/in/precious-enahoro/)

**Collaboration Welcome**: 
- Open to feedback and suggestions
- Happy to collaborate on related analyses
- Available to answer questions about this approach

## Acknowledgments
- Inspired by @TrevorW's sharing of how he started to think about the financial taxonomies on Slack!
---

**Last Updated**: 11/26/2025 | **Status**: In Progress

