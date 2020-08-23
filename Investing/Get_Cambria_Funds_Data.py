from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import bs4
import pandas as pd
from datetime import datetime
import xlsxwriter

#Change current working directory
os.chdir('C:/Users/12407/Desktop/Education/Projects/Investing')

#List of data to get
data_list = ['eyld','fyld','syld']

#Set chrome driver specifications
DRIVER_PATH = './chromedriver'
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")
driver = webdriver.Chrome(chrome_options=chrome_options, 
                          executable_path=DRIVER_PATH)

#Change current working directory
os.chdir('C:/Users/12407/Desktop/Education/Projects/Investing/Cambria_Funds_Data')

#Gather dataframes with data scraped from each link
reviews = {}
for key in data_list:
    driver.get('https://www.cambriafunds.com/'+key+'-holdings')
    res = driver.page_source
    bs4Soup = bs4.BeautifulSoup(res, 'html.parser')
    data_tags = bs4Soup.select("tr")
    data_list = []
    for tag in data_tags:
        temp_list = []
        if data_tags.index(tag) == 0:
            temp_tag = tag.select("th")            
        else:
            temp_tag = tag.select("td")
        for tag_2 in temp_tag:
            temp_list.append(tag_2.getText().strip())
        data_list.append(temp_list)
    reviews[key] = pd.DataFrame(data_list)

#Export dataframes to excel with today's date 
current_date = datetime.today().strftime('%Y-%m-%d')
writer = pd.ExcelWriter('Cambria_Funds_'+current_date+'.xlsx', engine='xlsxwriter')
for key in reviews:
    reviews[key].to_excel(writer, sheet_name=key, header=False, index=False)
writer.save()