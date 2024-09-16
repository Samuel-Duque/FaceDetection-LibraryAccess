# load_data.py
import json
from sqlalchemy.orm import Session
from database import engine
import models

# Função para carregar os dados do arquivo data.json
def load_json_data():
    with open('./data/data.json', 'r') as file:
        return json.load(file)

# Função para inserir os dados no banco de dados
def insert_data():
    # Carregar os dados do arquivo JSON
    data = load_json_data()

    # Criar uma sessão com o banco de dados
    session = Session(bind=engine)

    for usuario_data in data:
        # Ajustar o caminho da foto para apontar para a pasta static/images
        foto_path = f"static/images/{usuario_data['foto'].split('/')[-1]}"
        
        # Criar uma instância do modelo Usuario
        usuario = models.Usuario(
            id=usuario_data['id'],
            nome=usuario_data['nome'],
            foto=foto_path,  # Aqui ajustamos o caminho da foto
            matricula=usuario_data['matricula']
        )

        # Adicionar e confirmar a inserção no banco de dados
        session.add(usuario)

    # Salvar todas as inserções de uma vez
    session.commit()

    # Fechar a sessão
    session.close()

# Executar a função de inserção de dados
if __name__ == "__main__":
    insert_data()
    print("Dados inseridos com sucesso!")
