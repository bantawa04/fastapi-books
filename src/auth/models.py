import uuid
from datetime import datetime
from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg

class User(SQLModel, table=True):
    __tablename__='users'
    uid: uuid.UUID = Field(
        sa_column = Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4()
        )
    )
    first_name: str
    last_name: str    
    username: str
    password: str = Field(exclude=True)
    email:str
    is_verified: bool = Field(default=False)
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at:datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    
    def __repr__(self):
        return f"<User {self.username}>"