"use client";
import React, { useEffect, useState } from "react";
import axios from "axios";

function App() {
  const [videoSrc, setVideoSrc] = useState("");
  const [recognizedPerson, setRecognizedPerson] = useState("");
  const [nome, setNome] = useState("");
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [matricula, setMatricula] = useState("");
  const [capturedImage, setCapturedImage] = useState("");

  useEffect(() => {
    // URL do streaming de vídeo
    setVideoSrc("http://127.0.0.1:8000/video_feed");

    // Atualiza a pessoa reconhecida (se necessário, pode ser via WebSocket ou outro método)
    const fetchRecognitionResults = async () => {
      try {
        const response = await axios.get(
          "http://127.0.0.1:8000/recognition_result"
        );
        setRecognizedPerson(response.data.name);
      } catch (error) {
        console.error(
          "Erro ao buscar resultados de reconhecimento facial",
          error
        );
      }
    };

    const intervalId = setInterval(fetchRecognitionResults, 5000);

    return () => clearInterval(intervalId); // Limpa o intervalo ao desmontar o componente
  }, []);

  const captureFrame = async () => {
    try {
      const response = await axios.get("http://127.0.0.1:8000/capturar_frame");
      setCapturedImage(response.data.image_path);
    } catch (error) {
      console.error("Erro ao capturar o frame", error);
    }
  };

  const registerPerson = async () => {
    try {
      console.log("Registrando pessoa", nome, matricula);
      const response = await axios.post(
        "http://127.0.0.1:8000/registrar_usuario",
        {
          nome: nome,
          matricula: matricula,
        }
      );
      alert("Pessoa registrada com sucesso!");
    } catch (error) {
      console.error("Erro ao registrar pessoa", error);
    }
  };
  const openModal = () => {
    setIsModalOpen(true);
  };
  const closeModal = () => {
    setIsModalOpen(false);
    setNome("");
    setMatricula("");
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center gap-12 py-16 w-full max-h-screen">
      <div className="flex space-x-4 mt-6">
        <button
          onClick={captureFrame}
          className="bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded-lg shadow"
        >
          Capturar Foto
        </button>
        <button
          onClick={openModal}
          disabled={!capturedImage}
          className={`py-2 px-4 rounded-lg shadow ${
            capturedImage
              ? "bg-green-500 hover:bg-green-600 text-white"
              : "bg-gray-300 text-gray-500 cursor-not-allowed"
          }`}
        >
          Registrar
        </button>
      </div>

      <div className="w-full max-w-2xl p-4 rounded-lg shadow-lg">
        <img
          src={videoSrc}
          alt="Camera Feed"
          className="w-full max-h-80 object-cover rounded-lg"
        />
      </div>
      <div>
        {recognizedPerson && recognizedPerson != "Desconhecido" ? (
          <h2>
            Reconhecido:
            {<span className="text-green-400"> {recognizedPerson}</span>}
          </h2>
        ) : (
          <h2 className="animated-dots animate-pulse">
            Aguardando reconhecimento
          </h2>
        )}
      </div>
      {isModalOpen && (
        <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
          <div className="bg-white rounded-lg p-8 shadow-lg w-full max-w-md">
            <span
              className="text-gray-500 text-2xl cursor-pointer absolute top-4 right-4"
              onClick={closeModal}
            >
              &times;
            </span>
            <h2 className="text-2xl font-bold mb-4">Registrar Nova Pessoa</h2>
            <input
              type="text"
              placeholder="Nome"
              value={nome}
              onChange={(e) => setNome(e.target.value)}
              className="border text-gray-700 border-gray-300 rounded-lg w-full py-2 px-4 mb-4 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <input
              type="text"
              placeholder="Matrícula"
              value={matricula}
              onChange={(e) => setMatricula(e.target.value)}
              className="border text-gray-700 border-gray-300 rounded-lg w-full py-2 px-4 mb-4 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <button
              onClick={registerPerson}
              className="bg-green-500 hover:bg-green-600 text-white py-2 px-4 rounded-lg w-full"
            >
              Registrar
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
