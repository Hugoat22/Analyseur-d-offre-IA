import os
from sys import argv
from dotenv import load_dotenv
from src.extration import extraction_competences, recupere_data
from src.neo4j_connexion import Neo4jDb
from src.langgraph_service import graph

load_dotenv()

def actualiser_database(db):
    for offre in recupere_data("offres.json"):
        offre["competences"] = extraction_competences(offre["description"])
        db.ajouter_offre(offre)

    user = recupere_data("user.json")
    db.ajoute_candidat(user)

def reset_database(db):
    db.supprime_database()

def main():
    db = Neo4jDb(os.getenv("URL_NEO4J"), os.getenv("DATABASE_NEO4J"), os.getenv("PASSWORD_NEO4J"))
    if len(argv) not in [2,3]:
        raise Exception("Argument non valide !")
    match argv[1]:
        case "-help":
            print("""
            main.py -a : actualiser la base de donnée pour des changements de profil et d'offres
            main.py -r : supprime tout le contenue de la base de donnée
            main.py -s titre_offre : renvoie un avis sur le poste demander
            """)
        case "-import":
            actualiser_database(db)
        case "-reset":
            reset_database(db)
        case "-question":
            if len(argv) != 3:
                raise Exception("il manque la question !")

            res = graph.invoke({
                "question" : argv[2],
                "question_type" : "inconnu",
                "competences" : [],
                "nom_personne" : None,
                "titre_offre" : None,
                "resultat" : None,
                "reponse" : None
            })

            print(res["reponse"])

        case _:
            print("Faite -h pour plus d'aide !")

    db.close()

if __name__ == "__main__":
    main()

#"dit moi qu'elle sont les competences manquante et communes pour une offre: Alternance - Data Scientist H/F."

