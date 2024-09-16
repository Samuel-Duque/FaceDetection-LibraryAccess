"use client";
import Image from "next/image";
import { useEffect } from "react";

export default function Home() {
  useEffect(() => {
    // Atualiza o src da tag img para o feed de vídeo do backend
    const videoElement = document.getElementById("video-stream");
    videoElement.src = "http://127.0.0.1:8000/video_feed";
  }, []);
  useEffect(() => {
    const fetchUsers = async () => {
      const response = await fetch("http://127.0.0.1:8000/usuarios/");
      const data = await response.json();
      console.log(data);
    };
    fetchUsers();
  }, []);

  return (
    <div className="flex items-center justify-center sm:p-20 font-[family-name:var(--font-geist-sans)]">
      <h1>Reconhecimento Facial</h1>
      <img id="video-stream" alt="Feed de vídeo" />
    </div>
  );
}
