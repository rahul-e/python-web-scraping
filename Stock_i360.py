#!/usr/bin/env python
# coding: utf-8

# In[1]:


import csv
import requests
import os
from bs4 import BeautifulSoup
import pandas as pd
import datetime
from openpyxl import load_workbook
import numpy as np


# In[2]:


# Define the folder where the downloaded data will be stored
datapath = 'C:/Users/karnn/Documents/Stocks/'
print(datapath)
ct=datetime.date.today()
print(ct)


# In[3]:


# Define url where data can be downloaded
rate_url = 'https://www.marketwatch.com/investing/stock/' # Base url for searching for university ratings


# In[4]:


############## DOWNLOAD DATA ##############

print('\r')
print('Starting web scrape')
print('\r')

# Ticker labels
ticker =['msft', 'nvda', 'aapl', 'acn', 'qcom','nflx','fb','orcl','amzn','goog','txn', 'csco', 'dis','nke','t','cat','twlo']

# Define a file for storing the downloaded data
outfile = datapath + 'marketwatchscrape.xlsx'
book = load_workbook('C:/Users/karnn/Documents/Stocks/marketwatchscrape.xlsx')
writer = pd.ExcelWriter('C:/Users/karnn/Documents/Stocks/marketwatchscrape.xlsx', engine='openpyxl')
writer.book = book
writer.sheets = {ws.title: ws for ws in book.worksheets}

#with pd.ExcelWriter(outfile, dateformat='YYYY-MM-DD', mode="a", if_sheet_exists='new') as writer:
# Loop through the ticker list and do web-scraping for each
for orgid in ticker:
		try:
			org_url1 = rate_url + orgid + '/company-profile?mod=mw_quote_tab'

			r1 = requests.get(org_url1, allow_redirects=True) # Request the webpage
			print(r1.status_code) # Confirm if the request was successful (200 = success, anything else = not successful)

			soup = BeautifulSoup(r1.text, 'html.parser') # Convert the webpage's text into an object called 'soup'

			items = soup.find_all('td', attrs={'class': 'table__cell w75'}) #Find all web elements called 'span' whose 'class' attribute has the value 'score'
			df1=pd.DataFrame()
			tmpDF= pd.DataFrame(items,columns=['Col1'])        
			df1[['colA','colB']]= tmpDF.Col1.str.split(n=1,expand=True)
		
			val = soup.find_all('td', attrs={'class': 'table__cell w25'})
			tmpDF= pd.DataFrame(val,columns=['Col2'])
		
			df1[['Values']]= tmpDF.Col2.str.split(n=1,expand=True)
			df1['colB']=df1['colB'].fillna(value=' ')

			df1['Attribute']=df1['colA']+' '+df1['colB']
			#df1.to_excel(writer, sheet_name=orgid,columns=['Attribute'],header=['Attribute'],startcol=1)
			#df1.to_excel(writer, sheet_name=orgid,columns=['Values'],header=['Value'],startcol=5,index=False)


		except:
			print('Cannot find Page 2 for the ticker', orgid)
#	for orgid in ticker:
		try:        
			org_url2 = rate_url + orgid + '?mod=mw_quote_tab'
			r2 = requests.get(org_url2, allow_redirects=True) # Request the webpage
			print(r2.status_code)

			soup = BeautifulSoup(r2.text, 'html.parser') # Convert the webpage's text into an object called 'soup'
			items = soup.find_all('small', attrs={'class': 'label'}) #Find all web elements called 'span' whose 'class' attribute has the value 'score'
			val = soup.find_all('span', attrs={'class': 'primary'})
			tmpDF4= pd.DataFrame(items,columns=['Attribute'])        
            
			tmpDF2= pd.DataFrame(val,columns=['Col1'])
			tmpDF2=tmpDF2.drop(labels=[0,1,2,3,4]).reset_index()
			tmpDF4['Values']= tmpDF2['Col1']
			df1=pd.concat([df1,tmpDF4],ignore_index=False)
#			df1.to_excel(writer, sheet_name=orgid+str(ct),columns=['Attribute'],header=['Attribute'],startcol=1)
#			df1.to_excel(writer, sheet_name=orgid+str(ct),columns=['Values'],header=['Value'],startcol=5,index=False)
            
		except:
			print('Cannot find Page 1 for the ticker', orgid)
#	for orgid in ticker:
		try:        
			org_url3 = rate_url + orgid + '/financials'
			r3 = requests.get(org_url3, allow_redirects=True) # Request the webpage
			print(r3.status_code)

			soup = BeautifulSoup(r3.text, 'html.parser') # Convert the webpage's text into an object called 'soup'
			items_main = soup.find_all('div', attrs={'class': 'cell__content fixed--cell'}) #Find all web elements called 'span' whose 'class' attribute has the value 'score'
			items_sub = soup.find_all('div', attrs={'class': 'cell__content indent--small'})
			items_sub_sub = soup.find_all('div', attrs={'class': 'cell__content indent--medium'})
			heading = soup.find_all('th', attrs={'class': "overflow__heading"})
			ColumnHead = pd.Series(heading).astype('string')
			ColumnHead = ColumnHead.str.replace(r'\D+','',regex=True)
			ColumnHead = ColumnHead.drop(labels=[0, 6]).reset_index()
			ColumnHead.columns = ['Index','ColumnHead']
			ColumnHead = ColumnHead.drop(['Index'],axis=1)
			#val = soup.find_all('span', attrs={'class': ""})
			val_everything = soup.find_all('td', attrs={'class': "overflow__cell"})
			tmpDF= pd.DataFrame(items_main,columns=['Attribute'])        
			tmpDF=tmpDF.drop(labels=[0]).reset_index()
			tmpDF_= pd.DataFrame(items_sub,columns=['Sub attribute'])        
			tmpDF_s= pd.DataFrame(items_sub_sub,columns=['Sub sub attribute'])
            
			#tmpDF3= pd.DataFrame(val,columns=['Value'])
			#tmpDF3= tmpDF3.drop(labels=[0,1,2,3,4,5,6]).reset_index()
			tmpDF2= pd.DataFrame(val_everything,columns=['AllValues']).astype('string')
			tmpDF2['AllValues']= tmpDF2['AllValues'].str.replace('[^0-9A-Z.%-]+','',regex=True)
			numRow=57
			col=['Col1','Col2','Col3','Col4','Col5','Col6','Col7']*numRow
			s = pd.Series(tmpDF2.AllValues.values, col)
			u = np.unique(s.index.values).tolist()
			tmpDF5=pd.concat([s.loc[k].reset_index(drop=True) for k in u], axis=1, keys=u)

#			for sheetname in writer.sheets:
			tmpDF.to_excel(writer, sheet_name=orgid+str(ct),columns=['Attribute'],header=['Attribute'],startcol=10)
			tmpDF_.to_excel(writer, sheet_name=orgid+str(ct),columns=['Sub attribute'],header=['Attribute'],startcol=12,index=False)

			df1.to_excel(writer,sheet_name=orgid+str(ct), columns=['Attribute','Values'], startrow=2, index = False,header= ['Attribute', 'Values'])
			tmpDF5.to_excel(writer, sheet_name=orgid+str(ct), columns=['Col1','Col2','Col3','Col4','Col5','Col6'], startrow=2, startcol=16, index = False,header= ['Attribute']+ColumnHead['ColumnHead'].tolist())
			writer.save()
			
			print('Completed data download for ', orgid)
		except:

			print('Cannot find Page 3 for the ticker', orgid)




