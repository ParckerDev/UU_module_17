from models import Base, Task
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, DeclarativeBase


class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'keep_existing': True}
    id = Column(Integer, primary_key=True, index=True) # - целое число, первичный ключ, с индексом.
    username = Column(String) # - строка.
    firstname = Column(String) #- строка.
    lastname = Column(String) #- строка.
    age = Column(Integer) #- целое число.
    slug = Column(String, unique=True, index=True) #- строка, уникальная, с индексом.
    tasks = relationship('Task', back_populates='user') # - объект связи с таблицей с таблицей Task, где back_populates='user'.



from sqlalchemy.schema import CreateTable
print(CreateTable(User.__table__)) # type: ignore