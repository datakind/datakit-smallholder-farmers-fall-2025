# Analyzing Eng Data And Specializing Countries
When i first saw the data i thought it would be better to analyze it in english. I think the other languages are also deserves a good analysis but the data is so big and when we take only eng data it's like half of the whole data.
I think every country must be analyzed specifically i mean if you analyzing all the countries together the statistics may fail so after making the data english i seperated them by countries. I also checked whether question and response countries are same or not and and except small amount of rows in GB they are all same.
(To understand data more quickly i only red 1000 rows of every countries' data)

## first_look() function
This function created to understand the data in more detail and it shows shape,data types,sample rows,unique and missing values

<div align="center">
  <img src="images_from_analysis/dimensions_and_type.png" alt="Shape and Data Types" width="600">
</div>
<div align="center">
  <img src="images_from_analysis/first_row.png" alt="First Row" width="600">
</div>
<div align="center">
  <img src="images_from_analysis/missing_and_unique_values.png" alt="Missing and Unique Values" width="600">
</div>

##
##detailed_missing_value_analysis() 
In order to analyze distribution of missing values in every country i prepared this function and it will also give insights for further dropping and analysis

<div align="center">
  <img src="images_from_analysis/specifi_missing_values_analysis.png" alt="Distribution of Missing Values" width="600">
</div>

##finding_unnecessary_cols()
It's so important to drop unnecessary columns because they may be waste of time, for instance some of the countries have 0 or 1 unique value in their columns and these columns can't give any usable information so we drop them

<div align="center">
  <img src="images_from_analysis/General EDA/YUSUF DOGU/images_from_analysis/drop_unnecessary_cols.png" alt="Filling NaN and Dropping Columns" width="600">
</div>

##making_rows_unique()
as you can see below some rows are same but the only difference is their question and response topics so it shows that if question user choose 3 topics and response user chose 2 different topics there will be 6 rows and it's unnecessary

<p align="center">
  <img src="images_from_analysis/before_making_rows_unique.png" alt="Before Making Every Row Unique" width="45%"/>
  <img src="images_from_analysis/after_making_rows_unique.png" alt="After Making Every Row Unique" width="45%"/>
</p>

<p align="center">
  <b>Before</b> 🡒 <b>After</b>
</p>

Actually this eda was more about having a more clear data to analyze because the data was too big in the beginning so as i continue to analyze i will add more insights and there will be improved version for challenge 5. But for not here you can find more efficient data
