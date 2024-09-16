from fastapi import FastAPI, Depends, HTTPException, Response
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import models
import schemas 
from database import engine, get_db
import cv2


# Arruma o problema de CORS
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Adiciona o middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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


video_capture = cv2.VideoCapture(0)

# Função para gerar os frames
def generate_frames():
    while True:
        success, frame = video_capture.read()
        if not success:
            break
        else:
            # Codificar o frame em formato JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            # Usar yield para enviar o frame em formato multipart
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.get("/video_feed")
def video_feed():
    return StreamingResponse(generate_frames(), media_type="multipart/x-mixed-replace; boundary=frame")
