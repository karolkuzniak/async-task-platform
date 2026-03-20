from sqlalchemy.orm import Column, Integer, String
from app.database import Base

class Task(Base):
    __tablename__ = "task"

    id = Column(Integer, primary_key=Ture, index=True)
    data = Column(String)
    status = Column(String)
    result = Column(String, nullable=True)


