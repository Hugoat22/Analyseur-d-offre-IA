import json
import os

COMPETENCES = [
    "Python",
    "Java",
    "C++",
    "JavaScript",
    "SQL",
    "Neo4j",
    "MongoDB",
    "Git",
    "Docker",
    "JSON",
    "XML",
    "CSV",
    "Linux",
    "LLM",
    "LangGraph",
    "LangChain",
    "outils_MCP",
    "scikit-learn",
    "sklearn",
    "TensorFlow",
    "PyTorch",
    "pandas",
    "Spark",
    "Kafka",
    "AWS",
    "Azure",
    "Cypher",
    "Graph_Data_Science",
    "Graph_Neural_Networks",
    "Deep_Learning",
    "Machine_Learning"
]

def extraction_competences(description):
    description = description.replace("(","").replace(")","").replace(",","").replace(".","")
    description_mots = description.lower().split()
    competences_trouvees = []
    for competence in COMPETENCES:
        if competence.lower() in description_mots:
            competences_trouvees.append(competence)
    return competences_trouvees

def recupere_data(nom_fichier):
    with open(os.path.join("data",nom_fichier), 'r', encoding="utf-8") as f:
        data = json.load(f)
    return data