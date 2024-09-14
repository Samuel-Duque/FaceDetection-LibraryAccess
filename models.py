from sqlalchemy import Column, Integer, String
from database import Base, engine

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    foto = Column(String)
    matricula = Column(String)

def create_tables():
    Base.metadata.create_all(bind=engine)