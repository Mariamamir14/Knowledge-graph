#!/usr/bin/env python
# coding: utf-8

# In[39]:


from rdflib import Graph, Literal, RDF, URIRef
import pandas as pd
from SPARQLWrapper import SPARQLWrapper
from SPARQLWrapper import JSON


# In[10]:


get_ipython().run_line_magic('reload_ext', 'jupyter-rdfify')


# Here is the SPARQL query to extract individuals from Wikidata that will be used to build the knowledge graph which are
# Player, SportsClub, League, Position, Event, SportsClub Start date, SportsClub end date, Division and Conference.
# Filtering only the Players who have NBA_ID to limit the data 

# In[ ]:


sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
sparql.setReturnFormat(JSON)


query_player = """

PREFIX pq: <http://www.wikidata.org/prop/qualifier/>
PREFIX ps: <http://www.wikidata.org/prop/statement/>
PREFIX p: <http://www.wikidata.org/prop/>
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>


SELECT ?player ?playerName ?realgmID ?position ?event ?team ?start ?end ?teamCountry ?league ?division ?conference
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
           
             ?team wdt:P118 ?league # get the league the team plays in, if available
 
  OPTIONAL { ?team wdt:P361 ?division .
            ?division wdt:P361 ?conference.} #get the division of the team, if it exits get it's conference

            ?player p:P3957 ?realgmStatement .
            ?realgmStatement ps:P3957 ?realgmID . # get the RealGM ID for each player,
?player rdfs:label ?playerName . FILTER (lang(?playerName) = 'en')
  
  FILTER EXISTS {?player wdt:P2685 ?nbaID}
}

Limit 100000

"""
sparql.setQuery(query_player)
Basketball_players = sparql.query().convert()


# In[25]:


print(type(Basketball_players))


# In[26]:


Basketball_players["results"]["bindings"][4]


# In[27]:


len(Basketball_players["results"]["bindings"])


# In[28]:


#column list
cols = list(Basketball_players["results"]["bindings"][4].keys())
cols


# In[29]:


#creating a data dictionary
data = {key:[] for key in cols}
data


# In[30]:


for item in Basketball_players["results"]["bindings"]:
    for col in cols:
        if col in item:
            data[col].append(item[col]['value'])
        else:
            data[col].append("")


# In[31]:


data_frame = pd.DataFrame(data)
print('There are',len(data_frame),'records in the dataframe')
data_frame.head()


# In[32]:


#Total edges without temporal metadata
data_frame[['player','team', 'playerName', 'teamCountry', 'position', 'event', 'league', 'realgmID', 'division', 'conference']].size


# In[33]:


data_frame.to_csv('Wikidata_data.csv', index=False)


# In[41]:


Unique_player = data_frame['playerName'].unique()
len(Unique_player)
print("There are " + str(len(Unique_player))+ " unique Players.")


# In[42]:


Unique_RealGM = data_frame['realgmID'].unique()
len(Unique_RealGM)
print("There are " + str(len(Unique_RealGM))+ " unique ReamgmIDs.")


# In[ ]:




