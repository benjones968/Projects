import requests
import bs4
import pandas as pd

res = requests.get('https://www.irs.gov/individuals/international-taxpayers/yearly-average-currency-exchange-rates')
res.raise_for_status()
bs4Soup = bs4.BeautifulSoup(res.text, 'html.parser')

bs4Soup.find_all('tr')

irs_list = []
for tag in bs4Soup.find_all('tr'):
    irs_list.append(tag.getText().replace('\n','-').replace('--','-')
                .replace('--','-').replace('--','-').strip('-'))
irs_data = pd.DataFrame(irs_list)
irs_data = irs_data.join(irs_data[0].str.split('-', expand=True).add_prefix(0))
irs_data = irs_data.drop(columns=[0, '08'])
irs_data.columns = irs_data.iloc[0]
irs_data = irs_data.drop([0])
irs_data['National Currency'] = irs_data['Country'] + ' - ' + irs_data['Currency']
irs_data = irs_data.drop(columns=['Country', 'Currency'])
irs_data.set_index(['National Currency'],inplace=True)
irs_data = irs_data.stack()
irs_data = irs_data.rename_axis(['National Currency','Year']).reset_index()
irs_data = irs_data.rename(columns={0: "Data"})

irs_data.to_csv('C:/Users/12407/Desktop/Education/Projects/IRS/irs_data.csv', index=False)


