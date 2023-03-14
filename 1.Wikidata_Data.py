#!/usr/bin/env python
# coding: utf-8

# In[10]:


from rdflib import Graph, Literal, RDF, URIRef
import datetime
import pandas as pd
from SPARQLWrapper import SPARQLWrapper, JSON


# In[11]:


get_ipython().run_line_magic('reload_ext', 'jupyter-rdfify')


# Here is the SPARQL query to extract from Wikidata individuals that will be used to build the knowledge graph which are
# Player, SportsClub, League, Position, Event, SportsClub Start date , SportsClub end date
# Filtering only the Players who have NBA_ID to limit the data 

# In[19]:


sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
sparql.setReturnFormat(JSON)


query_player = """

PREFIX pq: <http://www.wikidata.org/prop/qualifier/>
PREFIX ps: <http://www.wikidata.org/prop/statement/>
PREFIX p: <http://www.wikidata.org/prop/>
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>


SELECT ?player ?playerName ?realgmID ?position ?event ?team ?start ?end ?teamCountry ?league 
WHERE {

  ?player wdt:P106 wd:Q3665646 ; # instance of basketball player
  
          wdt:P54 ?team . # plays for a basketball team
          
          
  OPTIONAL { ?team wdt:P17 ?teamCountry } # get the country of the team, if available
  
  OPTIONAL { ?player p:P54 ?statement .
             ?statement ps:P54 ?team .
             ?statement pq:P580 ?start .
             OPTIONAL { ?statement pq:P582 ?end }
           } # get the start and end date for each team
           
  OPTIONAL { ?player p:P413 ?positionStatement .
             ?positionStatement ps:P413 ?position .
             OPTIONAL { ?positionStatement pq:P580 ?start }
             OPTIONAL { ?positionStatement pq:P582 ?end }
           } # get the positions played by the player
           
  OPTIONAL { ?player p:P1344 ?eventStatement .
             ?eventStatement ps:P1344 ?event .
           } # get the events the player participated in
           
  OPTIONAL { ?team wdt:P118 ?league } # get the league the team plays in, if available
  
  OPTIONAL { ?player p:P3957 ?realgmStatement .
             ?realgmStatement ps:P3957 ?realgmID .
           } # get the RealGM ID for each player
           
  ?player rdfs:label ?playerName . FILTER (lang(?playerName) = 'en')
  
  
  FILTER EXISTS {?player wdt:P2685 ?nbaID}
}
Limit 100000
"""
sparql.setQuery(query_player)
Basketball_players = sparql.query().convert()


# In[20]:


print(type(Basketball_players))


# In[21]:


Basketball_players["results"]["bindings"][0]


# In[23]:


len(Basketball_players["results"]["bindings"])


# In[24]:


#column list
cols = list(Basketball_players["results"]["bindings"][1].keys())
cols


# In[25]:


#creating a data dictionary
data = {key:[] for key in cols}
data


# In[ ]:





# In[26]:


for item in Basketball_players["results"]["bindings"]:
    for col in cols:
        if col in item:
            data[col].append(item[col]['value'])
        else:
            data[col].append("")


# In[27]:


data_frame = pd.DataFrame(data)
print('There are',len(data_frame),'records in the dataframe')
data_frame.head()


# In[29]:


#Total possible edges excluding temporal metadata
data_frame[['player','team', 'playerName', 'teamCountry', 'position', 'event', 'league', 'realgmID']].size


# In[30]:


data_frame.to_csv('Player_Wikidata.csv', index=False)


# In[40]:


Unique_player = data_frame['playerName'].unique()
len(Unique_player)
print("There are " + str(len(Unique_player))+ " unique Players.")


# In[ ]:




