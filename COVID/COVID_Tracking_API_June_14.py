#####################################
#Get COVID tracking data through API#
#####################################

#Import python packages
import os
import pandas as pd
import requests
import json
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import matplotlib.dates as mdates
import numpy as np
import datetime as dt


#Set current working directory to fails data folder
print('Current Working Directory' , os.getcwd())
os.chdir('C:/Users/12407/Desktop/Education/Projects/COVID')
print('New Working Directory' , os.getcwd())

#Create state code dictionaries and strings for census data
state_code_dict = {"state":"code","AL":"01","AK":"02","AZ":"04","AR":"05","CA":"06","CO":"08","CT":"09","DE":"10","DC":"11","FL":"12","GA":"13","HI":"15","ID":"16","IL":"17","IN":"18","IA":"19","KS":"20","KY":"21","LA":"22","ME":"23","MD":"24","MA":"25","MI":"26","MN":"27","MS":"28","MO":"29","MT":"30","NE":"31","NV":"32","NH":"33","NJ":"34","NM":"35","NY":"36","NC":"37","ND":"38","OH":"39","OK":"40","OR":"41","PA":"42","RI":"44","SC":"45","SD":"46","TN":"47","TX":"48","UT":"49","VT":"50","VA":"51","WA":"53","WV":"54","WI":"55","WY":"56"}
state_code_string = "01,02,04,05,06,08,09,10,11,12,13,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,44,45,46,47,48,49,50,51,53,54,55,56"
state_code_list = ["01","02","04","05","06","08","09","10","11","12","13","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31","32","33","34","35","36","37","38","39","40","41","42","44","45","46","47","48","49","50","51","53","54","55","56"]
state_list = ["AL","AK","AZ","AR","CA","CO","CT","DE","DC","FL","GA","HI","ID","IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV","WI","WY"]
#state_list = ["AL","AK"]

#Get COVID dataset
url_covid = 'https://covidtracking.com/api/v1/states/daily.json'
response = requests.get(url_covid)
formattedResponse = json.loads(response.text)[1:]
df_covid = pd.DataFrame(formattedResponse)

#Get census pop dataset 
apiKey = 'c04ab30e3be5b31ad7772fa15ad226d93cf1fa4b'
response = requests.get('https://api.census.gov/data/2019/pep/population?get=POP&for=state:'
                         +state_code_string+'&key='+apiKey)
formattedResponse = json.loads(response.text)
df_pop = pd.DataFrame(formattedResponse)
new_header = df_pop.iloc[0] #grab the first row for the header
df_pop = df_pop[1:] #take the data less the header row
df_pop.columns = new_header #set the header row as the df header
df_pop = df_pop.rename(columns={"state": "code"})

#Assign state abbreviations to pop dataset and merge with COVID dataset
state_code_df = pd.DataFrame.from_dict(state_code_dict, orient='index')
new_header = state_code_df.iloc[0] #grab the first row for the header
state_code_df = state_code_df[1:] #take the data less the header row
state_code_df.columns = new_header #set the header row as the df header
state_code_df['state'] = state_code_df.index
state_pop = pd.merge(df_pop, state_code_df, how='inner', on='code')
#state_pop = state_pop.drop(columns=['code'])
state_pop['POP'] = state_pop['POP'].astype(int)
df = pd.merge(df_covid, state_pop, how='left', on='state')
         
#Calculate variables of interest
df['Negative_Pct'] = (df['negativeIncrease']) / df['POP'] * 100
df['Positive_Pct'] = (df['positiveIncrease']) / df['POP'] * 100
df['Death_Pct'] = (df['deathIncrease']) / df['POP'] * 100
df['Hospitalized_Pct'] = (df['hospitalizedIncrease']) / df['POP'] * 100

#Set stateID
stateID = 'MD'

#Create charts
for stateID in state_list:
    state_df = df[['date','state','Positive_Pct','Negative_Pct','Death_Pct','Hospitalized_Pct']]
    state_df = state_df[state_df['state']==stateID] 
    state_df['date'] = state_df['date'].astype(str)
    state_df['date'] = (state_df['date'].str[0:4:1] + '-' + state_df['date'].str[4:6:1] + '-' + state_df['date'].str[6:8:1])
    date_list = state_df['date'].astype('str')
    dates = [dt.datetime.strptime(d,'%Y-%m-%d').date() for d in date_list]
    fig, (ax1, ax2) = plt.subplots(2, 1)
    #ax1 - negative and postive percent stack chart
    positive_rates = state_df['Positive_Pct'].astype('float')
    negative_rates = state_df['Negative_Pct'].astype('float')
    labels = ['Positive (%)', 'Negative (%)']
    ax1.stackplot(dates, positive_rates, negative_rates, labels=labels)
    ax1.legend(loc='upper left')
    months = mdates.MonthLocator()
    months_fmt = mdates.DateFormatter('%b')
    ax1.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=1))
    ax1.xaxis.set_major_locator(months)
    ax1.xaxis.set_major_formatter(months_fmt)
    ax1.set_ylim(bottom=0.)
    ax1.grid(True)
    #ax1.ylim(0, 0.4)
    #ax2 - deaths and hospitalizations percent stack chart
    death_rates = state_df['Death_Pct'].astype('float')
    hospitalized_rates = state_df['Hospitalized_Pct'].astype('float')
    labels = ['Deaths (%)', 'Hospitalized (%)']
    ax2.plot(dates, death_rates, label='Deaths')
    ax2.plot(dates, hospitalized_rates, label='Hospitalizations')
    #ax2.plot(dates, death_rates, dates, hospitalized_rates)
    months = mdates.MonthLocator()
    months_fmt = mdates.DateFormatter('%b')
    ax2.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=3))
    ax2.xaxis.set_major_locator(months)
    ax2.xaxis.set_major_formatter(months_fmt)
    ax2.set_ylim(bottom=0.)
    ax2.legend(loc='upper left')
    ax2.grid(True)
    #ax2.ylim(0, 0.02)
    plt.savefig('positive_negative_pct_' + stateID + '.png', format='png', bbox_inches='tight')
    plt.close()