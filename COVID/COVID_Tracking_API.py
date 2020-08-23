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
state_pop = state_pop.drop(columns=['code'])
state_pop['POP'] = state_pop['POP'].astype(int)
df = pd.merge(df_covid, state_pop, how='left', on='state')
         
#Calculate variables of interest
df['Posivity_Rate'] = df['positiveIncrease'] / (df['negativeIncrease'] + df['positiveIncrease'])*100
df['Negative_Pct'] = (df['negativeIncrease']) / df['POP'] * 100
df['Positive_Pct'] = (df['positiveIncrease']) / df['POP'] * 100


#Set stateID
stateID = 'MD'

#Get negative and postive percent stack charts
state_df = df[['date','state','Positive_Pct','Negative_Pct']]
state_df = state_df[state_df['state']==stateID] 
state_df['date'] = state_df['date'].astype(str)
state_df['date'] = (state_df['date'].str[0:4:1] + '-' + state_df['date'].str[4:6:1] + '-' + state_df['date'].str[6:8:1])
positive_rates = state_df['Positive_Pct'].astype('float')
negative_rates = state_df['Negative_Pct'].astype('float')
date_list = state_df['date'].astype('str')
dates = [dt.datetime.strptime(d,'%Y-%m-%d').date() for d in date_list]
fig, (ax1, ax2) = plt.subplots(2, 1)
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





plt.savefig('posive_negative_pct_' + stateID + '.png', format='png', bbox_inches='tight')
plt.close()




positive_rate_list = state_df['Positive_Pct'].tolist()
negative_rate_list = state_df['Negative_Pct'].tolist()
labels = ["Positive (%)", "Negative (%)"]



plt.savefig('posivity_rate_' + stateID + '.png', format='png', bbox_inches='tight')
plt.close()


#Get positivity rate charts
state_df = df[['date','state','Positivity_Rate']]
state_df = state_df[state_df['state']==stateID] 
state_df['date'] = pd.to_datetime(state_df['date'], format='%Y%m%d')

months = mdates.MonthLocator()
months_fmt = mdates.DateFormatter('%b')

state_df = state_df.sort_values(by=['date'])
state_df['Positivity_Rate_SMA_7'] = state_df.iloc[:,2].rolling(window=7).mean()
fig, (ax1, ax2) = plt.subplots(2, 1)
fig.subplots_adjust(hspace=0.5)

ax1.plot(state_df['date'], state_df['Positivity_Rate'], state_df['date'], state_df['Positivity_Rate_SMA_7'])
#ax1.set_xlim(0, 5)
ax1.yaxis.set_major_formatter(mtick.PercentFormatter())
ax1.xaxis.set_major_locator(months)
ax1.xaxis.set_major_formatter(months_fmt)
#ax1.set_xlabel('Month')
ax1.set_ylabel('Positivity Rate (%)')
ax1.set_yticks((10, 25, 50)) 
ax1.grid(True)
plt.savefig('posivity_rate_' + stateID + '.png', format='png', bbox_inches='tight')
plt.close()





state_df = state_df[state_df['state']==stateID] 
state_df['date'] = pd.to_datetime(state_df['date'], format='%Y%m%d')
state_df = state_df.sort_values(by=['date'])
state_df['Positivity_Rate_SMA_7'] = state_df.iloc[:,2].rolling(window=7).mean()
plt.plot('date', 'Positivity_Rate', data=state_df, marker='', color='skyblue', linewidth=1)
plt.plot('date', 'Positivity_Rate_SMA_7', data=state_df, marker='', color='black', linewidth=4)
plt.legend()
plt.title('Positivity rate for ' + stateID)
plt.xlabel('Date')
plt.ylabel('Positivity Rate')
plt.ylim(0, 0.5)
plt.grid(True)
plt.savefig('posivity_rate_' + stateID + '.png', format='png', bbox_inches='tight')
plt.close()

#Get Testing rate charts
state_df = df[['date','state','Testing_Rate']]
state_df = state_df[state_df['state']==stateID] 
state_df['date'] = pd.to_datetime(state_df['date'], format='%Y%m%d')
state_df = state_df.sort_values(by=['date'])
state_df['Testing_Rate_SMA_7'] = state_df.iloc[:,2].rolling(window=7).mean()
plt.plot('date', 'Testing_Rate', data=state_df, marker='', color='skyblue', linewidth=1)
plt.plot('date', 'Testing_Rate_SMA_7', data=state_df, marker='', color='black', linewidth=4)
plt.legend()
plt.title('Testing rate for ' + stateID)
plt.xlabel('Date')
plt.ylabel('Testing Rate')

plt.grid(True)
plt.savefig('testing_rate_' + stateID + '.png', format='png', bbox_inches='tight')
plt.close()


x = [1, 2, 3, 4, 5]
y1 = [1, 1, 2, 3, 5]
y2 = [0, 4, 2, 6, 8]
y3 = [1, 3, 5, 7, 9]

y = np.vstack([y1, y2, y3])

labels = ["Fibonacci ", "Evens", "Odds"]

fig, ax = plt.subplots()
ax.stackplot(x, y1, y2, y3, labels=labels)
ax.legend(loc='upper left')
plt.show()



##CaLculate positivity rate and filter
#df['Positivity_Rate'] = df['positiveIncrease'] / (df['negativeIncrease'] + df['positiveIncrease'])
#df = df[['date','state','Positivity_Rate']]


##Generate graph for each state
#state_list = df['state'].tolist()
#for stateID in state_list:
#    state_df = df[df['state']==stateID] 
#    state_df['date'] = pd.to_datetime(state_df['date'], format='%Y%m%d')
#    state_df = state_df.sort_values(by=['date'])
#    state_df['Positivity_Rate_SMA_7'] = state_df.iloc[:,2].rolling(window=7).mean()
#    plt.plot('date', 'Positivity_Rate', data=state_df, marker='', color='skyblue', linewidth=1)
#    plt.plot('date', 'Positivity_Rate_SMA_7', data=state_df, marker='', color='black', linewidth=4)
#    plt.legend()
#    plt.title('Positivity rate for ' + stateID)
#    plt.xlabel('Date')
#    plt.ylabel('Positivity Rate')
#    plt.ylim(0, 0.5)
#    plt.grid(True)
#    plt.savefig('posivity_rate_' + stateID + '.png', format='png', bbox_inches='tight')
#    plt.close()



