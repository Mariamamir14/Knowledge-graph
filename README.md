# 🏀 BBKG: Basketball Time-Aware Knowledge Graph

## 📌 Overview

BBKG (Basketball Knowledge Graph) is a semantic data project that builds a **time-aware knowledge graph** for basketball data by integrating structured data from Wikidata and external data scraped from RealGM.

The project focuses on **ontology engineering, knowledge graph construction, and temporal representation**, enabling complex queries over player careers, awards, and relationships.


## 🎯 Objectives

* Design a **basketball ontology** including players, clubs, leagues, and events
* Extract structured data using SPARQL from Wikidata
* Enrich the dataset with external data from RealGM
* Represent **temporal information** (e.g., contracts, awards over time)
* Enable advanced querying over the knowledge graph


## 🧠 Key Concepts

* Ontology Engineering (Classes, Properties, Individuals)
* RDF & Triple-based representation
* Knowledge Graph Construction
* Data Integration (Wikidata + RealGM)
* **Temporal Knowledge Representation using Reification**


## 🏗️ Ontology Design

### Classes

* Player
* Sports_Club
* Sports_League
* Division
* Conference
* Position
* Event
* Award
* Active_Player / Inactive_Player

### Object Properties (Examples)

* `plays_for` → Player → Sports_Club
* `plays_as` → Player → Position
* `participated_in` → Player → Event
* `is_awarded` → Player → Award

### Data Properties

* `full_name` (string)
* `conference` (string)


## ⏳ Temporal Modeling (Core Contribution)

This project extends a standard knowledge graph into a **time-aware knowledge graph** using **reification**.

Reification allows representing relationships as entities to attach metadata such as:

* Start date
* End date
* Timestamp
* Context (e.g., conference)

### Example

Instead of:
Player → plays_for → Club

We represent:

* A relationship node with:

  * start date
  * end date

This enables querying:

* *Which team did a player play for in a specific year?*
* *Who won an award at a specific time?*

## 🌐 Data Sources

### 1. Wikidata

* Extracted using SPARQL queries
* Includes:

  * Players
  * Clubs
  * Leagues
  * Positions
  * Events

### 2. RealGM (Web Scraping)

* Player status (active / inactive)
* Player contracts
* Awards with timestamps:

  * Player of the Month
  * Player of the Week
  * Rookie of the Month

## 🛠️ Tech Stack

* Python
* RDFlib (RDF graph construction)
* SPARQL (Wikidata queries)
* Protégé (Ontology modeling)
* BeautifulSoup / Requests (Web scraping)
* Jupyter Notebook

## 📂 Project Structure

```bash
BBKG/
│── Wikidata_Data.ipynb              # Extract data from Wikidata via SPARQL
│── Scraping_RealGM_Award.ipynb      # Scrape awards data (temporal)
│── Scraping_Player_Status.ipynb     # Scrape player status (active/inactive)
│── Building_Ontology.ipynb          # Build RDF graph using RDFlib
│── Questions.ipynb                  # Query the knowledge graph
```

## ⚙️ How to Run

```bash
git clone https://github.com/Mariamamir14/Knowledge-graph.git
cd Knowledge-graph
pip install -r requirements.txt
jupyter notebook
```

### Execution Order

1. Wikidata_Data.ipynb
2. Scraping_RealGM_Award.ipynb
3. Scraping_Player_Status.ipynb
4. Building_Ontology.ipynb
5. Questions.ipynb


## 🔍 Example Queries

The knowledge graph supports complex queries such as:

* Players who play in the same position as a given player
* Club details of a player (league, country, division, conference)
* Player status (active / inactive)
* Award winners filtered by **time and conference**
* Events a player participated in


## 💡 Key Contribution

The main contribution of this project is the integration of:

* **Multiple heterogeneous data sources**
* **Temporal reasoning using reification**
* **Ontology-driven knowledge representation**

This enables more expressive queries compared to traditional datasets.


## 🔮 Future Work

* Add more leagues and international data
* Automate data pipelines
* Build a visualization dashboard
* Apply machine learning on graph embeddings


## 📜 License

This project was developed as part of a university group project at the University of Mannheim.
