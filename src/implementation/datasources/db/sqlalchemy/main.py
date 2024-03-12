from __future__ import annotations

from typing import Any, Dict, List, Iterator, Iterable, cast
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
    pass


class SQLSessionFactory:
    _session_factory: sessionmaker[Session]

    def __init__(self, url: str) -> None:
        self._engine = create_engine(
            url, echo=True
        )
        self._session_factory = sessionmaker(self._engine)
    
    
    def create(self) -> Session:
        return self._session_factory()
    

    def close_all(self) -> None:
        self._session_factory.close_all()

    
    def create_tables(self) -> None:
        BaseModel.metadata.create_all(self._engine)


class SQLAction:
    def __init__(
        self, 
        session: Session,
        statement: Any
    ) -> None:
        self.session = session
        self.statement = statement


    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        self.session.execute(
            self.statement, **input_data.get("kwargs", {})
        )
        self.session.commit()
        return input_data


class SQLActionWithReturns(SQLAction):
    def unpack_model(self, model: DeclarativeBase) -> Dict[str, Any]:
        tmp = model.__dict__
        tmp.pop("_sa_instance_state")
        return tmp


    def unpack_returns(self, returns: Iterable[Any]) -> Iterator[Any]:
        for i in returns:
            if isinstance(i, DeclarativeBase):
                yield self.unpack_model(i)
            elif isinstance(i, List) or isinstance(i, ScalarResult):
                yield list(self.unpack_returns(cast(List[Any], i)))
            else:
                yield i


    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        input_data["query_outputs"] = self.unpack_returns(
            self.session.scalars(
                self.statement, **input_data.get("kwargs", {})
            )
        )
        self.session.commit()
        return input_data


