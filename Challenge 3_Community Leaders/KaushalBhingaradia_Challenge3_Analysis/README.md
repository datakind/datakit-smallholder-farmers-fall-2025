# DataKind Challenge 3: Identifying Community Leaders



### Author

Kaushal Bhingaradia



### Objective

This project analyzes interaction data from Producers Direct’s farmer-to-farmer digital network to identify top community leaders, understand engagement patterns, and provide data-driven recommendations for strengthening community knowledge sharing.



### Approach

1. **Data Understanding** – Explored the structure of questions, responses, users, and locations. 

2. **Exploratory Analysis** – Generated summary statistics, response distributions, and engagement metrics.

3. **Network Analysis** – Modeled user interactions using NetworkX to reveal leadership hubs. I had to use a smaller sample as the original dataset was very large and was too much for my personal computer to handle.

4. **Similarity Detection** – Used text similarity metrics to identify repetitive questions.

5. **Composite Scoring** – Built a leaderboard based on multiple engagement factors.



### Key Insights

- **Top 1% of responders** handle **28.9%** of all responses.  

- **Average leader** engages with **5,810 unique farmers**.  

- **Engagement ratio** of **0.58** shows quality over quantity.  

- **55.2%** of questions are similar → opportunity for FAQ/knowledge base.  

- **Network follows a power-law** → leaders act as community hubs.



### Recommendations for Producers Direct

- Retain and empower the **top 20 leaders** who drive trust and engagement.  

- Encourage **topic specialization programs** for expert recognition.  

- Reduce redundancy through **FAQ and curated resources**.  

- Use the **composite scoring model** to identify emerging leaders early.



### Use of Generative AI

This analysis was completed with **human oversight and GenAI support**:

- **Tool used:** Gemini and Claude Code (for ideation and code assistance)  

- **Purpose:** Accelerating data exploration, organizing code, refining visualizations, and structuring documentation.  

- **Human review:** All code, outputs, and insights were manually validated for correctness and relevance.



### Files

- `DataKind_Challenge_3_Identifying_Community_Leaders.html` – Full Jupyter Notebook export  

- `community_leaders.csv` – Final leaderboard with composite leader scores  (removed as it is a very large file)

- `community_leaders_analysis.png` – 4 visualizations from the analysis for top leaders, reach, topic specialization, and network distribution.

- `community_network.png` – 4 visualization of the user network distribution.

- `README.md` – Project summary and documentation  



### Outcome

This project identifies measurable traits of community leaders and proposes strategies for Producers Direct to strengthen its global farmer network through data-driven insights.



