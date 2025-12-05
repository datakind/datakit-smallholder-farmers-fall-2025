
# Challenge 3 - Community Leaders

## Data and System Requirements

1. Raw data stored in file `producers_direct.csv`. Analysis carried out on a sample of ~25% of the data. 
2. Python package dependencies
   1. pandas
   2. numpy
   3. matplotlib
   4. seaborn
3. Results included in `visualizations/` folder

## Approach

### Possible Definitions of Community Leaders - 
1. Activity - Leaders might be those users who are highly active and provide the most responses or who are responsive the most number of days.
2. Expertise - Users who provide responses related to a particular topic more than other topics might be leaders in a specialized field.
3. Geographical Reach - Leaders might address questions from a wider population across different countries than the average user.
4. Reliability - Users who have older accounts and longer tenures, provide quick responses, or respond consistently over a period of time could be more trustworthy than other users.

### Metrics
1. Activity: 
   1. count of unique responses per user
   2. count of unique days when responses were provided
2. Expertise:
   1. purity of response topics using Gini Index
3. Geographical Reach: 
   1. count of unique countries reached through responses
4. Reliability:
   1. length of time elapsed from account creation date
   2. avg response time per question after it is first posted
   3. number of weeks that user has consistently provided responses

## Results and Insights

1. Top 10 users with the most responses provide more than ~3000 responses each, while the overall average of the dataset is approx 17 responses per user.
2. Most number of days that a response user is active = 489.
3. Higher the Gini Index, higher the concentration of responses of a user around a particular topic. In this case, assume a threshold >= 0.75 to indicate a specialized user. The average user has a response Gini Index of 0.2. Some common topics of specialized responses are 'tomato', 'maize', 'cattle', 'chicken'.
4. Data sample does not contain a large geographical reach for responses. Max number of countries for a user = 2.
5. Longest tenure for a user is 2778 days. 39182 users have tenures longer than 5 years.
6. While finding the users that respond the most consistently, remove users who have fewer than 5 total responses. 4566 users are active for more than half the year (26 weeks).

## Future Work

1. Expand analysis to the full 21M dataset based on availability of required compute and memory resources. 
2. Combine individual definitions of leaders into a single, consolidated definition.
3. Create a leaderboard based on individual and consolidated definitions.
4. Incorporate NLP techniques for a more comprehensive analysis.