import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

export type Voice = {
  id: string;
  name: string;
  language: string;
  model: string;
  available: boolean;
};

export type Voices = Record<"english" | "hindi" | "telugu", Voice[]>;

export const getVoices = async (): Promise<Voices> => {
  const response = await axios.get<Voices>(`${API_URL}/api/voices`);
  return response.data;
};