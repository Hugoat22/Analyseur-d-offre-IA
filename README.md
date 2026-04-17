# Assistant Alternance IA (LangGraph + Neo4j + MCP) *(En cours)*

Assistant intelligent permettant d'analyser des offres d'emploi en intelligence artificielle et de comparer les compétences demandées avec le profil d'un candidat.

Le projet utilise :

- **Neo4j** pour représenter les relations entre offres et compétences sous forme de graphe
- **LangGraph** pour orchestrer le workflow des questions de l'utilisateur
- **LLM (Llama3)** pour générer la réponse finale du pipeline
- **MCP** pour exposer les outils afin qu'une IA puisse les utiliser

---

# Objectif du projet

Apprendre des technologies utilisées en IA comme :

- le fonctionnement de la base de données **Neo4j** et du langage **Cypher**
- l'utilisation de **LangGraph** pour construire un pipeline
- l'intégration d'un **LLM dans un projet**
- le concept de **MCP (Model Context Protocol)**

Le projet permet d'aider un étudiant à comprendre :

- quelles sont les **compétences les plus demandées**
- quelles **offres demandent une compétence spécifique**
- quelles compétences sont **communes ou manquantes pour une offre**

---

# Exemple de question

dit moi qu'elle sont les competences manquante et communes pour une offre: Alternance - Data Scientist H/F ?

### Réponse générée par le pipeline

Bonjour Atlan !

Selon les données, pour l'offre d'alternance **Data Scientist H/F**, les compétences manquantes sont :

- scikit-learn
- TensorFlow
- PyTorch
- pandas

Les compétences communes sont :

- Python
- SQL

---

# Architecture
```
Utilisateur
│
▼
main.py
│
▼
LangGraph Workflow
│
├── détection du type de question
│
├── top compétences → Neo4j
│
├── offres par compétence → Neo4j
│
├── lien profil / offre → Neo4j
│
▼
LLM (Llama3)
│
▼
Réponse
```
---

# Technologies utilisées

- Python
- Neo4j
- LangGraph
- MCP (FastMCP)
- Llama3
- Requests
- dotenv

---

# Base de données (Neo4j)

Le graphe contient :

(Personne)-[:POSSEDE]->(Competence)

(Entreprise)-[:PROPOSE]->(Offre)

(Offre)-[:DEMANDE]->(Competence)

### Exemple

(Hugo)-[:POSSEDE]->(Python)

(Thales)-[:PROPOSE]->(Data Scientist)

(Data Scientist)-[:DEMANDE]->(Python)

(Data Scientist)-[:DEMANDE]->(TensorFlow)

---

# Configuration

### 1 Configurer le `.env`

URL_NEO4J=neo4j://localhost:7687
DATABASE_NEO4J=neo4j
PASSWORD_NEO4J=password
URL_LLM=http://localhost:11434/api/generate

### 2 installer les dépendances

- neo4j
- langgraph
- python-dotenv
- requests
- fastmcp

---

# Améliorations futures

- utiliser un **LLM pour détecter le type de question** au lieu d'une détection par règles
- améliorer l'extraction automatique des compétences dans les offres
- ajouter une **interface web**
- recommander des **compétences à apprendre**
