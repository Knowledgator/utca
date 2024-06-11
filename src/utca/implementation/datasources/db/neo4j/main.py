from typing import Any, Dict, Callable, Optional

from neo4j import GraphDatabase, Session, ManagedTransaction

from utca.core.executable_level_1.actions import Action

class Neo4jClient:
    """
    Neo4j client
    """
    def __init__(
        self, 
        url: str,
        user: str,
        password: str,
    ) -> None:
        """
        Args:
            url (str): Connetcion URL.

            user (str): Authentication user.

            password (str): Authentication password.
        """
        self.driver = GraphDatabase.driver(url, auth=(user, password))


    def close(self) -> None:
        self.driver.close()

    
    def session(self, database: str) -> Session:
        return self.driver.session(database=database)
    

class Neo4jWriteAction(Action[Dict[str, Any], Any]):
    """
    Neo4j write transaction

    Args:
        input_data (Dict[str, Any]): Expected keys:
            "args" (List[Any], optional): Positional arguments for transaction function.

            "kwargs" (Dict[str, Any], optional): Keyword arguments for transaction function.

    Returns:
        Any: result of the executed transaction
    """
    def __init__(
        self, 
        database: str, 
        transaction_function: Callable[[ManagedTransaction, Any], Any], 
        client: Neo4jClient,
        name: Optional[str]=None
    ):
        """
        Args:
            database (str): Database name.

            transaction_function(Callable[[ManagedTransaction, Any], Any]): Transaction that will be executed.

            client (Neo4jClient): Client that will be used.

            name (Optional[str], optional): Name for identification.
                If equals to None, class name will be used. Defaults to None.
        """
        super().__init__(name)
        self.database = database
        self.transaction_function = transaction_function
        self.client = client


    def execute(self, input_data: Dict[str, Any]) -> Any:
        """
        Args:
            input_data (Dict[str, Any]): Expected keys:
                "args" (List[Any], optional): Positional arguments for transaction function.

                "kwargs" (Dict[str, Any], optional): Keyword arguments for transaction function.

        Returns:
            Any: result of the executed transaction
        """
        with self.client.session(self.database) as session:
            return session.execute_write(
                transaction_function=self.transaction_function,
                *(input_data.get("args", [])),
                **(input_data.get("kwargs", {})),
            )


class Neo4jReadAction(Action[Dict[str, Any], Any]):
    """
    Neo4j read transaction
    """
    def __init__(
        self, 
        database: str, 
        transaction_function: Callable[[ManagedTransaction, Any], Any], 
        client: Neo4jClient,
        name: Optional[str]=None
    ):
        """
        Args:
            database (str): Database name.

            transaction_function(Callable[[ManagedTransaction, Any], Any]): Transaction that will be executed.

            client (Neo4jClient): Client that will be used.

            name (Optional[str], optional): Name for identification.
                If equals to None, class name will be used. Defaults to None.
        """
        super().__init__(name)
        self.database = database
        self.transaction_function = transaction_function
        self.client = client


    def execute(self, input_data: Dict[str, Any]) -> Any:
        """
        Args:
            input_data (Dict[str, Any]): Expected keys:
                "args" (List[Any], optional): Positional arguments for transaction function.

                "kwargs" (Dict[str, Any], optional): Keyword arguments for transaction function.

        Returns:
            Any: result of the executed transaction
        """
        with self.client.session(self.database) as session:
            return session.execute_read(
                transaction_function=self.transaction_function,
                *(input_data.get("args", [])),
                **(input_data.get("kwargs", {})),
            )