#!/usr/bin/env python
# coding: utf-8

# In[154]:


import requests
from bs4 import BeautifulSoup
import pandas as pd
from lxml import html
import datetime


# In[155]:


# Define the URL to scrape
url = 'https://basketball.realgm.com/nba/awards/by_season'

# Send a request to the website and get the HTML content
response = requests.get(url)
response


# NBA Player Of The Month

# In[156]:


# Find all the NBA Player Of The Month from 1947 till 2023
rows=[]
#looping through the years
for year in range(2000,2023):
    
    # Url for the year I want 
    url = 'https://basketball.realgm.com/nba/awards/by_season/'+str(year)

    # Send a request to the website and get the HTML content
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content, 'lxml')
    #The table that has all the lables and the tables
    div = soup.find('div',{ 'class': 'main wrapper clearfix container'})
    #h2 has the award name to fillter with the award I want 
    l=div.find_all('h2')
    
    #index used inorder to get a wrong table
    index=3000
    for i in l:
        if i.get_text()==str(year-1)+'-'+str(year)+' NBA Player Of The Month':
            index=l.index(i)
    tables= div.find_all('table', {'class': 'tablesaw'})
    table=tables[index-1]
    tbody=table.find('tbody')
    trs = tbody.find_all('tr')
    for tr in trs:
        values=tr.find_all('td')
        rows.append(
        {
            'Player':values[0].get_text() ,
            'Team':values[1].get_text().replace('\n' , '') ,
            'Conference': values[2].get_text(),
            'Month' :values[3].get_text(),
            'Year':year,
            'Award':"NBA Player Of The Month"
            #'Date':
        })

POM = pd.DataFrame(rows)
POM
#POM.to_excel("PlayerOfTheMonth.xlsx") 


# Player of the week

# In[152]:


# Find all the nba awards by-season starting with 2023 till 1947
rows=[]
for year in range(2021,2023):
    # Define the URL to scrape
    url = 'https://basketball.realgm.com/nba/awards/by_season/'+str(year)

    # Send a request to the website and get the HTML content
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content, 'lxml')
    div = soup.find('div',{ 'class': 'main wrapper clearfix container'})
#     elements=div.findChildren(recursive=False)
    l=div.find_all('h2')
    index=30
    for i in l:
        if i.get_text()==str(year-1)+'-'+str(year)+' NBA Player Of The Week':
            index=l.index(i)
    tables= div.find_all('table', {'class': 'tablesaw'})
    table=tables[index-1]
    tbody=table.find('tbody')
    trs = tbody.find_all('tr')
    for tr in trs:
        values=tr.find_all('td')
        rows.append(
        {
            'Player':values[0].get_text() ,
            'Team':values[1].get_text().replace('\n' , '') ,
            'Conference': values[2].get_text(),
            'Month' :values[3].get_text(),
            'Year':year,
            'Award':"NBA Player Of The Week"
        })

POW = pd.DataFrame(rows)
POW
#POW.to_excel("PlayerOfTheWeek.xlsx") 


# NBA Rookie Of The Month

# In[150]:


# Find all the nba awards by-season starting with 2023 till 1947
rows=[]
for year in range(2021,2023):
    # Define the URL to scrape
    url = 'https://basketball.realgm.com/nba/awards/by_season/'+str(year)

    # Send a request to the website and get the HTML content
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content, 'lxml')
    div = soup.find('div',{ 'class': 'main wrapper clearfix container'})
    l=div.find_all('h2')
    index=30
    for i in l:
        if i.get_text()==str(year-1)+'-'+str(year)+' NBA Rookie Of The Month':
            index=l.index(i)
    tables= div.find_all('table', {'class': 'tablesaw'})
    table=tables[index-1]
    tbody=table.find('tbody')
    trs = tbody.find_all('tr')
    for tr in trs:
        values=tr.find_all('td')
        rows.append(
        {
            'Player':values[0].get_text() ,
            'Team':values[1].get_text().replace('\n' , '') ,
            'Conference': values[2].get_text(),
            'Month' :values[3].get_text(),
            'Year':year
        })
ROM = pd.DataFrame(rows)
ROM
#ROM.to_excel("RookieOfTheMont.xlsx") 


# In[ ]:




