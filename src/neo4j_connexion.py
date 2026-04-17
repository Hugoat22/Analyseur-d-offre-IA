from neo4j import GraphDatabase

class Neo4jDb:
    def __init__(self, url, user, password):
        self.url = url
        self.user = user
        self.password = password
        self.driver = GraphDatabase.driver(self.url, auth=(self.user, self.password))

    def ajouter_offre(self, offre):
        with self.driver.session() as session:
            session.run("""
                MERGE (e:Entreprise {nom: $nom}) 
                MERGE (o:Offre {titre: $titre}) 
                MERGE (e)-[:PROPOSE]->(o)
            """,
            nom=offre["entreprise"],
            titre=offre["poste"]
            )
            for competence in offre["competences"]:
                session.run("""
                    MERGE (o:Offre {titre: $titre})
                    MERGE (c:Competence {nom : $nom_comp})
                    MERGE (o)-[:DEMANDE]->(c)
                """,
                nom_comp=competence,
                titre=offre["poste"]
                )

    def ajoute_candidat(self, user):
        with self.driver.session() as session:
            for competence in user["competences"]:
                session.run("""
                    MERGE (p:Personne {nom: $nom, prenom: $prenom})
                    MERGE (c:Competence {nom : $nom_comp})
                    MERGE (p)-[:POSSEDE]->(c)
                """,
                nom=user["nom"],
                prenom=user["prenom"],
                nom_comp=competence,
                )

    def supprime_database(self):
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")

    def close(self):
        self.driver.close()

