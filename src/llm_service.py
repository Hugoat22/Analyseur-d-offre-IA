import os
import requests

def generation_reponse_final_llm(state):
    prompt = f"""
    Tu es un RH specialise dans le recrutement d'alternants en IT.
    Tu a pour projet d'aide et d'informer l'etudient qui te pose des questions.

    consigne :
    - tu dois donner des reponses claires et precises.
    - tu dois donner des reponses courtes.
    - tu dois donner des reponses en francais.
    - ne n'invente pas de competences qui ne sont pas donnees dans les donnees.

    données :
    nom de l'utilisateur : {state["nom_personne"]}
    question de l'utilisateur : {state["question"]} 
    type de la question detecter: {state["question_type"]}
    resultat des outils : {state["resultat"]}
    """

    response = requests.post(
        os.getenv("URL_LLM"),
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
        
    )
    return response.json()["response"]