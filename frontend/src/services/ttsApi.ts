export type EmotionSentence = {
sentence: string;
emotion: string;
};

const API_BASE_URL = "http://127.0.0.1:8000/api";

export async function generateSpeech(
text: string,
voice: string,
speed: number,
): Promise<Blob> {
const response = await fetch(
`${API_BASE_URL}/tts`,
{
method: "POST",
headers: {
"Content-Type": "application/json",
},
body: JSON.stringify({
text,
voice,
speed,
}),
},
);

if (!response.ok) {
const errorData = await response.json().catch(
() => null,
);


throw new Error(
  errorData?.detail ??
    "Failed to generate speech.",
);


}

return response.blob();
}

export async function analyzeText(
text: string,
): Promise<EmotionSentence[]> {
const response = await fetch(
`${API_BASE_URL}/analyze`,
{
method: "POST",
headers: {
"Content-Type": "application/json",
},
body: JSON.stringify({ text }),
},
);

if (!response.ok) {
const errorData = await response.json().catch(
() => null,
);

throw new Error(
  errorData?.detail ??
    "Failed to analyze emotions.",
);

}

const data = await response.json();

return data.sentences;
}

export async function transcribeAudioFile(
file: File,
): Promise<string> {
const formData = new FormData();

formData.append("file", file);

const response = await fetch(
`${API_BASE_URL}/transcribe`,
{
method: "POST",
body: formData,
},
);

if (!response.ok) {
const errorData = await response.json().catch(
() => null,
);


throw new Error(
  errorData?.detail ??
    "Failed to transcribe audio.",
);


}

const data = await response.json();

return data.text;
}
