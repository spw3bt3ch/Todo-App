import datetime
from sqlalchemy import Column, String, Integer, ForeignKey, TIMESTAMP, text
from database import Base
from sqlalchemy.orm import relationship


class Todos(Base):
    __tablename__ = "tasks"
    id = Column(Integer, index=True, primary_key=True)
    tasks = Column(String, nullable=False)
    cat_id = Column(Integer, ForeignKey("task_categories.id"))
    categories = relationship("Categories", back_populates="tasks")
    # time = Column(TIMESTAMP(timezone=True), nullable=True, server_default=text('now()'))


class Categories(Base):
    __tablename__ = "task_categories"
    id = Column(Integer, index=True, primary_key=True)
    categories = Column(String, nullable=False)

    tasks = relationship("Todos", back_populates="categories")
