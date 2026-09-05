import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

export const generateSpeech = async (text: string): Promise<Blob> => {
  const response = await axios.post(
    `${API_URL}/api/tts`,
    { text },
    {
      responseType: "blob",
    }
  );

  return response.data;
};