1.Dataset:



&nbsp;Since the original Dataset is huge, I considered a 10 % sample of data for my analysis. The same analysis can be applied to the entire dataset.


2\. Metric Categories



We compute three families of metrics:



A. Basic Productivity Metrics

Metric	Meaning

unique\_questions\_answered	How many distinct questions the farmer answered

unique\_users\_served		Number of unique users they helped

median\_response\_time\_min	Typical response time

mean\_response\_words		Richness/length of messages



These measure responsiveness \& helpfulness.


 B. Language Metrics

Metric	Meaning

lang\_alignment\_frac		Fraction of responses in the same language as the question

num\_question\_languages\_answered	Languages in which the farmer is able to answer questions

(optional) language\_entropy	Diversity of languages used (not used in final score)



These measure accessibility \& multilingual capacity.


 C. Consistency Metrics



We analyze activity over time (month-by-month).



Metric	Meaning

prop\_months\_active	% of months in which the farmer participated

gini\_monthly		Inequality in month activity (0 = perfectly steady, 1 = extremely spiky)

consistency\_score	Combined score: prop\_months\_active - gini\_monthly



Consistency reflects reliability and long-term engagement.



3\. Composite Leader Score



We standardize metrics using z-score normalization and apply weights:

Leader Score = weighted sum of all standardized metrics.



This ensures the score combines:



* productivity
* helpfulness
* speed
* linguistic alignment
* multilingual ability
* consistency over time



4\. Vizualizations

