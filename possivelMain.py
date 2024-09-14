import face_recognition
import cv2
import numpy as np
import requests
import json

# URL da API
API_URL = "http://127.0.0.1:8000"

# Função para buscar usuários da API
def get_usuarios():
    response = requests.get(f"{API_URL}/usuarios/")
    if response.status_code == 200:
        return response.json()  # Retorna a lista de usuários
    return []

# Função para criar um novo usuário via API
def create_usuario(nome, foto, matricula):
    data = {
        "nome": nome,
        "foto": foto,
        "matricula": matricula
    }
    response = requests.post(f"{API_URL}/usuarios/", json=data)
    return response.json()

# Carrega os usuários do banco de dados via API
usuarios = get_usuarios()

known_face_encodings = []
known_face_names = []
known_face_matriculas = []

# Processa os usuários retornados da API e carrega suas informações
for usuario in usuarios:
    imagem = face_recognition.load_image_file(usuario['foto'])
    face_encoding = face_recognition.face_encodings(imagem)[0]
    
    known_face_encodings.append(face_encoding)
    known_face_names.append(usuario['nome'])
    known_face_matriculas.append(usuario['matricula'])

print('Aprendidas as codificações de', len(known_face_encodings), 'imagens.')

video_capture = cv2.VideoCapture(0)

face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while True:
    ret, frame = video_capture.read()

    if process_this_frame:
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Desconhecido"

            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = f"{known_face_names[best_match_index]}-{known_face_matriculas[best_match_index]}"
            else:
                # Caso seja um novo rosto, adicione à API
                new_name = input("Novo rosto detectado. Digite o nome: ")
                new_path = new_name.replace(" ", "_")
                new_matricula = input("Digite a matrícula: ")
                
                # Salve a nova imagem e envie para a API
                cv2.imwrite(f"./static/images/{new_path}.jpg", frame)  # Salva a imagem
                create_usuario(new_name, f"./static/images/{new_name}.jpg", new_matricula)  # Envia para a API
                
                # Adiciona o novo rosto na lista de conhecidos
                face_encoding_new = face_recognition.face_encodings(frame)[0]
                known_face_encodings.append(face_encoding_new)
                known_face_names.append(new_name)
                known_face_matriculas.append(new_matricula)
                name = f"{new_name}-{new_matricula}"

            face_names.append(name)

    process_this_frame = not process_this_frame

    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_PLAIN
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
