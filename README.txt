About the raw data:
Extract the raw data from zip file after downloading from the source. The datasets have more than 19000 xml files

About the code:
The code should run on Spyder IDE
Before running the code, please remember to choose Spyder setting as the follow option:
Tools > Preferences > Run > Choose > check “Run in console’s namespace instead of an empty one”
This choice will help the code run on default variables created in the pre-processing step

There are 4 scripts corresponding to 4 steps in analysis process.
Due to the large dataset, each step will be slow and spend from 5 to 20 minutes or longer to run:
Step 1: run 1_data_pre_processing.py (modifying the link to folder including the xml files, being just extracted in the above step) 
	this step will be slow because of the pre-processing on 19000 xml files

Step 2: run 2_descriptive_analysis_and_visualize.py

Step 3: run 3_model_clustering_purpose_and_visualize.py

Step 4: run 4_model_sentiment_analysis_and_visualize.py
	this step will be slow due to the scoring process on the original posts