const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

export type EmotionSentence = {
  sentence: string;
  emotion: string;
  speed: number;
  pause: number;
};

export async function generateSpeech(
  text: string,
  voice: string,
): Promise<Blob> {
  const response = await fetch(`${API_URL}/api/tts`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Accept: "audio/wav",
    },
    body: JSON.stringify({ text, voice }),
  });

  if (!response.ok) {
    let errorMessage = "Failed to generate speech";

    try {
      const errorData = (await response.json()) as { detail?: string };
      errorMessage = errorData.detail || errorMessage;
    } catch {
      // The server may return a non-JSON error response.
    }

    throw new Error(errorMessage);
  }

  return response.blob();
}

export async function analyzeText(text: string): Promise<EmotionSentence[]> {
  const response = await fetch(`${API_URL}/api/analyze`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text }),
  });

  if (!response.ok) {
    let errorMessage = "Failed to analyze emotions";
    try {
      const errorData = (await response.json()) as { detail?: string };
      errorMessage = errorData.detail || errorMessage;
    } catch {
      // The server may return a non-JSON error response.
    }
    throw new Error(errorMessage);
  }

  const data = (await response.json()) as { sentences: EmotionSentence[] };
  return data.sentences;
}
