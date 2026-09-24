export type Voice = {
id: string;
name: string;
language: string;
model: string;
available: boolean;
};

export type Voices = Record<
string,
Voice[]

> ;

const API_BASE_URL =
"http://127.0.0.1:8000/api";

export async function getVoices(): Promise<Voices> {
const response = await fetch(
`${API_BASE_URL}/voices`,
);

if (!response.ok) {
throw new Error(
"Failed to load voices.",
);
}

return response.json();
}

