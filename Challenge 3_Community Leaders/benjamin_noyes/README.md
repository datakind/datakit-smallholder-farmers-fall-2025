# Introduction
### Datakind Datakit: Smallholder Farmers
This analysis was produced for a DataKit event, hosted by DataKind, in tandem with Producers Direct.

The dataset comes from WeFarm, a farmer-to-farmer question and answer service that operated via SMS. Smallholder farmers could ask a question via SMS to the WeFarm system the system would decide which users to send questions to, and then these users would respond to the system with the answers. All responses were then forwarded to the question poster in real time via SMS. WeFarm operated primarily in East Africa from 2017-2021, but was shut down during COVID.

The data itself is very large and heavily text-based. The unmodified data has around 20 million rows. Columns include “question text”, “response text”, “timestamps”, and the various user id columns. Categories pf text were included, but nulls were highly present at over 60%, and the categories that did exist varied in their usefulness. Based on this data, DataKind challenged event participants with identifying leaders in the dataset, uncovering network effects, and ultimately understanding how smallholder farmers were interacting within WeFarm.

This analysis aims to define segments of leaders in the data, create topic categories, and see which topics leaders were talking about. It defines leaders in four different ways (detailed below in the section “Four dimensions of leadership”), but generally, leaders are the “superusers” of the service, who either use the service more frequently, or over a longer period of time, or respond more quickly, etc.

More specifically, the segmentation was calculated by responses – not by questions. The thought process was: if leaders are the ones who have the expert knowledge, and are actively using WeFarm to empower other smallholder farmers, that data will come from response behavior.

Once the segmentation was completed, this analysis drilled down to then looked at the questions those leaders produced. The ultimate goal was to examine the following: what were the leaders unsure about? Essentially, what are the most important pain points of the leader market?

This dashboard is hosted on Amazon Web Services, and is available at the domain here:
https://bn.datakit-smallholder-farmers.com/

### General themes
The social currency concept
- Much of the data supports the idea that WeFarm was used as a means of sharing success, as opposed to purely a q&a service.
High-context culture
- The cultures of Uganda and Kenya are considered “high-context”, which means that context can supersede semantic accuracy. This can prove challenging for data analysis – for example, users who scored low on various leadership dimensions asked more questions about "diversification" (“expand”, “begin”, “how”, “when”); initially, it would appear that new users were the ones seeking to expand their farming portfolio. However, when all the data is looked at in aggregate, it is also notable that these terms could be euphemisms for accumulating social status within the service, and being well-known in the local community as an expert.
- More examples of this are in the Insights section at the end of the document.
What are the downstream effects of WeFarm?
- How does the social status of being a “WeFarm influencer” tie in to how local business is done? 
Is the Q&A market taken over by ChatGPT and Google?
- Where could a new version of WeFarm provide the most value?
What are the emotional benefits of WeFarm?
- Could these be amplified in any way, to create a network / community among smallholder farmers?

# Data preparation
### Sample space
English speaking users only. No translation was performed, though the pipeline allows for more data to be ingested, if translation is done beforehand. With the current data, the vast majority of English-speaking users were based in Kenya and Uganda, so this analysis focused on those two regions.

### Four dimensions of leaders
Leaders were defined by their responses.
- Count: by user, the total number of responses each user had.
- Speed: by user, the mean difference between the time questions were posted, and the time their response was sent.
- Reach: by user, the number of unique question askers that the responding user reached.
- Tenure: by user, the raw difference in time between his/her first response and his/her last response.

Each of the four segmentation dimension has 5 ordinal categories: from 1 (low), 2, 3, 4, to  5 (high). In this way, the final 20 subsegments look like this:

- Count_1, Count_2, Count_3, Count_4, Count_5 (100% of users)
- Speed_1, Speed_2, Speed_3, Speed_4, Speed_5 (100% of users)
- Reach_1, Reach_2, Reach_3, Reach_4, Reach_5 (100% of users)
- Tenure_1, Tenure_2, Tenure_3, Tenure_4, Tenure_5  (100% of users)

Notably, each dimension is treated independently, with 1, 2, 3, 4, and 5 of each dimension summing to 100% of all users.

Along the same lines, Count_5 and Speed_5 are not the same subsegment – there is no connection between the numerical labels, besides donating more leadlike behavior. Count_5 is comprised of leaders as analyzed by Count, and Speed_5 is comprised of leaders as analyzed by Speed. 

From here, it is possible to take the intersection of subsegments, i.e. users who were both in Count_5 and in Speed_5. This new user group (or “custom segment”) is like a venn diagram. More information can be found on Tab 3 of the dashboard.

If you’re interested in what defines Count_1 vs Count_2  vs Count_3, and so on, the notebook for this segmentation can be found on GitHub here.

### Topic Analysis
Text analysis was originally relegated to LDA, with top_n=30 and with number of categories k as np.linspace(5, 30, 6), to investigate where clusters naturally appeared. Several common themes emerged, including “disease”, “crops”, and “economic”.

Based on information from Producers Direct and DataKind, several other topics were included, such as “financial inclusion” and “diversification”.

From here, 7 broad categories were created (all categories can be found in the appendix). Within each broad category, around 5~50 terms were included for investigation. For each of these in total ~100 terms:
- Similar terms were computed in vector space, using word2vec with min_count=1
- Questions were tagged as “including” if they included any of those similar terms
- A sparse dataframe of questions and their topics was created – these topics were not mutually exclusive, as a question could ask about both “passionfruit” and “drought” in the same question

From here, the count of mentions was summed together, and divided by the total user group, to find the % of the user base’s questions that mentioned each topic.

# Navigating the dashboard
### Dropdowns
- Basic segments
    - Country: the country (or countries)
    - Segmentation: the four dimensions of leader segmentation
    - Individual segments: the subsegments 1, 2, 3, 4, 5 of each dimension.
- Custom segments: the intersection of different subsegments, like Count_5 and Tenure_5.
    - Country: the country (or countries)
    - Count: the individual subsegments within Count
    - Speed: the individual subsegments within Speed
    - Reach: the individual subsegments within Reach
    - Tenure: the individual subsegments within Tenure
- Topic: the % of the selected user segment(s) that used words similar to the given keyword in their questions.
    - Broad topic: the broad category of keywords to zoom in on.
    - Niche topic: the specific keyword to zoom in on.
    - Toggle: this changes the graph from aggregate of all keywords in that category (“broad”) to zoom in on specific keywords (“niche”)
- Time:
    - Time slice: the time dimension over which users talked about the topics.

### Tabs
1. Tab 1, Geography: The number of users in each country.
2. Tab 2: Basic segments: the distribution of the four dimensions of leaders.
3. Tab 3: Custom segments: the drilldown of the subsegment intersections; for example, the intersection of Speed_1 and Tenure_5
4. Tab 4: Topic: the % of the user segment(s) that used words similar to the given keywords.
5. Tab 5: Time: the % of the user segment(s) that used words similar to the given keywords, over time.

# Insights
Analysis with images can be foud here: https://docs.google.com/document/d/1ss3YIwQBhB1awjnIaxl2X3MBfR5zfU0s1obNl4Jb3U8/edit?tab=t.0
##### Prized livestock
- Datapoint: leaders (as defined by response count) talked more about livestock than non-leaders, and this disparity increased over time. Specifically, valuable livestock –  such as a cattle, goats, donkeys, and camel – were where this difference was centralized. Chatter about less valuable livestock topics, such as hens, chickens, and poultry did not see a difference.
- Analysis: In Uganda, leaders may have talked more about valuable livestock as a means of sharing their success – in the US, this could be similar to how users post on Instagram to brag about their latest birthday party.
- Insight: the emotional value of WeFarm may have added to the total value of the service in Uganda. The data suggests this trend increased over time.

 
##### Heat
- Datapoint: leaders (as defined by response count) talked more about “heat” than nonleaders. The relationship over time is a bit more subtle, but in general, the total percentage of questions that mentioned “heat” increased over time, and in Uganda, there appears to be a linear relationship within leaders between “year” and “heat”.
- Analysis:
    - Scenario 1: global warming could have led to an increase in temperatures, therefore causing people to post more about “heat” as the years went on. However, this seems unlikely, as macro data on temperatures in Uganda and Kenya were fairly consistent from 2017 – 2021.
    - Scenario 2: social currency is used everywhere, but especially in high context cultures. Both Kenya and Uganda are categorized as high context cultures. “Heat” could have been a euphemism for activity on the site.
    - Scenario 3: similar to how people in the US find solace in lamenting large-scale problems, farmers could simply be talking more about “heat” as an easy means of connecting with other farmers through connecting over day-to-day grievances.
    - There are certainly many other possibilities as well. Regardless, the data shows that “heat” was talked about more among people who posted more, and more over time.
- Insight: In all three of these scenarios, “heat” is not talked about as a means of answering questions, but rather about the social context around the term. That’s not a bad thing – easy access to quote-on-quote “inexpensive” contextual social currency allows for a more vibrant social ecosystem.

 
##### Diversification
- Datapoint: several terms around diversification/expansion (“expand”, “begin”, “how” and “when”) were talked about more by specific subsets of nonleaders than by leaders.
- Analysis: nonleaders here can generally be understood as people who didn’t use the service that much.
    - Scenario 1: these questions tie in to how someone might begin to accumulate social currency on the platform, a pathway to becoming an active user.
    - Scenario 2: if we think from a different perspective, nonleaders could be a subset who do use it as a q&a platform – when they have a real question about “how” to do something, or “beginning” in a new area of farming, they could use the service to get local knowledge.
- Insight: as more data accumulates, it seems that the service was just as much a means of social connectivity as it was a means of question & answer – whether that is specific to active users, or ingrained in the culture of the region; that is beyond the scope of this analysis.
- Potential product idea: In a new version of WeFarm, it could be useful to have an option “question=answered” that the question asker could mark, which might sway the dynamic more towards q&a, if that is what is desired.

 
##### Financial inclusion
- Datapoint: similar to the above analysis, financial topics such as “sell”, “money”,  “credit”, “loan”, and etc. were talked about more by nonleaders, whereas the terms “market” and “bank” were used more by leaders.
- Analysis: Again, it is very difficult to say if this is because of the high-context nature of the cultures, or if new users are actually looking for financial wisdom, and elder users are sharing that wisdom.
- Insight: Same as above – both scenarios seem plausible.
- Product idea: making it clear that the marketplace would be available to all farmers (if this is true) could remove tension / the need to compete within the WeFarm ecosystem.


# Conclusions, thoughts for further analysis
- Qualitative interviews:
    - A focus group or an ethnographic study would help immensely in identifying the context with which farmers operated on the service.
- The social currency concept: while social in nature, it can still identify success
    - Much of the data supported the idea that users on WeFarm were using the service as a means of sharing success, as opposed to purely a q&a service.
    - High-context languages and cultures are difficult to navigate, as context can supersede semantic accuracy (speaking from my own [limited] experience living/working in China); however, they can still point to legitimate metrics of success. For example, if active users are posting more about prized livestock, that could be both because they want to share their success more, and also because they have more prized livestock to share. Therefore, even if we assume that if the desire for social currency is not constant, it’s still likely the WeFarm system identified farmers who genuinely had more prized livestock, and funneled questions to them – it just identified both users who had more prized livestock, and also had the drive to share their success.
- What are the downstream effects of WeFarm?
    - How does the social status of being a “WeFarm influencer” tie in to how local business is done? 
    - How are local youths tied in to WeFarm?
- Is the Q&A market taken over by ChatGPT and Google?
    - Where could a new version of WeFarm provide the most value?
- What are the emotional benefits of WeFarm?
    - Could these be amplified in any way, to create a network / community among smallholder farmers?

# Appendix
There are two categories of topics: broad categories and niche categories
climate
  "season",
  "time",
  "climate",
  "water",
  "rain",
  "heat",
  "sun",
  "temperature",
  "flood",
  "drought"
crop
  "crop",
  "soil",
  "fruit",
  "plant",
  "leave",
  "fertilizer",
  "seed",
  "potatoes",
  "passion",
  "maize",
  "tomatoes",
  "banana",
  "manure",
  "layer",
  "coffee",
  "tea",
  "onions",
  "grow",
  "mulch",
  "bean",
  "type",
  "cabbage",
  "land",
  "variety",
  "yield",
  "keep",
  "rice",
  "harvest",
disease
  "disease",
  "sick",
  "unhealthy",
  "medicine",
  "treat",
  "weed",
  "control",
  "plant",
  "leave",
  "spray",
  "harvest",
  "affect",
  "prevent",
  "pests",
  "chemical",
  "rabbit",
  "care",
  "tick",
  "attack",
  "mean",
  "black",
  "space",
  "turn",
  "keep"
diversification
  "new",
  "expand",
  "begin",
  "best",
  "increase",
  "clear",
  "add",
  "diversify",
  "irrigation",
  "obtain",
  "shift",
  "acquire",
  "scale",
  "register",
  "use",
  "acreage",
  "grow"
financial inclusion
  "economy",
  "price",
  "sell",
  "market",
  "buy",
  "cost",
  "fee",
  "finance",
  "investment",
  "money",
  "sum",
  "credit",
  "loan",
  "insurance",
  "bank"
livestock
  "livestock",
  "animals",
  "sheep",
  "cattle",
  "donkey",
  "pig",
  "cow",
  "goat",
  "camel",
  "hen",
  "chicken",
  "poultry",
  "lay",
  "egg",
  "milk",
  "breed",
  "dairy",
  "bee"
question
  "who",
  "what",
  "where",
  "when",
  "how",
  "which",
  "many"



