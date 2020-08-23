#Import python packages
import pandas as pd
import os

#Set current working directory to fails data folder
print('Current Working Directory' , os.getcwd())
os.chdir('C:/Users/12407/Desktop/Education/Projects/Portfolio_Allocation')
print('New Working Directory' , os.getcwd())

#Read in data from excel
df = pd.read_excel('Annual_Investment_Data.xlsx', sheetname='Summary')

#Initialize return table
return_table = pd.DataFrame(columns=[0,1,2,3,4,5,6,7,8,9,10])

#Calculate additional portfolios
df['Faber'] = 0.50*df['Stocks'] + 0.25*df['Bonds'] + 0.25*df['Gold']
df['SGold'] = 0.75*df['Stocks'] + 0.25*df['Gold']
df['SPrecious'] = (0.75*df['Stocks'] + 0.10*df['Gold'] + 0.05*df['Silver'] 
                + 0.05*df['Palladium'] + 0.05*df['Platinum'])

#Calculate annual rates for each group
df['Ann_Stocks'] = df['Stocks'].pct_change(1)
df['Ann_Bills'] = df['Bills'].pct_change(1)
df['Ann_Bonds'] = df['Bonds'].pct_change(1)
df['Ann_Gold'] = df['Gold'].pct_change(1)
df['Ann_Silver'] = df['Silver'].pct_change(1)
df['Ann_Palladium'] = df['Palladium'].pct_change(1)
df['Ann_Platinum'] = df['Platinum'].pct_change(1)
df['Ann_Faber'] = df['Faber'].pct_change(1)
df['Ann_SGold'] = df['SGold'].pct_change(1)
df['Ann_SPrecious'] = df['SPrecious'].pct_change(1)

#Calculate annual average returns for each group
Ann_Avg_Return_Stocks = ((df.at[df[df['Year'].astype(int)==2018].index[0],'Stocks']/
                        df.at[df[df['Year'].astype(int)==1928].index[0],'Stocks'])
                         ** (1/(2018-1928))-1)
Ann_Avg_Return_Bills = ((df.at[df[df['Year'].astype(int)==2018].index[0],'Bills']/
                        df.at[df[df['Year'].astype(int)==1928].index[0],'Bills'])
                         ** (1/(2018-1928))-1)
Ann_Avg_Return_Bonds = ((df.at[df[df['Year'].astype(int)==2018].index[0],'Bonds']/
                        df.at[df[df['Year'].astype(int)==1928].index[0],'Bonds'])
                         ** (1/(2018-1928))-1)
Ann_Avg_Return_Gold = ((df.at[df[df['Year'].astype(int)==2018].index[0],'Gold']/
                        df.at[df[df['Year'].astype(int)==1928].index[0],'Gold'])
                         ** (1/(2018-1928))-1)
Ann_Avg_Return_Silver = ((df.at[df[df['Year'].astype(int)==2018].index[0],'Silver']/
                        df.at[df[df['Year'].astype(int)==1928].index[0],'Silver'])
                         ** (1/(2018-1928))-1)
Ann_Avg_Return_Palladium = ((df.at[df[df['Year'].astype(int)==2018].index[0],'Palladium']/
                        df.at[df[df['Year'].astype(int)==1928].index[0],'Palladium'])
                         ** (1/(2018-1928))-1)
Ann_Avg_Return_Platinum = ((df.at[df[df['Year'].astype(int)==2018].index[0],'Platinum']/
                        df.at[df[df['Year'].astype(int)==1928].index[0],'Platinum'])
                         ** (1/(2018-1928))-1)
Ann_Avg_Return_Faber = ((df.at[df[df['Year'].astype(int)==2018].index[0],'Faber']/
                        df.at[df[df['Year'].astype(int)==1928].index[0],'Faber'])
                         ** (1/(2018-1928))-1)
Ann_Avg_Return_SGold = ((df.at[df[df['Year'].astype(int)==2018].index[0],'SGold']/
                        df.at[df[df['Year'].astype(int)==1928].index[0],'SGold'])
                         ** (1/(2018-1928))-1)
Ann_Avg_Return_SPrecious = ((df.at[df[df['Year'].astype(int)==2018].index[0],'SPrecious']/
                        df.at[df[df['Year'].astype(int)==1928].index[0],'SPrecious'])
                         ** (1/(2018-1928))-1)
rec = pd.DataFrame([['Annual Average Return', Ann_Avg_Return_Stocks, Ann_Avg_Return_Bills, 
                    Ann_Avg_Return_Bonds, Ann_Avg_Return_Gold, Ann_Avg_Return_Silver,
                    Ann_Avg_Return_Palladium, Ann_Avg_Return_Platinum, Ann_Avg_Return_Faber, 
                    Ann_Avg_Return_SGold, Ann_Avg_Return_SPrecious]])
return_table = return_table.append(rec)

#Calculate sharpe ratios for each group
Sharpe_Ratio_Stocks = df['Stocks'].pct_change(1).mean()/df['Stocks'].pct_change(1).std()
Sharpe_Ratio_Bills = df['Bills'].pct_change(1).mean()/df['Bills'].pct_change(1).std()
Sharpe_Ratio_Bonds = df['Bonds'].pct_change(1).mean()/df['Bonds'].pct_change(1).std()
Sharpe_Ratio_Gold = df['Gold'].pct_change(1).mean()/df['Gold'].pct_change(1).std()
Sharpe_Ratio_Silver = df['Silver'].pct_change(1).mean()/df['Silver'].pct_change(1).std()
Sharpe_Ratio_Palladium = df['Palladium'].pct_change(1).mean()/df['Palladium'].pct_change(1).std()
Sharpe_Ratio_Platinum = df['Platinum'].pct_change(1).mean()/df['Platinum'].pct_change(1).std()
Sharpe_Ratio_Faber = df['Faber'].pct_change(1).mean()/df['Faber'].pct_change(1).std()
Sharpe_Ratio_SGold = df['SGold'].pct_change(1).mean()/df['SGold'].pct_change(1).std()
Sharpe_Ratio_SPrecious = df['SPrecious'].pct_change(1).mean()/df['SPrecious'].pct_change(1).std()
rec = pd.DataFrame([['Sharpe Ratio', Sharpe_Ratio_Stocks, Sharpe_Ratio_Bills, 
                    Sharpe_Ratio_Bonds, Sharpe_Ratio_Gold, Sharpe_Ratio_Silver,
                    Sharpe_Ratio_Palladium, Sharpe_Ratio_Platinum, Sharpe_Ratio_Faber, 
                    Sharpe_Ratio_SGold, Sharpe_Ratio_SPrecious]])
return_table = return_table.append(rec)

#Calculate max drawdown for each group
Max_Drawdown_Stocks = df['Stocks'].pct_change(1).min()
Max_Drawdown_Bills = df['Bills'].pct_change(1).min()
Max_Drawdown_Bonds = df['Bonds'].pct_change(1).min()
Max_Drawdown_Gold = df['Gold'].pct_change(1).min()
Max_Drawdown_Silver = df['Silver'].pct_change(1).min()
Max_Drawdown_Palladium = df['Palladium'].pct_change(1).min()
Max_Drawdown_Platinum = df['Platinum'].pct_change(1).min()
Max_Drawdown_Faber = df['Faber'].pct_change(1).min()
Max_Drawdown_SGold = df['SGold'].pct_change(1).min()
Max_Drawdown_SPrecious = df['SPrecious'].pct_change(1).min()
rec = pd.DataFrame([['Max Drawdown', Max_Drawdown_Stocks, Max_Drawdown_Bills, 
                    Max_Drawdown_Bonds, Max_Drawdown_Gold, Max_Drawdown_Silver,
                    Max_Drawdown_Palladium, Max_Drawdown_Platinum, Max_Drawdown_Faber, 
                    Max_Drawdown_SGold, Max_Drawdown_SPrecious]])
return_table = return_table.append(rec)



#Sharpe_Ratio = portf_val[‘Daily Return’].mean() / portf_val[‘Daily Return’].std()
#Ann_Avg_Return_Stocks = df['Stocks'].pct_change(1).mean()



#Calculated 

#Insert column headers
return_table.columns = ['Concept','Stocks','Bills','Bonds','Gold','Silver','Palladium',
                        'Platinum','Faber','SGold','SPrecious']
