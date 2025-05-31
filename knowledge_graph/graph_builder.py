from neo4j import GraphDatabase

class GraphBuilder:
    def __init__(self, uri="bolt://localhost:7687", user="neo4j", password="password1234"):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def add_entities_and_relationships(self, entities, relationships):
        with self.driver.session() as session:
            for entity in entities:
                session.run("MERGE (e:Entity {name: $name})", name=entity)

            for subj, rel, obj in relationships:
                session.run("""
                    MATCH (a:Entity {name: $subj})
                    MATCH (b:Entity {name: $obj})
                    MERGE (a)-[:REL {type: $rel}]->(b)
                """, subj=subj, obj=obj, rel=rel)

    def find_related_entities(self, entity_name):
        with self.driver.session() as session:
            query = """
            MATCH (n:Entity {name: $name})-[:REL*1..2]-(m)
            RETURN DISTINCT m.name AS related_entity
            """
            results = session.run(query, name=entity_name)
            return [record["related_entity"] for record in results]
