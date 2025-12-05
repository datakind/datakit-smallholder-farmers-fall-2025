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
- July–August: most significant spike in market price questions, driven by major harvest and selling season.
- November: a smaller second peak tied to the short-rains harvest and end-of-year financial pressure.

**Implications for Producers Direct:**

1. Seasonal peaks mean farmer needs are predictable, enabling the company to time educational content, nudges, or onboarding sequences around planting and harvest cycles. Hence, time financial products to farming cycles:
   - Jan–Apr: input loans + cost-saving tips
   - Jul–Aug: market-price tools + selling support
   - Nov: repayment flexibility + savings nudges

2. Prioritize price-discovery features during harvest, since this dominates financial questions.


### Key Finding 3: Ugandan farmers prioritize price discovery, while Kenyan farmers additionally seek credit and startup capital before planting seasons.
Ugandan farmers ask significantly more financial questions than Kenyan farmers, a difference confirmed by a chi-square test (p < 0.001).

![Key Finding 3a](https://github.com/PreciousEnahoro/datakit-smallholder-farmers-fall-2025/blob/main/Challenge%205_%20Financial%20Inclusion/Precious%20Enahoro/key-finding-vizzes/Financial%20Questions%20as%20a%20Share%20of%20Total%20Farmer%20Queries%20(by%20Country).png)

Market price questions dominate financial needs in both countries, but **Uganda is far more reliant on price discovery**, with prices accounting for nearly 60% of all financial queries. **Kenyan farmers display a more diversified financial profile**, combining price discovery with strong demand for credit, startup capital, and investment evaluation. In general, seasonal patterns also mirror agricultural cycles.

![Key Finding 3b](https://github.com/PreciousEnahoro/datakit-smallholder-farmers-fall-2025/blob/main/Challenge%205_%20Financial%20Inclusion/Precious%20Enahoro/key-finding-vizzes/Financial%20Subcategory%20Mix%20by%20Country.png)

**Implications for Producers Direct:**
1. Country patterns differ significantly, so localized strategies will be more effective than a uniform financial product.
2. Since price discovery remains essential in both countries, any price-related improvements could generate cross-market impact and create immediate, large-scale value.
3. Kenya’s pronounced demand for loans and startup capital suggests an opportunity for partnerships with lenders or lightweight credit-readiness tools.


### Key Finding 4: Farmers use two distinct financial vocabularies: one signaling immediate hardship (“no money,” “things are expensive”), and another signaling opportunity through investment, profitability, and high-earning crop choices.

![Key Finding 4](https://github.com/PreciousEnahoro/datakit-smallholder-farmers-fall-2025/blob/main/Challenge%205_%20Financial%20Inclusion/Precious%20Enahoro/key-finding-vizzes/Sankey%20Plot%20-%20Farmers%20Challenges%20and%20Opportunities.png)

Farmers frame financial questions in practical, outcome-driven language. Common expressions fall into these core categories:

1. **Affordability Problems:** “too expensive,” “no money for inputs,” “cannot afford fertilizer.”
2. **Liquidity Requests:** “help me with money,” “I need funds,” “lend me some money.”
3. **Startup & Investment Planning:** “how much capital do I need to start poultry?”
4. **Profit Opportunity Seeking:** “which crop brings quick money?,” “what business gives profit fast?”
5. **Price Intelligence:** “how much is maize today?,” “how much is rice in Gulu?”
6. **Cost-Minimization:** “cheapest method,” “what type of goat is the cheapest?”

**Implications for Producers Direct:**
1. Farmers’ financial concerns are focused on cash flow, affordability, and immediate next steps — tools should match this behavior. As mentioned throughout this analysis, Price discovery is an essential financial infrastructure, especially for Uganda. Improving price accuracy, frequency, and localization directly addresses the top pain.
2. Financial challenge language (especially “no money”, “too expensive”) signals distress, which could be used to trigger nudges, alternative low-cost recommendations, or subsidy program information.
3. Quick-money / profitability queries indicate high demand for guidance on viable crops, which could inform seasonal extension campaigns.
4. Support requests reflect a belief that the platform can provide financial support—messaging and expectations need to be clarified if this is not the case.

## Next Steps 
### For Further Analysis
1. **Deepen crop-level analysis:** Identify which financial concerns (prices, loans, profitability) matter most for each major crop to inform targeted advisory content.
2. **Add non-English data:** Integrate Luganda, Swahili, Runyankole, etc., to capture financial language patterns currently missing from the English-only sample.
3. **Improve classification with ML:** Use embeddings or a lightweight supervised model to resolve edge cases (e.g., invest vs infest, interest, ambiguous “money” use).
4. **Temporal validation:** Check whether seasonal patterns persist across multiple years or shift with weather anomalies.


## Limitations and Challenges

1. Manual category interpretation: Subcategory rules were refined by human judgment—useful but subjective and not perfectly reproducible.
2. Non-English questions excluded: Large volumes in Luganda/Swahili were not analyzed, creating language bias.
3. Early filtering by eye: Some data corrections were made through visual inspection, which may not scale or be consistently repeatable.
4. Keyword-based classification: Regex logic can misclassify misspellings, slang, or nuanced intent (e.g., invest vs infest). The long regex patterns used for crop/financial term detection are brittle and require constant maintenance.
5. Data quality noise: Duplicates, missing and incomplete fields, inconsistent formatting, and unstructured text increase classification uncertainty.
6. No automated text-modeling: Without embeddings or machine learning, nuanced financial intent may be underestimated or mislabelled.


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
   - Designed Tableau dashboards to explore and visualize monthly trends, category flows, and country differences [Dashboard Link - Tableau Public](https://public.tableau.com/app/profile/precious.o.enahoro/viz/DataKindandProducersDirectDataKitChallenge-PreciousEnahoro-Challenge5/KeyFinding1)
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
    - Providing statistical test outputs and helping phrase initial insight summaries for this report.
    - Exploratory thought partner on financial taxonomy and figuring out edge cases.
    - Code to create the Sankey diagram for Key Finding 4.

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
Precious Enahoro/
├── README.md (this file)
├── key-findings-vizzes/
│   ├── Financial Questions as a Share of Total Farmer Queries (by Country).png
│   ├── Financial Subcategory Mix by Country.png
│   ├── Key Finding 1.png
│   ├── Sankey Plot - Farmers Challenges and Opportunities.png
│   ├── Seasonal Trends in Farmer Financial Questions By Country.png
│   ├── Seasonal Trends in Farmer Financial Questions.png
│   └──images.md
├── sql_scripts/
│   ├── base_analysis_scripts/
|   │   ├── README.md
|   │   ├── base_tables_for_chi_square_tests.sql
|   │   └── finding_pct_subcategory_per_month.sql
│   ├── **README.md (has the directions on how to run the scripts)**
│   ├── cleaning_question_topic_field.sql
│   ├── condensing_financial_subthemes.sql
│   ├── data_loading_and_main_financial_classifier.sql
│   ├── deduping_questions.sql
│   ├── downloading_streamlined_file_to_desktop.sql
│   └── extra_data_cleaning.sql
└── tableau/ 
    └── Tableau Public Link.md
```

## Dependencies

SQL code ran using DuckDB driver in DBeaver.


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

**Last Updated**: 11/29/2025 | **Status**: Complete

