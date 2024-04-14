from __future__ import annotations

from typing import List
from typing import Optional
from sqlalchemy import (
    ForeignKey, 
    String,
    insert, 
    select
)
from sqlalchemy.orm import (
    Mapped, 
    mapped_column, 
    relationship
)

from implementation.datasources.db.sqlalchemy.main import (
    SQLSessionFactory, BaseModel, SQLAction, SQLActionWithReturns
)

class User(BaseModel):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]]
    addresses: Mapped[List[Address]] = relationship(back_populates="user")
    
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"


class Address(BaseModel):
    __tablename__ = "address"

    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]
    user_id = mapped_column(ForeignKey("user_account.id"))
    user: Mapped[User] = relationship(back_populates="addresses")
    
    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"


if __name__ == "__main__":
    s = SQLSessionFactory("sqlite+pysqlite:///:memory:")
    s.create_tables()
    session = s.create()
    SQLAction(session, insert(User)).execute({
        "kwargs": {
            "params": [{
                "name": "Boris",
                "fullname": "Razor"
            }]
        }
    })
    res = SQLActionWithReturns(
        session, select(User).where(User.id==1)
    ).execute({})
    print(list(res['query_outputs']))
    s.close_all()