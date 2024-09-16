import time
from fastapi import FastAPI, Depends, HTTPException, Response
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse
import requests
from sqlalchemy.orm import Session
import models
import schemas 
from database import engine, get_db
import cv2
import face_recognition
import numpy as np
from fastapi.middleware.cors import CORSMiddleware

API_URL = "http://127.0.0.1:8000"

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

app.mount("/static", StaticFiles(directory="static"), name="static")

def get_usuarios():
    response = requests.get(f"{API_URL}/usuarios/")
    if response.status_code == 200:
        return response.json()  
    return []

video_capture = cv2.VideoCapture(0)

name = "Desconhecido"
start_time = time.time()

# Função para capturar os usuários do banco e carregar suas faces
def load_known_faces():
    usuarios = get_usuarios()  # Assumindo que essa função já retorna usuários da API
    known_face_encodings = []
    known_face_names = []
    for usuario in usuarios:
        imagem = face_recognition.load_image_file(usuario['foto'])
        face_encoding = face_recognition.face_encodings(imagem)[0]
        known_face_encodings.append(face_encoding)
        known_face_names.append(usuario['nome'])
    return known_face_encodings, known_face_names

# Função para gerar os frames e processar reconhecimento facial
def generate_frames():
    global name
    global start_time

    known_face_encodings, known_face_names = load_known_faces()
    while True:
        success, frame = video_capture.read()
        if not success:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)


        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Desconhecido"

            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = f"{known_face_names[first_match_index]} - {known_face_matriculas[first_match_index]}"

            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = {known_face_names[best_match_index]}
                start_time = time.time()


        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.get("/video_feed")
def video_feed():
    return StreamingResponse(generate_frames(), media_type="multipart/x-mixed-replace; boundary=frame")

@app.get("/recognition_result")
def recognition_result():
    global name
    #Create a time to reset the name if the name has not changed after 30 seconds
    if time.time() - start_time > 30:
        name = "Desconhecido"



    return {"name": name, "time": start_time}
