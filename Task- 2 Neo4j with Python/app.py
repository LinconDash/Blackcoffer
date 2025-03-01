# Instagram-like app 
# Node : Person {name, posts_count}
# Relationship : Follows

import logging
from neo4j import GraphDatabase, RoutingControl
from neo4j.exceptions import DriverError, Neo4jError

class Instagram:
    def __init__(self, uri, user, password, database=None):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))
        self._database = database

    def close(self):
        self._driver.close()
    
    def follows(self, p1_name, p2_name):
        with self._driver.session() as session:
            result = self._create_node_and_relationship(p1_name, p2_name)
            print(f"Created relationship between : {result['p1']} and {result['p2']}")

    def _create_node_and_relationship(self, p1_name, p2_name):
        if self.find_person(p1_name):
            if self.find_person(p2_name):
                query = (
                    "MATCH (p1:Person {name : $p1_name}), (p2:Person {name : $p2_name}) "
                    "CREATE (p1)-[:FOLLOWS]->(p2) "
                    "RETURN p1.name, p2.name"
                )
            else:
                query = (
                    "CREATE (p2:Person {name: $p2_name}) "
                    "WITH p2 "  
                    "MATCH (p1:Person {name: $p1_name}) "
                    "CREATE (p1)-[:FOLLOWS]->(p2) "
                    "RETURN p1.name, p2.name"
                )
        else:
            query = (
                "CREATE (p1:Person {name : $p1_name}) "
                "CREATE (p2:Person {name : $p2_name}) "
                "CREATE (p1)-[:FOLLOWS]->(p2)"
                "RETURN p1.name, p2.name"
            )

        try:
            record = self._driver.execute_query(
                query, p1_name=p1_name, p2_name=p2_name,
                database_=self._database,
                result_transformer_=lambda r: r.single(strict=True)
            )
            return {"p1": record["p1.name"], "p2": record["p2.name"]}
        except (DriverError, Neo4jError) as exception:
            logging.error("%s raised an error: \n%s", query, exception)
            raise
    
    def find_person(self, person_name):
        names = self._find_and_return_person(person_name)
        for name in names:
            print(f"Found person: {name}")
        if names:
            return names
        return None

    def _find_and_return_person(self, person_name):
        query = (
            "MATCH (p:Person) "
            "WHERE p.name = $person_name "
            "RETURN p.name AS name"
        )
        
        names = self._driver.execute_query(
            query, person_name=person_name,
            database_=self._database, routing_=RoutingControl.READ,
            result_transformer_=lambda r: r.value("name")
        )
        return names

if __name__ == "__main__":
    scheme = "bolt"
    host_name = "localhost"
    port = 7687 
    uri = f"{scheme}://{host_name}:{port}"
    user = "neo4j"
    database = "neo4j"
    password = "password"
    app = Instagram(uri=uri, user=user, password=password, database=database)
    try:
        app.follows("Ram", "Shyam")
        app.follows("Shyam", "Ram")
        app.follows("Ram", "Gopal")
        app.follows("Gopal", "Ram")
    finally:
        app.close() 
