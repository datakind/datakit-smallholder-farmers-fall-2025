# Imports


```python
import pandas as pd
import numpy as np
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple
import warnings
from matplotlib import pyplot as plt
import seaborn as sns
warnings.filterwarnings('ignore')

# Custom library
import WeFarmPy
```

# Load data data
Note that for most personal computers, playing around with the full 6 GB raw csv data is going to be slow and cumbersome.

Recommend for exploratory work to load a subset; converting to parquet will also make subsequent loads much faster.

### Raw data


```python
# Full filepath
fpath_raw = r'/Users/georgelewis/Desktop/Datakind farmer project/raw_data.csv'
```


```python
### Load subset for playing around / increase responsiveness

# # Read only N rows randomly distributed throughout file
# sample_size = 1500000  # 1.5M rows ~300MB in memory

# # Calculate skip probability to get uniform sample
# total_rows = 20304843  # Full dataset
# skip_prob = 1 - (sample_size / total_rows)

# # Load
# np.random.seed(1)
# df_sample = pd.read_csv(
#     fpath_raw,
#     skiprows=lambda i: i > 0 and np.random.random() > skip_prob,
#     nrows=sample_size  # Safety limit
# )

# # Check there are responses from ke/ug/tz (tz counts are very low)
# df_sample['question_user_country_code'].value_counts()
```


```python
### Otherwise load the full dataset (much slower)
df_sample = pd.read_csv(fpath_raw)
```

### Process data
- Ensures datetime columns load correctly
- Standardises country codes and language names
- Adds data completeness info
- Adds temporal data
- Adds season category


```python
processor = WeFarmPy.DataCleaning()
df_sample_clean = processor.process(df_sample)

df_sample_clean
```

    Starting data processing pipeline on 20,304,843 rows...
    ================================================================================
    Parsing datetime columns...
      question_sent:
        Valid: 20,304,843 | Null: 0
        Range: 2017-11-22 12:25:03+00:00 to 2022-06-21 14:31:25.474665+00:00
      response_sent:
        Valid: 20,304,843 | Null: 0
        Range: 2017-11-22 12:28:03+00:00 to 2022-07-07 14:12:45.369580+00:00
      question_user_dob:
        Valid: 1,231,284 | Null: 19,073,559
        Range: 1917-01-13 00:00:00+00:00 to 2020-09-23 00:00:00+00:00
      question_user_created_at:
        Valid: 20,304,843 | Null: 0
        Range: 2014-11-27 15:06:11+00:00 to 2022-04-07 08:05:37.297909+00:00
      response_user_dob:
        Valid: 1,664,688 | Null: 18,640,155
        Range: 1916-02-07 00:00:00+00:00 to 2020-09-23 00:00:00+00:00
      response_user_created_at:
        Valid: 20,304,843 | Null: 0
        Range: 2014-11-27 15:06:11+00:00 to 2022-04-06 04:48:37.656557+00:00
    Standardizing country codes to ISO 3166-1 alpha-3...
      question_user_country_code:
        Before: {'ke': 9758607, 'ug': 6312194, 'tz': 4233726, 'gb': 316}
        After:  {'KEN': 9758607, 'UGA': 6312194, 'TZA': 4233726, 'gb': 316}
      response_user_country_code:
        Before: {'ke': 9769748, 'ug': 6312194, 'tz': 4222579, 'gb': 322}
        After:  {'KEN': 9769748, 'UGA': 6312194, 'TZA': 4222579, 'gb': 322}
    Adding language names...
      question_language -> question_language_name
      response_language -> response_language_name
    Extracting temporal features...
      Added temporal features for questions
      Added temporal features for responses
        Response time: median=0.3h, mean=117.9h
    Adding farming season context...
      Farming season distribution:
        short_rains: 3,153,046
        harvest_1: 2,333,749
        long_rains: 2,267,444
        season_b_plant: 1,977,217
        off_season: 1,874,166
      Standardized seasons:
        rainy_secondary: 6,255,017
        rainy_main: 4,939,511
        harvest_main: 4,910,780
        harvest_secondary: 2,325,053
        off_season: 1,874,482
    Extracting text features...
      Question length: median=55 chars, mean=63 chars
      Response length: median=34 chars, mean=49 chars
    Computing data completeness metrics...
      Core fields completeness: 100.0% avg
      User metadata completeness: 5.5% avg
    ================================================================================
    Processing complete! Output: 20,304,515 rows, 51 columns (+27 added)





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>q_id</th>
      <th>q_user_id</th>
      <th>q_lang_code</th>
      <th>q_text</th>
      <th>q_topic</th>
      <th>q_datetime</th>
      <th>r_id</th>
      <th>r_user_id</th>
      <th>r_lang_code</th>
      <th>r_text</th>
      <th>...</th>
      <th>season</th>
      <th>season_std</th>
      <th>q_chars</th>
      <th>q_words</th>
      <th>r_chars</th>
      <th>r_words</th>
      <th>completeness_pct</th>
      <th>metadata_pct</th>
      <th>has_q_topic</th>
      <th>has_r_topic</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>3849056</td>
      <td>519124</td>
      <td>nyn</td>
      <td>E ABA WEFARM OFFICES ZABO NIZISHANGWA NKAHI?</td>
      <td>NaN</td>
      <td>2017-11-22 12:25:03+00:00</td>
      <td>20691011</td>
      <td>200868</td>
      <td>nyn</td>
      <td>E!23 Omubazi Ni Dudu Cipa'</td>
      <td>...</td>
      <td>season_b_plant</td>
      <td>rainy_secondary</td>
      <td>44</td>
      <td>7</td>
      <td>26</td>
      <td>5</td>
      <td>100.0</td>
      <td>0.0</td>
      <td>False</td>
      <td>False</td>
    </tr>
    <tr>
      <th>1</th>
      <td>3849061</td>
      <td>521327</td>
      <td>eng</td>
      <td>Q this goes to wefarm. is it possible to get f...</td>
      <td>NaN</td>
      <td>2017-11-22 12:25:05+00:00</td>
      <td>4334249</td>
      <td>526113</td>
      <td>eng</td>
      <td>Q1 which stage is marleks last vaccinated</td>
      <td>...</td>
      <td>season_b_plant</td>
      <td>rainy_secondary</td>
      <td>80</td>
      <td>17</td>
      <td>41</td>
      <td>7</td>
      <td>100.0</td>
      <td>0.0</td>
      <td>False</td>
      <td>False</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3849077</td>
      <td>307821</td>
      <td>nyn</td>
      <td>E ENTE YANJE EZAIRE ENYENA YASHOBERA. \nOBWIRE...</td>
      <td>cattle</td>
      <td>2017-11-22 12:25:08+00:00</td>
      <td>3849291</td>
      <td>296187</td>
      <td>nyn</td>
      <td>Muhanguzi.Benon kuruga masha isingiro ente yaw...</td>
      <td>...</td>
      <td>season_b_plant</td>
      <td>rainy_secondary</td>
      <td>160</td>
      <td>21</td>
      <td>117</td>
      <td>14</td>
      <td>100.0</td>
      <td>0.0</td>
      <td>True</td>
      <td>True</td>
    </tr>
    <tr>
      <th>3</th>
      <td>3849077</td>
      <td>307821</td>
      <td>nyn</td>
      <td>E ENTE YANJE EZAIRE ENYENA YASHOBERA. \nOBWIRE...</td>
      <td>cattle</td>
      <td>2017-11-22 12:25:08+00:00</td>
      <td>3849291</td>
      <td>296187</td>
      <td>nyn</td>
      <td>Muhanguzi.Benon kuruga masha isingiro ente yaw...</td>
      <td>...</td>
      <td>season_b_plant</td>
      <td>rainy_secondary</td>
      <td>160</td>
      <td>21</td>
      <td>117</td>
      <td>14</td>
      <td>100.0</td>
      <td>0.0</td>
      <td>True</td>
      <td>True</td>
    </tr>
    <tr>
      <th>4</th>
      <td>3849077</td>
      <td>307821</td>
      <td>nyn</td>
      <td>E ENTE YANJE EZAIRE ENYENA YASHOBERA. \nOBWIRE...</td>
      <td>cat</td>
      <td>2017-11-22 12:25:08+00:00</td>
      <td>3849291</td>
      <td>296187</td>
      <td>nyn</td>
      <td>Muhanguzi.Benon kuruga masha isingiro ente yaw...</td>
      <td>...</td>
      <td>season_b_plant</td>
      <td>rainy_secondary</td>
      <td>160</td>
      <td>21</td>
      <td>117</td>
      <td>14</td>
      <td>100.0</td>
      <td>0.0</td>
      <td>True</td>
      <td>True</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>20304838</th>
      <td>59258899</td>
      <td>3684299</td>
      <td>swa</td>
      <td>Naomba,mbegu ya mahindi..nmeishiwa kabisa na s...</td>
      <td>maize</td>
      <td>2022-05-09 11:46:22.464727+00:00</td>
      <td>59258905</td>
      <td>2500216</td>
      <td>eng</td>
      <td>Apply only deficient nutrients for maize and c...</td>
      <td>...</td>
      <td>long_rains</td>
      <td>rainy_main</td>
      <td>58</td>
      <td>7</td>
      <td>128</td>
      <td>16</td>
      <td>100.0</td>
      <td>0.0</td>
      <td>True</td>
      <td>True</td>
    </tr>
    <tr>
      <th>20304839</th>
      <td>59259045</td>
      <td>2772369</td>
      <td>eng</td>
      <td>I want to grow cabbage someone to give me the ...</td>
      <td>cabbage</td>
      <td>2022-05-12 11:30:05.749550+00:00</td>
      <td>59259053</td>
      <td>3681140</td>
      <td>eng</td>
      <td>1</td>
      <td>...</td>
      <td>long_rains</td>
      <td>rainy_main</td>
      <td>64</td>
      <td>12</td>
      <td>1</td>
      <td>1</td>
      <td>100.0</td>
      <td>0.0</td>
      <td>True</td>
      <td>False</td>
    </tr>
    <tr>
      <th>20304840</th>
      <td>59260982</td>
      <td>110220</td>
      <td>eng</td>
      <td>Q how can i permanently control birds destroyi...</td>
      <td>maize</td>
      <td>2022-06-11 11:52:34.447200+00:00</td>
      <td>59261028</td>
      <td>1493318</td>
      <td>eng</td>
      <td>Open the forum as soon as possible</td>
      <td>...</td>
      <td>harvest_1</td>
      <td>harvest_main</td>
      <td>67</td>
      <td>12</td>
      <td>34</td>
      <td>7</td>
      <td>100.0</td>
      <td>50.0</td>
      <td>True</td>
      <td>False</td>
    </tr>
    <tr>
      <th>20304841</th>
      <td>59260982</td>
      <td>110220</td>
      <td>eng</td>
      <td>Q how can i permanently control birds destroyi...</td>
      <td>bird</td>
      <td>2022-06-11 11:52:34.447200+00:00</td>
      <td>59261028</td>
      <td>1493318</td>
      <td>eng</td>
      <td>Open the forum as soon as possible</td>
      <td>...</td>
      <td>harvest_1</td>
      <td>harvest_main</td>
      <td>67</td>
      <td>12</td>
      <td>34</td>
      <td>7</td>
      <td>100.0</td>
      <td>50.0</td>
      <td>True</td>
      <td>False</td>
    </tr>
    <tr>
      <th>20304842</th>
      <td>59261512</td>
      <td>3735072</td>
      <td>eng</td>
      <td>Q. Which is the best Season of dlanting tomato</td>
      <td>tomato</td>
      <td>2022-06-21 14:31:25.474665+00:00</td>
      <td>59261534</td>
      <td>1493318</td>
      <td>eng</td>
      <td>Bw. We farm, tell us where to head. Are you in...</td>
      <td>...</td>
      <td>harvest_1</td>
      <td>harvest_main</td>
      <td>46</td>
      <td>9</td>
      <td>60</td>
      <td>13</td>
      <td>100.0</td>
      <td>0.0</td>
      <td>True</td>
      <td>False</td>
    </tr>
  </tbody>
</table>
<p>20304515 rows × 51 columns</p>
</div>



# Time analysis


```python
fig = WeFarmPy.EDA.plot_temporal_overview(df_sample_clean)
```


    
![png](output_files/output_10_0.png)
    


- Questions appear to peak August to November, being lowest at the start of the calendar year.
- Average response time appears to be quite fast (under 1 hr)! The tail-end of responses shows some questions took 10s of days to answer - could be interesting to dig into these 'difficult' questions?
- Intersting that weekday evenings appear to be most popular engagement time (straight after finishing work?) - as opposed to perhaps asking as things happen during the day, or reflecting on work at weekends. (Note hour of day has been converted back into local timezones)

# Geography analysis


```python
fig = WeFarmPy.EDA.plot_geographic_overview(df_sample_clean)
```

    Looks like you are using a tranform that doesn't support FancyArrowPatch, using ax.annotate instead. The arrows might strike through texts. Increasing shrinkA in arrowprops might help.



    
![png](output_files/output_13_1.png)
    


- Filtered out country code 'gb' - are these tests sent from the UK? V. small % of responses
- There are fewer questions coming from Tanzania (presumably WeFarm had a lower presence there?)
- Seems that on average, a greater % of questions are asked in the rainy seasons than the harvest seasons, thgouh in Tanzania, roughly 1/5th of all questions were asked 'off-season'.
- There is a fair bit of overlap in question categories. between countires - chicken and maize are two of the most common topics in all three countries. Cattle feature much more in Kenya than other countries.

# Language analysis


```python
fig = WeFarmPy.EDA.plot_linguistic_overview(df_sample_clean)
```


    
![png](output_files/output_16_0.png)
    


- Almost 60% of all answers are in English
- All Tanzanian and some Kenyan responses are in Swahili
- Ugandan has ~20% of its responses in Runyankore, and ~10% in Luganda
- 95% of questions are answered in the same language

# User analysis


```python
fig = WeFarmPy.EDA.plot_user_overview(df_sample_clean)
```


    
![png](output_files/output_19_0.png)
    


- Most users (~80%) are male
- Very little correlation between question length and response length, average is about 50 characters
- Most users about 40 years old
- The average user sent 5 to 20 questions, though there were also some very active users (>10000 questions each)


# Data quality


```python
fig = WeFarmPy.EDA.plot_data_quality(df_sample_clean)
```


    
![png](output_files/output_22_0.png)
    


- All questions have basic 'core' fields (question, response, time, country)
- User metadata appears to be some of the most lacking fields - >80% are missing gender and DOB.
