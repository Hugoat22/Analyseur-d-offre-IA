from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import os
from outils import *
from neo4j_connexion import Neo4jDb

load_dotenv()

db = Neo4jDb(os.getenv("URL_NEO4J"), os.getenv("DATABASE_NEO4J"), os.getenv("PASSWORD_NEO4J"))

mcp = FastMCP("Assistant Alternance")

@mcp.tool()
def recup_top_competences(top_n: int=25):
    """
        Retourne les competences les plus demandee dans les offres.

        Args:
            top_n: nombre maximun de competences a retourner.

        Returns:
            Liste des noms des competences les plus demandees.
    """
    return top_competences(db, top_n)

@mcp.tool()
def recup_offres_par_competence(competence: str):
    """
        Retourne les offres demandant une competence donnee.

        Args:
            competence: nom de la competence recherchee.

        Returns:
            Liste des titres des offres qui demandant cette competence.
    """
    return offres_par_competence(db,competence)

@mcp.tool()
def recup_lien_profil_offre(nom : str, titre: str):
    """
        Compare les competences d'un profil avec celles demandees par une offre.

        Args:
            nom: nom de la personne.
            titre: titre de l'offre.

        Returns:
            Dictionnaire contenant:
            - competences_communes 
            - competences_manquantes
    """
    return lien_profil_offre(db, nom, titre)

mcp.run()