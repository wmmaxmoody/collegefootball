# -*- coding: utf-8 -*-
"""
Created on Thu Feb  2 12:10:39 2023

@author: wmmax
"""
#Requests to grab the data, json to convert from JSON, pprint to test, and pandas to get to excel
import requests
import json
import pprint
import pandas as pd

output = r"C:\Football Analysis\4 Year Stats Database.xlsx"

# Set base year
base_year = 2022
num_of_years = 4

# Set the headers to access the CFBD API
headers = {"accept": "application/json",
           "Authorization":"bearer iQ9gBDZVfji6VbY5HouFgdPq86iY8skNEmFZb8CXAd8Et0scQPOtbOq4JmS5hKhV"}

# Set base ISS URL
ISS_URL = 'https://api.collegefootballdata.com/stats/player/season'

# Set params for each year
params_list = [{'year': base_year - i, 'startWeek':1, 'endWeek':16} for i in range(num_of_years)]

# List to store dataframes for each year
ISS_list = []

for params in params_list:
    # Get data from each year and transform to a dataframe 
    Indv_season_stats = requests.get(ISS_URL,params=params,headers=headers)
    ISS_data = json.loads(Indv_season_stats.text)
    ISS = pd.DataFrame(ISS_data)
    ISS.columns = list(ISS_data[0].keys())
    ISS.insert(0, "Season", params['year'])
    ISS.insert(1,"Team/Individual",'Individual')
    ISS['stat'] = ISS['stat'].astype(float)
    ISS = ISS[ISS['stat']!=0]
    ISS_list.append(ISS)

# Concat all ISS data frames
ISS = pd.concat(ISS_list)

#drop rows equal to 0
#ISS['stat']=ISS['stat'].astype(float)
#ISS = ISS[ISS['stat'] !=0]

#Go to next category

# Set base TSS URL
TSS_URL = 'https://api.collegefootballdata.com/stats/season'

# Set params for each year
params_list = [{'year': base_year - i, 'startWeek':1, 'endWeek':16} for i in range(num_of_years)]

# List to store dataframes for each year
TSS_list = []

for params in params_list:
    # Get data from each year and transform to a dataframe 
    Indv_season_stats = requests.get(TSS_URL,params=params,headers=headers)
    TSS_data = json.loads(Indv_season_stats.text)
    TSS = pd.DataFrame(TSS_data)
    TSS.columns = list(TSS_data[0].keys())
    TSS.insert(0, "Season", params['year'])
    TSS.insert(1,"Team/Individual",'Team')
    TSS_list.append(TSS)

# Concat all TSS data frames
TSS = pd.concat(TSS_list)

#drop rows equal to 0
TSS['statValue']=TSS['statValue'].astype(float)
TSS = TSS[TSS['statValue'] !=0]

#filter to FSU
FSU_ISS = ISS.drop(index=ISS[ISS['team']!= "Florida State"].index)
# Create an Excel writer object and define each sheet
with pd.ExcelWriter(output,engine="xlsxwriter") as writer:
    ISS.to_excel(writer, sheet_name='Individual Season Stats')
    TSS.to_excel(writer, sheet_name='Team Season Stats')
    FSU_ISS.to_excel(writer, sheet_name='FSU Ind Season Stats')   
    
    
# Save the Excel workbook
writer.save()
writer.close()