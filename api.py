# api.py
from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import models
import schemas  # Importando os schemas Pydantic
from database import engine, get_db

app = FastAPI()

# Cria as tabelas no banco
models.create_tables()

app.mount("/static", StaticFiles(directory="static"), name="static")


# Endpoint para listar os usuários
@app.get("/usuarios/", response_model=list[schemas.Usuario])
def read_usuarios(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    usuarios = db.query(models.Usuario).offset(skip).limit(limit).all()
    return usuarios

# Endpoint para criar um novo usuário
@app.post("/usuarios/", response_model=schemas.Usuario)
def create_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    db_usuario = models.Usuario(**usuario.dict())  # Converte os dados Pydantic para o formato SQLAlchemy
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

# Endpoint para buscar um usuário específico pelo ID
@app.get("/usuarios/{usuario_id}", response_model=schemas.Usuario)
def read_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario

# Endpoint para deletar um usuário específico pelo ID
@app.delete("/usuarios/{usuario_id}", response_model=schemas.Usuario)
def delete_usuario(usuario_id: int, db: Session = Depends(get_db)):
    # Busca o usuário no banco de dados
    usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    # Remove o usuário do banco de dados
    db.delete(usuario)
    db.commit()
    
    return usuario