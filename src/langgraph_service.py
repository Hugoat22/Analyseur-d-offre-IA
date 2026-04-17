from langgraph.graph import StateGraph, START, END
from typing import TypedDict
from dotenv import load_dotenv
import os
from src.llm_service import generation_reponse_final_llm
from src.extration import COMPETENCES, recupere_data
from src.neo4j_connexion import Neo4jDb
from src.outils import *

load_dotenv()

db = Neo4jDb(os.getenv("URL_NEO4J"), os.getenv("DATABASE_NEO4J"), os.getenv("PASSWORD_NEO4J"))

def graph_top_competences(state):
    data = top_competences(db, top_n=25)
    return {"resultat": data}

def graph_offres_par_competence(state):
    comp = state["competences"]
    result = {}
    if comp:
        for competence in comp:
            result[competence] = offres_par_competence(db, competence)
    return {"resultat": result}

def graph_lien_profil_offre(state):
    nom = state["nom_personne"]
    titre = state["titre_offre"]
    data = lien_profil_offre(db, nom, titre)
    return {"resultat": data}

def detection_type_question(state):
    question = state["question"].lower()

    modif = {
        "question_type" : "inconnu",
        "competences" : [],
        "nom_personne" : None,
        "titre_offre" : None
    }

    if ("top" in question or "plus demand" in question) and ("competences" in question):
        modif["question_type"] = "top_competences"
    elif ("profil" in question or "competences" in question or "manquantes" in question or "communes" in question) and "offre: " in question:
        modif["question_type"] = "lien_profil_offre"
        modif["nom_personne"] = recupere_data("user.json")["nom"]
        modif["titre_offre"] = state["question"].split("offre: ")[1].split(".")[0]
    elif "offre" in question or "competence" in question:
        for comp in COMPETENCES:
            if comp.lower() in question:
                modif["question_type"] = "offres_par_competence"
                modif["competences"].append(comp)

    return modif

def question_inconnue(state):
    return {"reponse": "Je n'ai pas compris le type de votre question."}

def generation_reponse(state):
    rep = generation_reponse_final_llm(state)
    return {"reponse": rep}
def router(state):
    return state["question_type"]
    
class State(TypedDict):
    question: str
    question_type: str
    competences: list
    nom_personne: str
    titre_offre: str
    resultat: str
    reponse: str

builder = StateGraph(State)

builder.add_node("detection_type_question", detection_type_question)
builder.add_node("top_competences",graph_top_competences)
builder.add_node("offres_par_competence",graph_offres_par_competence)
builder.add_node("lien_profil_offre",graph_lien_profil_offre)
builder.add_node("question_inconnue",question_inconnue)
builder.add_node("generation_reponse",generation_reponse)

builder.add_edge(START, "detection_type_question")

choix = {
    "top_competences" : "top_competences",
    "offres_par_competence" : "offres_par_competence",
    "lien_profil_offre" : "lien_profil_offre",
    "inconnu" : "question_inconnue"
}

builder.add_conditional_edges("detection_type_question",router,choix)

builder.add_edge("top_competences", "generation_reponse")
builder.add_edge("offres_par_competence", "generation_reponse")
builder.add_edge("lien_profil_offre", "generation_reponse")
builder.add_edge("question_inconnue", END)
builder.add_edge("generation_reponse", END)

graph = builder.compile()