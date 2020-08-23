#################################
#Do analysis on USGS metals data#
#################################

#Import python packages
import bs4
import requests
import pandas as pd
import os
import wget
from zipfile import ZipFile 
import re
import glob
import matplotlib.pyplot as plt
import numpy as np 
import seaborn as sns

#Set current working directory to fails data folder
print('Current Working Directory' , os.getcwd())
os.chdir('C:/Users/12407/Desktop/Education/Projects/Metals/Data')
print('New Working Directory' , os.getcwd())

#Get links for each metal data file
'''
res = requests.get('https://pubs.usgs.gov/sir/2012/5188/tables/')
res.raise_for_status()
bs4Soup = bs4.BeautifulSoup(res.text, 'html.parser')
links = []
for link in bs4Soup.find_all('a', attrs={'href': re.compile('xlsx')}):
    links.append('https://pubs.usgs.gov/sir/2012/5188/tables/' + link.get('href'))
'''

#Python code to remove duplicate elements 
'''
def Remove(duplicate): 
    final_list = [] 
    for num in duplicate: 
        if num not in final_list: 
            final_list.append(num) 
    return final_list 
links = Remove(links)
'''

#Download metals to metals data folder 
'''
for link in links:
    filename = wget.download(link)
'''

#Put file names into a list: r=root, d=directories, f = files
'''
path = os.getcwd()
files = []
for r, d, f in os.walk(path):
    for file in f:
        if '.xlsx' in file:
            #files.append(os.path.join(r, file))
            files.append(file)
'''

#Create function to read in excel files 
'''
def md_read(file,tab,name):
    print(name)
    df = pd.read_excel(file, sheet_name=tab)
    if len(df.columns) == 2:
        df.columns = ['Year','Price']
    else:
        df = df.iloc[:,0:3]
        df.columns = ['Year','Blank','Price']
        df = df[['Year','Price']]
    df['Type'] = name.split(".")[0]
    start_row = df.index[df['Year'] == 'Year'].tolist()[0]+1
    df = df[start_row:]
    #end_row = df.index[df['Year'].str[:2] == 'No'].tolist()[0]-1
    end_row = df.index[df['Year'].isnull()].tolist()[0] - start_row
    df = df[:end_row]
    return df
'''

#Read in excel files into data frame 
'''
Dict = {'chromium.xlsx': ['Ore','Ferrochromium','Metal'],
        'ironore.xlsx': ['Fines','Pellets'],
        'nickel.xlsx': ['Nickel','Stainless steel'],
        'niobium.xlsx': ['Ore&Conc', 'FeNb'],
        'pgm.xlsx': ['Iridium','Osmium','Palladium','Platinum','Rhodium','Ruthenium'],
        'rare_earth.xlsx': ['Cerium','Dysprosium','Europium','Gadolinium',
                            'Lanthanum','Neodymium','Praseodymium',
                            'Samarium','Scandium','Terbium','Yttrium']} 
Dict2 = {'ferrosilicon.xlsx': 'Data',
         'silicon.xlsx': 'Data',
         'tantalum.xlsx': 'Ta prices'}
mdf = pd.DataFrame(columns=['Year','Price','Type'])
for file in files:
    if file=='appendix1_deflators.xlsx':
        pass
    elif file in Dict:
        for element in Dict[file]:
            mdf = mdf.append(md_read(file,element,element+' '+file))
    elif file in Dict2:
        mdf = mdf.append(md_read(file,Dict2[file],file))
    else:
        mdf = mdf.append(md_read(file,'Sheet1',file))
'''
        
#Export file
#mdf.to_csv(r'C:/Users/12407/Desktop/Education/Projects/Metals/Metals_Data.csv',index=False)

mdf = pd.read_csv(r'C:/Users/12407/Desktop/Education/Projects/Metals/Metals_Data.csv')

#Graph precious metals price history
os.chdir('C:/Users/12407/Desktop/Education/Projects/Metals')
os.chdir('C:/Users/12407/Desktop/Education/Projects/Metals')
df = mdf[mdf['Type'].isin(['gold','Palladium pgm','Platinum pgm','silver'])]
df = df[df['Year'] >= '1968']
sns_plot = sns.lineplot(x="Year", y="Price", hue="Type", data=df)
fig = sns_plot.get_figure()
fig.savefig("output.png")

#Graph pgm price history
os.chdir('C:/Users/12407/Desktop/Education/Projects/Metals')
df = mdf[mdf['Type'].isin(['Palladium pgm','Platinum pgm','Iridium pgm',
         'Osmium pgm','Rhodium pgm','Ruthenium pgm'])]
df = df[df['Year'] >= '1930']
sns_plot = sns.lineplot(x="Year", y="Price", hue="Type", data=df)
fig = sns_plot.get_figure()
fig.savefig("pgm.png")

#Look at correlation in precious metals
mdf = pd.read_csv(r'C:/Users/12407/Desktop/Education/Projects/Metals/Metals_Data.csv')
df = mdf[mdf['Type'].isin(['gold','Palladium pgm','Platinum pgm','silver'])]
df.set_index(['Year','Type'],inplace=True)
df = df.unstack()
pm_corr = df.corr()

#Look at correlation in pgms
df = mdf[mdf['Type'].isin(['Palladium pgm','Platinum pgm','Iridium pgm',
         'Osmium pgm','Rhodium pgm','Ruthenium pgm'])]
df.set_index(['Year','Type'],inplace=True)
df = df.unstack()
pgm_corr = df.corr()

#Look at correlation in all metals
df = mdf
df.set_index(['Year','Type'],inplace=True)
df = df.unstack()

#Look at correlation between two metals
mdf = pd.read_csv(r'C:/Users/12407/Desktop/Education/Projects/Metals/Metals_Data.csv')
Metals_List = []
Metal_1 = 'gold'
Metals_List.append(Metal_1)
Metal_2 = 'Platinum pgm'
Metals_List.append(Metal_2)
df = mdf[mdf['Type'].isin(Metals_List)]
df.set_index(['Year','Type'],inplace=True)
df = df.unstack()
sm_corr = df.corr()
print(sm_corr.iat[1,0])


