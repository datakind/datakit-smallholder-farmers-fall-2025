# Overview
I attempted Challenge #2 - Seasonality. My goal was to find whether there
was correlation between the frequency of specific question topics asked during the
year and the planting and harvesting seasons for Kenya and Uganda.

## Dataset Used
eng_data.csv was created by a volunteer (Bashir), and is an English only version of the original Producer's Direct-WeFarm Dataset. It is available on slack in the challenge0-translation channel.

---

# Approach

### Importing Libraries & Data
1) Imported necessary libraries  
   - Pandas  
   - Numpy  
   - Seaborn  
   - Matplotlib.pyplot  
   - Duckdb

2) Converted the data from a csv file into a parquet file, drastically reducing run  
   times.  
   - Used Duckdb to convert the csv into parquet.

### Initial Exploration
1) Got a cursory understanding of the different columns featured in the dataset.  
   What might be useful, what might not.  
2) Read the initial EDA’s of other submissions to get a better understanding of the  
   data, and what avenues might be worth pursuing.  
3) Useful Columns:  
   - question_topic - had a description of what the question was about,
        usually a one-word description(apple, pig, wheat, etc.).  
   - question_language - I was only confident working with questions/topics
        in english.  
   - question_sent - date-time; best approximation of when the user had the
        particular problem compared to the time of the answer being sent.  
   - question_user_country - necessary in order to separate analyses for
        different locations.

### Data Cleaning
1) Question_topic  
   - Was found to have 748 unique values. A quick glance at some of the  
        longer strings made it evident that there were many non-topic strings  
        (dates, questions, etc). Most actual topics were described in one word.  
   - Removed all rows where question_topic was more  
        than one word.  
   - Some random punctuation and quotations were causing for there to be  
        repeats, for example: (‘wheat’ and ‘“”wheat””’). Stripped the punctations,  
        quotations, and any numerical values (to remove dates that had been  
        counted as one word).  
   - Although we were now down to a much cleaner set of unique values in  
        question_topic there were still some clearly non-topic values. Because  
        the values were far more manageable, I removed them manually  
        to ensure accuracy.  
   - Removed all the rows that had the irrelevant values mentioned above.


### Categorization
I used an LLM to help sort the actual topics into broader categories:

1) Livestock - (pig, cattle, goat, sheep, etc.)  
2) Poultry - (chicken, turkey, guinea-fowl, etc.)  
3) Fish - (fish, tilapia)  
4) Fodder - (grass, rye, oat, napier-grass, etc.)  
5) Tree - (mango, paw-paw, avocado, bamboo, etc.)  
6) Crop_generic - (crop)  
7) Crop_legume - (bean, chickpea, soya, etc.)  
8) Crop_tuber - (potato, cassava, taro, yam, etc.)  
9) Crop_vegetable - (cauliflower, squash, cabbage, spinach, capsicum, etc.)  
10) Crop_fruit - (watermelon, pineapple, strawberry, tomato, etc.)  
11) Crop_spiceherb - (garlic, ginger, coriander, etc.)  
12) Crop_oil - (sunflower, rapeseed, sesame, castor-bean)  
13) Crop_cash - (cotton, tobacco, coffee, cocoa, sugar-cane)  
14) Pest - (locust)

Created a topic_group column, and deleted any row that returned as uncategorized. I
also removed all rows for which we didn’t have question_sent data for.

### Time
1) Created three time columns based on question_sent data.  
   - month  
   - year  
   - Month_year  

The data in this english-question dataset was from February 2018 till June 2022.

### Line-Charts
I aggregated the data across the entire 4-ish years to help show the general pattern from
month-to-month. I also grouped different topic_groups based on relevancy to be on the
same chart. And separate charts were made for Kenya and Uganda. Below are my
outputs:

#### Kenya Charts

![crop_related_kenya](images/crop_related_kenya.png)
![animal_related_kenya](images/animal_related_kenya.png)
![fodder_pest_kenya](images/fodder_pest_kenya.png)
![tree_related_kenya](images/tree_related_kenya.png)

#### Uganda Charts
![crop_related_uganda](images/crop_related_uganda.png)
![animal_related_uganda](images/animal_related_uganda.png)
![fodder_pest_uganda](images/fodder_pest_uganda.png)
![tree_related_uganda](images/tree_related_uganda.png)

---

# Insight
- Kenya had a more active user base in terms of the total number of questions  
  asked in English  
- Some topics like fish, spices & herbs, and pests were rarely asked about.  
- The end of the year, November and December, typically had a huge peak in  
  numbers of questions asked.  
- Crop-related questions peaked during planting seasons in Uganda and Kenya.

---

# LLM-Use Acknowledgement
  I used an LLM to categorize topics, help with coding errors, and help with  
  producing graphs.

---

# Further Analysis
- Using NLP to analyze the actual question to give us topics with added detail  
  would be extremely beneficial. All we know about this data through  
  question_topic is that a question was asked about a certain thing (crop or a fruit  
  or an animal), but not specifically what the issue was (when to harvest, when to  
  plant, issues with growth, disease, weather etc.)  
- Drilling down and exploring specific years and months.
