from __future__ import annotations
from typing import Any, Dict, cast

from neo4j import ManagedTransaction

from utca.core import While, ExecuteFunction
from utca.implementation.datasources.db import (
    Neo4jClient, Neo4jWriteAction
)

employee_threshold=10

def employ_person_tx(tx: ManagedTransaction, name: str) -> str:
    # Create new Person node with given name, if not exists already
    result = tx.run("""
        MERGE (p:Person {name: $name})
        RETURN p.name AS name
        """, name=name
    )

    # Obtain most recent organization ID and the number of people linked to it
    result = tx.run("""
        MATCH (o:Organization)
        RETURN o.id AS id, COUNT{(p:Person)-[r:WORKS_FOR]->(o)} AS employees_n
        ORDER BY o.created_date DESC
        LIMIT 1
    """)
    org = result.single()

    if org is not None and org["employees_n"] == 0:
        raise Exception("Most recent organization is empty.")
        # Transaction will roll back -> not even Person is created!

    # If org does not have too many employees, add this Person to that
    if org is not None and org.get("employees_n") < employee_threshold:
        result = tx.run("""
            MATCH (o:Organization {id: $org_id})
            MATCH (p:Person {name: $name})
            MERGE (p)-[r:WORKS_FOR]->(o)
            RETURN $org_id AS id
            """, org_id=org["id"], name=name
        )

    # Otherwise, create a new Organization and link Person to it
    else:
        result = tx.run("""
            MATCH (p:Person {name: $name})
            CREATE (o:Organization {id: randomuuid(), created_date: datetime()})
            MERGE (p)-[r:WORKS_FOR]->(o)
            RETURN o.id AS id
            """, name=name
        )

    # Return the Organization ID to which the new Person ends up in
    return cast(str, result.single(strict=True)["id"])

if __name__ == "__main__":
    # See shell script for docker
    client = Neo4jClient(
        url="neo4j://localhost:7687",
        user="neo4j",
        password="password",
    )

    employee_id = 0
    def employee_name(_: Any) -> Dict[str, Any]:
        global employee_id
        employee_id += 1
        return {"kwargs": {"name": f"Thor{employee_id}"}}

    def print_message(input_data: Dict[str, Any]) -> None:
        print(f'User {input_data["kwargs"]["name"]} added to organization {input_data["org_id"]}')

    p = While(
        ExecuteFunction(employee_name)
        | Neo4jWriteAction(
            database="neo4j",
            transaction_function=employ_person_tx,
            client=client,
        ).use(set_key="org_id")
        | ExecuteFunction(print_message),
        max_iterations=100,
    )
    p.run()

    client.close()