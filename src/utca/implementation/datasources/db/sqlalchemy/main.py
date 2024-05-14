from __future__ import annotations
from typing import (
    Any, Dict, List, Iterator, Iterable, Optional, Type, cast
)
from utca.core.executable_level_1.actions import Action
from sqlalchemy import (
    ScalarResult, 
    create_engine, 
)
from sqlalchemy.orm import (
    sessionmaker,
    Session,
    DeclarativeBase, 
)

class BaseModel(DeclarativeBase):
    """
    Base table model
    """
    pass


class SQLSessionFactory:
    _session_factory: sessionmaker[Session]

    def __init__(self, url: str, echo: bool=False) -> None:
        """
        Args:
            url (str): connection URL of the DB.

            echo (bool, optional): If equals to True, logs debug info. 
                Defaults to False.
        """
        self._engine = create_engine(
            url, echo=echo
        )
        self._session_factory = sessionmaker(self._engine)
    
    
    def create(self) -> Session:
        """
        Create session
        """
        return self._session_factory()
    

    def close_all(self) -> None:
        """
        Close all sessions
        """
        self._session_factory.close_all()

    
    def create_tables(self, tables_class: Type[DeclarativeBase]=BaseModel) -> None:
        """
        Create all tables

        Args:
            tables_class (Type[DeclarativeBase], optional): Base class of tables that
                will be used to trigger creation. Defaults to BaseModel.
        """
        tables_class.metadata.create_all(self._engine)


class SQLAction(Action[Dict[str, Any], None]):
    """
    SQL action without returns

    Args:
        input_data (Dict[str, Any]): Data to process. Expected keys:
            'statement' (Any): SQLAlchemy statement.
            
            'kwargs' (Dict[str, Any], optional): Extra arguments.
    """
    def __init__(
        self, 
        session: SQLSessionFactory,
        name: Optional[str]=None
    ) -> None:
        """
        Args:
            session (SQLSessionFactory): Session to use.
            
            name (Optional[str], optional): Name for identification.
                If equals to None, class name will be used. Defaults to None.
        """
        super().__init__(name)
        self.session = session


    def execute(self, input_data: Dict[str, Any]) -> None:
        """
        Args:
            input_data (Dict[str, Any]): Data to process. Expected keys:
                'statement' (Any): SQLAlchemy statement.
                
                'kwargs' (Dict[str, Any], optional): Extra arguments.

        """
        with self.session.create() as session:
            session.execute(
                input_data["statement"], **input_data.get("kwargs", {})
            )
            session.commit()


class SQLActionWithReturns(Action[Dict[str, Any], List[Any]]):
    """
    SQL action with returns
    """
    def __init__(
        self, 
        session: SQLSessionFactory,
        name: Optional[str]=None
    ) -> None:
        """
        Args:
            session (SQLSessionFactory): Session to use.
            
            name (Optional[str], optional): Name for identification.
                If equals to None, class name will be used. Defaults to None.
        """
        super().__init__(name)
        self.session = session


    def unpack_model(self, model: DeclarativeBase) -> Dict[str, Any]:
        """
        Unpack table model
        """
        tmp = model.__dict__
        tmp.pop("_sa_instance_state")
        return tmp


    def unpack_returns(self, returns: Iterable[Any]) -> Iterator[Any]:
        """
        Process returned data

        Args:
            returns (Iterable[Any]): Returned data.

        Yields:
            Iterator[Any]: Processed data.
        """
        for i in returns:
            if isinstance(i, DeclarativeBase):
                yield self.unpack_model(i)
            elif isinstance(i, List) or isinstance(i, ScalarResult):
                yield list(self.unpack_returns(cast(List[Any], i)))
            else:
                yield i


    def execute(self, input_data: Dict[str, Any]) -> List[Any]:
        """
        Args:
            input_data (Dict[str, Any]): Data to process. Expected keys:
                'statement' (Any): SQLAlchemy statement.
                
                'kwargs' (Dict[str, Any], optional): Extra arguments.
        
        Returns:
            List[Any]: Result of query.
        """
        with self.session.create() as session:
            res = self.unpack_returns(
                session.scalars(
                    input_data["statement"], **input_data.get("kwargs", {})
                )
            )
            session.commit()
            return list(res)


