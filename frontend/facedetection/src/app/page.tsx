"use client";
import React, { useEffect, useState } from "react";
import axios from "axios";

function App() {
  const [videoSrc, setVideoSrc] = useState("");
  const [recognizedPerson, setRecognizedPerson] = useState("");
  const [turnOn, setTurnOn] = useState(false);

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
  }, [turnOn]);

  return (
    <div className="text-3xl flex justify-center items-center flex-col gap-12 py-16 w-full max-h-screen">
      <div className="text-7xl">
        Reconhecimento <span className="">Facial</span>
      </div>
      <div>
        <button
          className={`${
            turnOn ? "bg-red-500" : "bg-green-500"
          } text-white px-4 py-2 rounded-lg pb-4`}
          onClick={() => setTurnOn(!turnOn)}
        >
          {turnOn ? "Desligar" : "Ligar"}
        </button>
      </div>
      {turnOn && (
        <>
          <div className="flex">
            <img
              src={videoSrc}
              className="rounded-lg shadow"
              alt="Camera Feed"
              // style={{ width: "100%" }}
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
        </>
      )}
    </div>
  );
}

export default App;
