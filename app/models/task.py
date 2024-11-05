from models import Base, User

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship, DeclarativeBase


class Task(Base):
    __tablename__ = 'tasks'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, index=True)#- целое число, первичный ключ, с индексом.
    title = Column(String) #- строка.
    content = Column(String) #- строка.
    priority = Column(Integer, default=0) #- целое число, по умолчанию 0.
    completed = Column(Boolean, default=False) #- булевое значение, по умолчанию False.
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True) #- целое число, внешний ключ на id из таблицы 'users', не NULL, с индексом.
    slug = Column(String, unique=True, index=True) # - строка, уникальная, с индексом.
    user = relationship('User', back_populates='tasks') # - объект связи с таблицей с таблицей User, где back_populates='task



from sqlalchemy.schema import CreateTable
print(CreateTable(Task.__table__)) # type: ignore