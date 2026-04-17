
def top_competences(db, top_n=25):
    top_comp = []
    data, _, _ = db.driver.execute_query("""
        MATCH (:Offre)-[:DEMANDE]->(c:Competence)
        RETURN c as competences,count(*) as nbr
        ORDER BY nbr DESC
        """)
    for competence in data:
        top_comp.append(competence["competences"]["nom"])
    return top_comp[:top_n]

def offres_par_competence(db, competence):
    offres = set()
    data, _, _ = db.driver.execute_query("""
        MATCH (o:Offre)-[:DEMANDE]->(:Competence {nom: $competence})
        RETURN o as offres
        """,
        competence=competence
        )
    for offre in data:
        offres.add(offre["offres"]["titre"])
    return list(offres)

def lien_profil_offre(db, nom, titre):
    data, _, _ = db.driver.execute_query("""
        MATCH (p:Personne {nom: $nom})
        MATCH (o:Offre {titre: $titre})

        OPTIONAL MATCH (p)-[:POSSEDE]->(c1:Competence)<-[:DEMANDE]-(o)
        WITH o, collect(DISTINCT c1) as comp_commun
                             
        MATCH (o)-[:DEMANDE]->(c2:Competence)
        WHERE NOT c2 IN comp_commun 
                             
        RETURN comp_commun, collect(DISTINCT c2) as comp_manquant
        """,
        nom=nom,
        titre=titre
        )
    comp = {}
    if data:
        comp["competences_communes"] = [comp_c["nom"] for comp_c in data[0]["comp_commun"]]
        comp["competences_manquantes"] = [comp_m["nom"] for comp_m in data[0]["comp_manquant"]]
    return comp