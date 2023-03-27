#!/usr/bin/env python
# coding: utf-8

# KG Builfding 

# In[479]:


import rdflib
from urllib.parse import quote
from rdflib import Graph, URIRef, Literal, BNode, Namespace
from rdflib.namespace import FOAF, RDF, OWL, RDFS, XSD
import pandas as pd
from owlready2 import *
import owlready2 as owl
from datetime import datetime


# In[405]:


df = pd.read_csv("/Users/mariamamir/BB_KG/Wikidata_data.csv")
df.head()


# In[408]:


# Count the number of NA values in column RealgmID
na_count = df['realgmID'].isna().sum()
print(f"Number of NA rows in column realgmID: {na_count}")


# In[462]:


na_count = df['realgmID'].unique()
len(na_count)
#Unique players = 5897


# In[463]:


#detele all NA values because it turns the column from Integer to float
df.dropna(subset=['realgmID'], inplace=True)
df['realgmID'] =df['realgmID'].apply (lambda x : str(x))
# Save the cleaned dataset to a new file
df.to_csv("/Users/mariamamir/BB_KG/Wikidata_dataCleaned.csv", index=False)


# In[464]:


df = pd.read_csv("/Users/mariamamir/BB_KG/Wikidata_dataCleaned.csv", dtype={'realgmID': int})
df


# In[281]:


len(df.team.unique())


# In[282]:


df.dtypes


# In[284]:


#replacing fullname with - for the website of Realgm 
df['realgmURL']= df['playerName'].apply(lambda x : "https://basketball.realgm.com/player/"+x.replace(" ", "-") + '/summary/' )
df['realgmID'] =df['realgmID'].apply (lambda x : str(x))
df["realgmURL"]= df["realgmURL"] + df['realgmID']
df.head()


# In[466]:


dt=df


# In[286]:


dt['realgmURL'][0]


# ### Loading my bb.owl file (didn't work)

# In[363]:


#onto = owl.get_ontology("/Users/mariamamir/BB_KG/BB.owl").load()


# In[364]:


#print("Classes:")
#for cls in onto.classes():
    #print(cls)


# In[365]:


#onto.classes()


# In[366]:


list(onto.classes())


# In[367]:


#for index, row in dt.iterrows():
    #try:
       # new_individual = onto.Individual(row['Player'])
    #except Exception as e:
        #print("Failed to create individual for row {}: {}".format(index, e))
        #continue



# In[368]:


#player_class = onto.search_one(iri="http://www.semanticweb.org/mariamamir/ontologies/2022/11/untitled-ontology-10#Player")
#player_class.instances.append(new_individual)


# ### URI Creation

# In[369]:


from rdflib import Namespace


# In[370]:


def create_uri_ref(name:str, mainURL):
    """Takes a string and a mainURL then returns a URI extending the baseURL """
    
    quoted = quote(name.replace(" ","_"))
    return mainURL[quoted]


# In[371]:



#bbkg is basketball knowledge graph
mainURL = Namespace('http://bbkg.com/')
# Create an RDF URI node to use as the subject for multiple triples
x = create_uri_ref('playes_for', mainURL)
x


# In[467]:


dt.columns


# In[373]:


Ontology_col = ['Player', 'full_name', 'ID', 'Sports_Club','Sports_League','Country','Position','Event','Division','Conference']


# ### Column Mapping

# In[447]:


#the mapping will be used for creating predicate URI from column name
player_prop_URI_map = {
    
    'full_name':create_uri_ref('full_name',mainURL),
    'ID':create_uri_ref('ID',mainURL),
    'plays_for':create_uri_ref('plays_for',mainURL), 
    'play_as':create_uri_ref('play_as',mainURL),
    'participated_in':create_uri_ref('participated_in',mainURL),
    #'is_awarded':create_uri_ref('is_awarded',mainURL),
    #'in':create_uri_ref('in',mainURL),
}

team_prop_URI_map = {
    
    'based_in':create_uri_ref('based_in',mainURL),
    'competes_in':create_uri_ref('competes_in',mainURL),
    'part_of':create_uri_ref('part_of',mainURL),
    #'start':create_uri_ref('start',mainURL),
    #'end':create_uri_ref('end',mainURL),
}

division_prop_URI_map = {
    
    'is_in':create_uri_ref('is_in',mainURL)
    
}


# In[375]:


uri_features = ['ID','plays_for','play_as','participated_in','is_awarded','based_in','competes_in','part_of','is_in']
literal_features = ['full_name','start','end','in']


# ### Ontology

# In[432]:


from rdflib import Graph


# In[433]:


g = Graph()
g.bind('bbkg',mainURL)


# In[434]:


#T-Box for classes

#classes
g.add((mainURL.Player, RDF.type, RDFS.Class))
g.add((mainURL.Basketball_Player, RDF.type, RDFS.Class))
g.add((mainURL.Active_Player, RDF.type, RDFS.Class))
g.add((mainURL.Inactive_Player, RDF.type, RDFS.Class))

g.add((mainURL.Sports_Club, RDF.type, RDFS.Class))
g.add((mainURL.Basketball_Club, RDF.type, RDFS.Class))

g.add((mainURL.Country, RDF.type, RDFS.Class))

g.add((mainURL.Sports_League, RDF.type, RDFS.Class))
g.add((mainURL.Basketball_League, RDF.type, RDFS.Class))

g.add((mainURL.Position, RDF.type, RDFS.Class))
g.add((mainURL.Basketball_Position, RDF.type, RDFS.Class))

g.add((mainURL.Event, RDF.type, RDFS.Class))

g.add((mainURL.Division, RDF.type, RDFS.Class))
g.add((mainURL.Basketball_Division, RDF.type, RDFS.Class))

g.add((mainURL.Conference, RDF.type, RDFS.Class))
g.add((mainURL.Statement, RDF.type, RDFS.Class))
g.add((mainURL.Award, RDF.type, RDFS.Class))
g.add((mainURL.RealGM, RDF.type, RDFS.Class))



#Subclass
g.add((mainURL.Player, RDFS.subClassOf, FOAF.Person))
g.add((mainURL.Sports_Club, RDFS.subClassOf, FOAF.Organization))
g.add((mainURL.Basketball_Player, RDFS.subClassOf, mainURL.Player))
g.add((mainURL.Active_Player, RDFS.subClassOf, mainURL.Player))
g.add((mainURL.Inactive_Player, RDFS.subClassOf, mainURL.Player))
g.add((mainURL.Basketball_Position, RDFS.subClassOf, mainURL.Position))
g.add((mainURL.Basketball_Division, RDFS.subClassOf, mainURL.Division))
g.add((mainURL.Basketball_League, RDFS.subClassOf, mainURL.Sports_League))

#OWL same as
g.add((mainURL.Player,OWL.sameAs,URIRef("https://www.wikidata.org/wiki/Q3665646"))) 
g.add((mainURL.Sports_Club, OWL.sameAs,URIRef("https://www.wikidata.org/wiki/Q13393265" ))) 
g.add((mainURL.Country, OWL.sameAs, URIRef("https://www.wikidata.org/wiki/Q6256"))) 
g.add((mainURL.Sports_League, OWL.sameAs, URIRef("https://www.wikidata.org/wiki/Q18536323"))) 
g.add((mainURL.Position, OWL.sameAs, URIRef("https://www.wikidata.org/wiki/Q1148974")))
g.add((mainURL.Event, OWL.sameAs, URIRef("https://www.wikidata.org/wiki/Q27020041"))) 
g.add((mainURL.Division, OWL.sameAs, URIRef("https://www.wikidata.org/wiki/Q3032333"))) 
g.add((mainURL.Conference, OWL.sameAs, URIRef("https://www.wikidata.org/wiki/Q3032333"))) 
g.add((mainURL.RealGM, OWL.sameAs, URIRef("https://www.wikidata.org/wiki/Q42253"))) 


print(g.serialize(format='ttl'))


# In[435]:


# funciton to add properties

def addProperty(g:Graph,class_uri:URIRef,class_prop_URI_map:dict,uri_cols:list,literal_cols:list):
    
    """The function takes in graph g, property and URI mapping dictionary, uri_obects dictionalry and 
    pleayer property to add object/ datatype properties.
    
    Arguments:
    
        g: graph object
        class_uri : The URI of the class to wich these properties belong
        class_prop_URI_map: dictionary with column name and it's URI mapping belonging to a specific class
        uri_cols : columns that have URI type values
        literal_cols : columns that have literal type values
        
    Output:
    
        Returns the graph object g by adding the properties
        
        """
    for prop, uri in class_prop_URI_map.items():
        #Object type properties
        if prop in uri_cols:
            g.add((uri, RDF.type, OWL.ObjectProperty))#property type
            g.add((uri,RDFS.domain,class_uri)) #domain
        #literal type (data type) properties    
        elif prop in literal_cols:
            g.add((uri, RDF.type, OWL.DatatypeProperty))#property type
            g.add((uri, RDFS.domain, class_uri)) #domain
    # return the graph        
    return g


# In[436]:


# T- Box for properties
#adding the properties including their domains but not ranges
addProperty(g,mainURL.Player,player_prop_URI_map,uri_features,literal_features)
addProperty(g,mainURL.Sports_Club,team_prop_URI_map,uri_features,literal_features)
addProperty(g,mainURL.Division,division_prop_URI_map,uri_features,literal_features)
print(g.serialize(format='ttl'))


# In[437]:


#T-Box for properties

#adding property ranges

g.add((create_uri_ref('full_name',mainURL), RDFS.range, XSD.string))
g.add((create_uri_ref('start',mainURL), RDFS.range, XSD.dateTimeStamp))
g.add((create_uri_ref('end',mainURL), RDFS.range, XSD.dateTimeStamp))
g.add((create_uri_ref('in',mainURL), RDFS.range, XSD.dateTimeStamp))
g.add((create_uri_ref('ID',mainURL), RDFS.range, mainURL.RealGM))

g.add((create_uri_ref('plays_for',mainURL), RDFS.range, mainURL.Sports_Club))
g.add((create_uri_ref('plays_as',mainURL), RDFS.range, mainURL.Position))
g.add((create_uri_ref('participated_in',mainURL), RDFS.range, mainURL.Event))
g.add((create_uri_ref('part_of',mainURL), RDFS.range, mainURL.Division))
g.add((create_uri_ref('based_in',mainURL), RDFS.range, mainURL.Country))
g.add((create_uri_ref('competes_in',mainURL), RDFS.range, mainURL.Sports_League))
g.add((create_uri_ref('is_in',mainURL), RDFS.range, mainURL.Conference))

#Define property subcalsses

#Define property owl:sameas here


# In[468]:


#A- Box
import math
# define a functio to add the data from the database to the graph

def assertionBox(g:Graph,dt:pd.DataFrame,sub_col:str,class_prop_URI_map:dict):
    """
    The function adds triples to the graph object iteratively based on the input dataframe and the property mappings
    
    g:Graph: Graph object to which the triples will be added
    dt:pd.DataFrame : input pandas dataframe : The column names are property names except for the subject column
    sub:col : This is the name of the column in the dataframe whose values are considered to be subjects.
    class_prop_URI_map:dict : column name and its correspong URI mapping : The column names are predicates.
    
    """
    #reset the index of dataframe to avoid indexing errors
    dt = dt.reset_index()
    row = 0
    num_row = len(dt.index)
    #for each row in the dataframe
    while row<num_row:
        
        #get the record
        data_row = dt.loc[row,]
#         print(data_row)
        #setting subject value
        value=data_row[sub_col]
        #Nan= float
        if not type(value)==float: 
            subject = URIRef(value)
            #loop for predicates and their corresponding values
            for label, predicate in class_prop_URI_map.items():
                #setting the object value
                obj_val   = data_row[label]
                #Division can be NaN
                if not type(obj_val)==float: 
                    if label in uri_features:
                        g.add((subject,predicate,URIRef(obj_val)))
                    #if object is a Literal
                    elif label in literal_features:
                        g.add((subject,predicate,Literal(obj_val)))
        row+=1


    return g


# In[469]:


dt.columns


# In[471]:


dt['plays_for']=dt.Sports_Club
dt['play_as']=dt.Position
dt['participated_in']=dt.Event


# In[444]:


#Adding player and its linked data
assertionBox(g,dt,"Player", player_prop_URI_map)


# In[450]:


dt['based_in']=dt.Country
dt['competes_in']=dt.Sports_League
dt['part_of']=dt.Division


# In[451]:


#Adding Team and its country,league and division
assertionBox(g,dt,"Sports_Club",team_prop_URI_map)


# In[454]:


dt['is_in']=dt.Conference


# In[457]:


dt


# In[461]:


#Adding conference to the division
assertionBox(g,dt,"Division",division_prop_URI_map)


# In[477]:


def temporalAssertionBox(g:Graph, dt:pd.DataFrame, sub_col:str):
    """
    The function adds triples to the graph object iteratively based on the input dataframe and the property mappings
    
    g:Graph: Graph object to which the triples will be added
    dt:pd.DataFrame : input pandas dataframe : The column names are property names except for the subject column
    sub:col : This is the name of the column in the dataframe whose values are considered to be subjects.
    class_prop_URI_map:dict : column name and its correspong URI mapping : The column names are predicates.
    
    """
    #reset the index of dataframe to avoid indexing errors
    dt = dt.reset_index()
    row = 0
    num_row = len(dt.index)
    #for each row in the dataframe
    while row < num_row:
        #get the record
        data_row = dt.loc[row,]
#         print(data_row)
        #setting subject value
        subject = URIRef(data_row[sub_col])
        #creating a blank node for the timestamp or time interval
        start_node = BNode()
        #adding the start time interval triple
        g.add((start_node, RDF.type, RDF.Statement))
        g.add((start_node, RDF.subject, subject))
        g.add((start_node, RDF.predicate, URIRef("start")))
        g.add((start_node, RDF.object, Literal(data_row["start"], datatype=XSD.dateTime)))
        #adding the end time interval triple
        
        end_node = BNode()
        #adding the start or time interval triple
        g.add((end_node, RDF.type, RDF.Statement))
        g.add((end_node, RDF.subject, subject))
        g.add((end_node, RDF.predicate, URIRef("end")))
        g.add((end_node, RDF.object, Literal(data_row["end"], datatype=XSD.dateTime)))
        row += 1

    return g


# In[478]:



temporalAssertionBox(g,dt,"player")


# In[480]:


def create_timestamp(df):
    df['in']=None
    for index, row in df.iterrows():
        df.loc[index,'in']=datetime.strptime(row.Month+' '+str(row.Year),'%B %Y')


# In[481]:


dm = pd.read_csv("/Users/mariamamir/BB_KG/PlayerOfTheMonth.csv")
dm.head()


# In[482]:


create_timestamp(dm)
dm


# In[483]:


dr = pd.read_csv("/Users/mariamamir/BB_KG/RookieOfTheMont.csv")
df.head()


# In[485]:


dw = pd.read_csv("/Users/mariamamir/BB_KG/PlayerOfTheWeek.csv")
dw


# In[ ]:


def TemporalInAssertionBox(g:Graph, dt:pd.DataFrame, sub_col:str):
    """
    The function adds triples to the graph object iteratively based on the input dataframe and the property mappings
    
    g:Graph: Graph object to which the triples will be added
    dt:pd.DataFrame : input pandas dataframe : The column names are property names except for the subject column
    sub:col : This is the name of the column in the dataframe whose values are considered to be subjects.
    class_prop_URI_map:dict : column name and its correspong URI mapping : The column names are predicates.
    
    """
    #reset the index of dataframe to avoid indexing errors
    dt = dt.reset_index()
    row = 0
    num_row = len(dt.index)
    #for each row in the dataframe
    while row < num_row:
        #get the record
        data_row = dt.loc[row,]
        #setting subject value
        subject = URIRef(data_row[sub_col])
        #creating a blank node for the timestamp or time interval
        start_node = BNode()
        #adding the start time interval triple
        g.add((start_node, RDF.type, RDF.Statement))
        g.add((start_node, RDF.subject, subject))
        g.add((start_node, RDF.predicate, URIRef("in")))
        g.add((start_node, RDF.object, Literal(data_row["in"], datatype=XSD.dateTime)))
        
        #creating a blank node for the timestamp or time interval
        start_node = BNode()
        #adding the start time interval triple
        g.add((start_node, RDF.type, RDF.Statement))
        g.add((start_node, RDF.subject, subject))
        g.add((start_node, RDF.predicate, URIRef("in")))
        g.add((start_node, RDF.object, Literal(data_row["in"], datatype=XSD.dateTime)))
        #adding the end time interval triple
        
        end_node = BNode()
        #adding the start or time interval triple
        g.add((end_node, RDF.type, RDF.Statement))
        g.add((end_node, RDF.subject, subject))
        g.add((end_node, RDF.predicate, URIRef("end")))
        g.add((end_node, RDF.object, Literal(data_row["end"], datatype=XSD.dateTime)))
        row += 1

    return g


# In[492]:


f=rdflib.Graph()
start_node = BNode()
f.add((start_node, RDF.type, RDF.Statement))
f.add((start_node, RDF.subject, URIRef('subject')))
f.add((start_node, RDF.predicate, URIRef("in")))
f.add((start_node, RDF.object, Literal("saca")))
f.add((start_node, create_uri_ref('start', mainURL), Literal('2023-03-27T10:00:00', datatype=XSD.dateTime)))
      


# In[490]:


from rdflib import Graph, Literal, Namespace, RDF, URIRef, XSD

# Define namespaces for the graph
ex = Namespace('http://example.com/')
dcterms = Namespace('http://purl.org/dc/terms/')

# Create an RDF graph
g = Graph()

# Define the subject, predicate, and object of the triple
subject = URIRef(ex['my-event'])
predicate = RDF.type
object = URIRef(ex['Event'])

# Add the triple to the graph
g.add((subject, predicate, object))

# Define the start and end times
start_time = Literal('2023-03-27T10:00:00', datatype=XSD.dateTime)
end_time = Literal('2023-03-27T11:00:00', datatype=XSD.dateTime)

# Add the start and end times to the graph using the dcterms namespace
g.add((subject, dcterms['startDate'], start_time))
g.add((subject, dcterms['endDate'], end_time))


# In[ ]:




