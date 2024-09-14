# schemas.py
from pydantic import BaseModel

# Defina o schema que a API vai esperar para o usuário
class UsuarioBase(BaseModel):
    nome: str
    foto: str
    matricula: str

# Este schema será usado ao criar um novo usuário
class UsuarioCreate(UsuarioBase):
    pass

# Este schema será usado ao retornar um usuário da API
class Usuario(UsuarioBase):
    id: int

    class Config:
        orm_mode = True  # Isso permite que os dados SQLAlchemy sejam convertidos para Pydantic
