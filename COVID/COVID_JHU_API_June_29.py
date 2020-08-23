################################
#Get COVID JHU data through API#
################################

#Import python packages
import os
import pandas as pd
import requests
import csv
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import matplotlib.dates as mdates

#Set current working directory to fails data folder
print('Current Working Directory' , os.getcwd())
os.chdir('C:/Users/12407/Desktop/Education/Projects/COVID/Graphs_CJ')
print('New Working Directory' , os.getcwd())

#Bring in population data obtained from World Bank
country_pop_dict = {"country": "population","Afghanistan": "37172390","Albania": "2866380","Algeria": "42228430","Andorra": "77010","Angola": "30809760","Antigua and Barbuda": "96290","Argentina": "44494500","Armenia": "2951780","Australia": "24982690","Austria": "8840520","Azerbaijan": "9939800","Bahamas": "385640","Bahrain": "1569440","Bangladesh": "161356040","Barbados": "286640","Belarus": "9483500","Belgium": "11433260","Belize": "383070","Benin": "11485050","Bhutan": "754390","Bolivia": "11353140","Bosnia and Herzegovina": "3323930","Botswana": "2254130","Brazil": "209469330","Brunei": "428960","Bulgaria": "7025040","Burkina Faso": "19751530","Burundi": "11175380","Cabo Verde": "543770","Cambodia": "16249800","Cameroon": "25216240","Canada": "37057760","Central African Republic": "4666380","Chad": "15477750","Chile": "18729160","China": "1392730000","Colombia": "49648680","Comoros": "832320","Congo (Kinshasa)": "84068090","Congo (Brazzaville)": "5244360","Costa Rica": "4999440","Cote d'Ivoire": "25069230","Croatia": "4087840","Cuba": "11338140","Cyprus": "1189270","Czechia": "10629930","Denmark": "5793640","Djibouti": "958920","Dominica": "71630","Dominican Republic": "10627170","Ecuador": "17084360","Egypt": "98423600","El Salvador": "6420740","Equatorial Guinea": "1308970","Eritrea": "3213970","Estonia": "1321980","Eswatini": "1136190","Ethiopia": "109224560","Fiji": "883480","Finland": "5515520","France": "66977110","Gabon": "2119280","Gambia": "2280100","Georgia": "3726550","Germany": "82905780","Ghana": "29767110","Greece": "10731730","Grenada": "111450","Guatemala": "17247810","Guinea": "12414320","Guinea-Bissau": "1874310","Guyana": "779000","Haiti": "11123180","Honduras": "9587520","Hungary": "9775560","Iceland": "352720","India": "1352617330","Indonesia": "267663430","Iran": "81800270","Iraq": "38433600","Ireland": "4867310","Israel": "8882800","Italy": "60421760","Jamaica": "2934860","Japan": "126529100","Jordan": "9956010","Kazakhstan": "18272430","Kenya": "51393010","Korea, South": "51606630","Kosovo": "1845300","Kuwait": "4137310","Kyrgyzstan": "6322800","Laos": "7061510","Latvia": "1927170","Lebanon": "6848930","Lesotho": "2108130","Liberia": "4818980","Libya": "6678570","Liechtenstein": "37910","Lithuania": "2801540","Luxembourg": "607950","Madagascar": "26262370","Malawi": "18143310","Malaysia": "31528580","Maldives": "515700","Mali": "19077690","Malta": "484630","Mauritania": "4403320","Mauritius": "1265300","Mexico": "126190790","Moldova": "2706050","Monaco": "38680","Mongolia": "3170210","Montenegro": "622230","Morocco": "36029140","Mozambique": "29495960","Burma": "53708390","Namibia": "2448260","Nepal": "28087870","Netherlands": "17231620","New Zealand": "4841000","Nicaragua": "6465510","Niger": "22442950","Nigeria": "195874740","North Macedonia": "2082960","Norway": "5311920","Oman": "4829480","Pakistan": "212215030","Panama": "4176870","Papua New Guinea": "8606320","Paraguay": "6956070","Peru": "31989260","Philippines": "106651920","Poland": "37974750","Portugal": "10283820","Qatar": "2781680","Romania": "19466150","Russia": "144478050","Rwanda": "12301940","San Marino": "33780","Sao Tome and Principe": "211030","Saudi Arabia": "33699950","Senegal": "15854360","Serbia": "6982600","Seychelles": "96760","Sierra Leone": "7650150","Singapore": "5638680","Slovakia": "5446770","Slovenia": "2073890","Somalia": "15008150","South Africa": "57779620","South Sudan": "10975920","Spain": "46796540","Sri Lanka": "21670000","Saint Kitts and Nevis": "52440","Saint Lucia": "181890","Saint Vincent and the Grenadines": "110210","Sudan": "41801530","Suriname": "575990","Sweden": "10175210","Switzerland": "8513230","Syria": "16906280","Tajikistan": "9100840","Tanzania": "56318350","Thailand": "69428520","Timor-Leste": "1267970","Togo": "7889090","Trinidad and Tobago": "1389860","Tunisia": "11565200","Turkey": "82319720","Uganda": "42723140","Ukraine": "44622520","United Arab Emirates": "9630960","United Kingdom": "66460340","US": "326687500","Uruguay": "3449300","Uzbekistan": "32955400","Venezuela": "28870190","Vietnam": "95540400","Yemen": "28498690","Zambia": "17351820"}
country_pop_df = pd.DataFrame.from_dict(country_pop_dict, orient='index')
new_header = country_pop_df.iloc[0]
country_pop_df = country_pop_df[1:]
country_pop_df.columns = new_header
country_pop_df['population'] = country_pop_df['population'].astype(int)
country_pop_df = country_pop_df.reset_index()
country_pop_df = country_pop_df.rename(columns={'index': 'country'})

#Function to pull in COVID data
def pull_covid_data(var):
    url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_'+var+'_global.csv'
    response = requests.get(url)
    formatted = csv.reader(response.text.strip().split('\n'))
    list_records = []
    for record in formatted:
        list_records.append(record)
    df = pd.DataFrame(list_records)
    header = df.iloc[0]
    df = df[1:]
    df.columns = header
    df = df.drop(columns=['Province/State', 'Lat', 'Long'])
    df = df.set_index('Country/Region')
    df = df.apply(pd.to_numeric)
    df = df.reset_index()
    df = df.groupby(['Country/Region']).sum()
    df = df.reset_index()
    df = pd.melt(df, id_vars=['Country/Region'])
    df = df.rename(columns={'Country/Region': 'country', 0: 'date', 'value': var})
    return df

#Get COVID data for confirmed, deaths and recovered
df_confirmed = pull_covid_data('confirmed')
df_deaths = pull_covid_data('deaths')
df_recovered = pull_covid_data('recovered')

#Merge datasets and drop missing
df_covid = pd.merge(df_confirmed, df_deaths,  how='inner', left_on=['country','date'], right_on = ['country','date'])
df_covid = pd.merge(df_covid, df_recovered,  how='inner', left_on=['country','date'], right_on = ['country','date'])
df_covid = pd.merge(df_covid, country_pop_df, how='left', on='country')
df_covid = df_covid.dropna()

#Get list of countries
def remove_duplicates(x):
    return list(dict.fromkeys(x))
country_list = remove_duplicates(df_covid['country'].tolist())

#country_list = ['Denmark','US']

#Create charts
for countryID in country_list:
    country_df = df_covid[['date','country','confirmed','deaths','recovered','population']]
    country_df = country_df[country_df['country']==countryID]
    country_df[['confirmed_diff','recovered_diff','deaths_diff']]=country_df[[
            'confirmed','recovered','deaths']].diff()    
    country_df['confirmed_pct'] = (country_df['confirmed_diff']) / country_df['population'] * 100
    country_df['deaths_pct'] = (country_df['deaths_diff']) / country_df['population'] * 100
    country_df['recovered_pct'] = (country_df['recovered_diff']) / country_df['population'] * 100
    country_df['date'] = country_df['date'].astype(str)
    date_list = country_df['date'].astype('str')
    dates = [dt.datetime.strptime(d,'%m/%d/%y').date() for d in date_list]
    fig = plt.figure(figsize=(18,9))    
    ax1 = fig.add_subplot(2, 1, 1)
    ax2 = fig.add_subplot(2, 1, 2)
    fig.suptitle('Daily COVID statistics for ' + countryID, fontsize=16)
    months = mdates.MonthLocator()
    months_fmt = mdates.DateFormatter('%b')
    #ax1 - numeric data
    confirmed = country_df['confirmed_diff'].astype('float')
    deaths = country_df['deaths_diff'].astype('float')
    recovered = country_df['recovered_diff'].astype('float')
    ax1.plot(dates, confirmed, label='Confirmed Cases', color='blue')
    ax1.plot(dates, recovered, label='Recoveries', color='green')
    ax1.legend(loc='upper left')
    ax1.xaxis.set_major_locator(months)
    ax1.xaxis.set_major_formatter(months_fmt)
    ax1.set_ylim(bottom=0.)
    ax1.get_yaxis().set_major_formatter(
            mtick.FuncFormatter(lambda x, p: format(int(x), ',')))
    ax1r = ax1.twinx()
    ax1r.plot(dates, deaths, label='Deaths', color='red')
    ax1r.xaxis.set_major_locator(months)
    ax1r.xaxis.set_major_formatter(months_fmt)
    ax1r.set_ylim(bottom=0.)    
    ax1r.get_yaxis().set_major_formatter(
            mtick.FuncFormatter(lambda x, p: format(int(x), ',')))
    ax1r.legend(loc='upper right')
    ax1r.grid(True)
    #ax2 - percentage data
    confirmed = country_df['confirmed_pct'].astype('float')
    deaths = country_df['deaths_pct'].astype('float')
    recovered = country_df['recovered_pct'].astype('float')
    ax2.plot(dates, confirmed, label='Confirmed Cases % of Pop', color='blue')
    ax2.plot(dates, recovered, label='Recoveries % of Pop', color='green')
    ax2.set_ylim(0, 0.040)
    ax2.set_yticks((0, 0.008, 0.016, 0.024, 0.032, 0.040))
    ax2.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=3))
    ax2.legend(loc='upper left')
    ax2.xaxis.set_major_locator(months)
    ax2.xaxis.set_major_formatter(months_fmt)
    ax2.set_ylim(bottom=0.)
    ax2r = ax2.twinx()
    ax2r.plot(dates, deaths, label='Deaths % of Pop', color='red')
    ax2r.xaxis.set_major_locator(months)
    ax2r.xaxis.set_major_formatter(months_fmt)
    ax2r.set_ylim(0, 0.0040)
    ax2r.set_yticks((0, 0.0008, 0.0016, 0.0024, 0.0032, 0.0040))
    ax2r.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=4))
    ax2r.legend(loc='upper right')
    ax2r.grid(True)
    plt.savefig('covid_graph_' + countryID + '.png', format='png', bbox_inches='tight')
    plt.close()