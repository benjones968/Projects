## Inspired by: 
### https://towardsdatascience.com/google-trends-api-for-python-a84bc25db88f
### https://github.com/GeneralMills/pytrends#installation
### https://medium.com/intro-to-python-wows/google-trends-4db836214868

## Note: Does not work on anaconda, only regular python

#Import packages. Note that pytrends will likely need to be installed, and I wasn't successful in installing it on anaconda.
import pandas as pd
from pytrends.request import TrendReq
import os

#Create cluster data for a specific key word. In this case "Coronavirus"
key_word = 'Coronavirus'
os.chdir('C:/Users/12407/Desktop/Education/Projects/Google_Trends')
pytrend = TrendReq(geo='US')
pytrend.build_payload(kw_list=[key_word])
related_queries = pytrend.related_queries()
df_rq = list(related_queries.get(key_word).values())[0]
data = {'State_Name':[
	'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'District of Columbia', 'Florida', 
	'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 
	'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 
	'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 
	'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming'
]}
data = pd.DataFrame(data) 
data = data.set_index('State_Name')
for ind in df_rq.index: 
	pytrend = TrendReq(geo='US')
	pytrend.build_payload(kw_list=[df_rq['query'][ind]])
	df = pytrend.interest_by_region(resolution='REGION', inc_low_vol=False, inc_geo_code=False)
	data = data.merge(df, left_index=True, right_index=True)
	print('loop index: ' + str(ind+1))
data.to_csv('cluster_data.csv')
















	#print(df.head())
	#print(type(df))


#print(type(df_rq))
#print(list(df_rq.columns))
#df_rq = df_rq.drop(df_rq.index[2:])
#for ind in df_rq.index: 
#     print(df_rq['query'][ind]) 


#data.to_csv('file_name0.csv')
#data = data.merge(df, left_index=True, right_index=True)



#print(np(df_rq.iloc[:,0].values))
#print(type(related_queries))
#data = list(related_queries.values())
#print(type(data))
#print(data)
# Interest by Region
#pytrends.interest_by_region(resolution='COUNTRY', inc_low_vol=True, inc_geo_code=False)
#df = pytrend.interest_by_region(resolution='REGION', inc_low_vol=False, inc_geo_code=False)
#print(df.head())
#df = pytrend.trending_searches(pn='united_states')
#print(df.head())


