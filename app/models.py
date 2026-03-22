from sqlalchemy import Column, String
from app.database import Base

class Task(Base):
    __tablename__ = "task"

    id = Column(String, primary_key=True, index=True)
    data = Column(String)
    status = Column(String)
    result = Column(String, nullable=True)


