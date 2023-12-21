## IMPORTANT: For the API to work you need to ensure you have your Kaggle credentials file in your
# /.kaggle folder. If you have no account, I've included my json file which you can move to the
# required folder once the Kaggle package has been installed
# Also ensure to install all packages in requirements.txt

#import pandas and kaggle api to download and read dataset
import pandas as pd
from kaggle.api.kaggle_api_extended import KaggleApi

# Connect to API, ensure the json credentials file is in the correct folder before running
api = KaggleApi()
api.authenticate()

#Extract data
api = KaggleApi()
api.authenticate()
api.dataset_download_files('gauravarora1091/muhammad-ali-boxing-stats', 'muhammad-ali-boxing-stats', unzip='True')

#Load as dataframe
data = pd.read_csv('~/muhammad-ali-boxing-stats/Muhammad Ali Boxing.csv')

#Look at first 5 rows of dataset
data.head(5)

#Check size of dataframe
data.shape

#Checking for null values
data.isna().sum()

#Looking at the rows where Type is null, all related to non-professional (exibition or amateaur). 
data[data['Type'].isnull()]

#Dropping rows where Type is null, as they are not important to official record
clean_data = data.dropna(axis=0, how='any')

#Removing first column as it's a repeat index
clean_data = clean_data.iloc[: , 1:]

#Reviewing if Notes column has relevant information, and it does so will keep this column.
clean_data.Notes.unique()

#Dropping row with the notes Under special boxing-wrestling rules. as it's not a boxing match
clean_data = clean_data[clean_data['Notes'] != 'Under special boxing-wrestling rules.']

#Reviewing results. He had no draws in his professional fights so will remove these rows
clean_data.Result.unique()
clean_data = clean_data[clean_data['Result'] != 'Draw']

#Reviewing losses
losses = clean_data[(clean_data['Result']=='Loss')]
losses

#Removing rows where round contains ? as it's unofficial 
#(all professional boxing matches has a set number of rounds)
clean_data = clean_data[clean_data['Round, time'] != '?']
clean_data = clean_data[clean_data['Round, time'] != '? (2)']

#Our dataframe now only contains the official fights
clean_data.shape

#Before saving, let's ensure all columns have correct data types
clean_data.info()

#Reviewing dates for to_datetime conversion, one row contains full month name and ends in [115] and is causing errors.
clean_data.Date.unique()

#Replacing bad date with correct format 
clean_data["Date"] = clean_data["Date"].str.replace("[115]", "")
clean_data["Date"] = clean_data["Date"].str.replace("July", "Jul")

#Changing Date column to date format
clean_data['Date'] = pd.to_datetime(clean_data['Date'], format='%b %d, %Y')

#Checking data type of all columns
clean_data.info()

#Save to csv for further analysis and visualisations
clean_data.to_csv('Professional Bouts Ali.csv')