v2 Information:
	
	The code now generates a table at the end with a summary of the response_users with the 20 most responses.

	Code:
		Challenge3_Jesper_v2.ipynb 
		To run the notebook, save the raw dataset as "datakit.csv" in a subfolder titled "Raw_data". The notebook will save the raw dataset into a parquet file, which is much smaller and which can be used in subsequent runs of the notebook.
		
	Dependencies:
		Python 2.7.15
		Jupyter 7.4.5
		pandas 2.3.2
		matplotlib 3.10.6
		pyarrow 22.0.0

	Use of GenAI: I used Claude for help with misc. coding questions, e.g. how to geneate the final summary table. I manually double checked all the results.


v1 Information:

	Goal: Identify community leaders.

	Approach taken here: Identify users who are responding to a lot of questions from a lot of other users.

	Executive summary:
		Identified the 5 response_users who had the most responses, see table below. 
		
<img width="1137" height="189" alt="image" src="https://github.com/user-attachments/assets/ce503605-06b7-48fc-866e-07da6c0b81ae" />

		For each of these users, we also counted the number of users served, and the number of questions responded to.
	
	Code:
		Challenge3_Jesper_v1.ipynb --> Jupyter notebook used to get the results displayed in the table above.
		To run the notebook, save the raw dataset as "datakit.csv" in a subfolder titled "Raw_data".
		
	Dependencies:
		Python 2.7.15
		Jupyter 7.4.5
		pandas 2.3.2
		matplotlib 3.10.6
		
