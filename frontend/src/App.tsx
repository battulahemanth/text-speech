import { useState } from "react";
import { generateSpeech } from "./services/ttsService";

function App() {
  const [text, setText] = useState("");
  const [audioUrl, setAudioUrl] = useState("");
  const [loading, setLoading] = useState(false);

  const handleGenerate = async () => {
    if (!text.trim()) {
      alert("Please enter some text");
      return;
    }

    try {
      setLoading(true);

      const audioBlob = await generateSpeech(text);

      const url = URL.createObjectURL(audioBlob);
      setAudioUrl(url);
    } catch (error) {
      console.error(error);
      alert("Failed to generate speech");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1>Text to Speech</h1>

      <textarea
        value={text}
        onChange={(event) => setText(event.target.value)}
        placeholder="Enter text here..."
        rows={8}
        cols={50}
      />

      <br />

      <button onClick={handleGenerate} disabled={loading}>
        {loading ? "Generating..." : "Generate Speech"}
      </button>

      {audioUrl && (
        <div>
          <h2>Generated Audio</h2>

          <audio controls src={audioUrl}>
            Your browser does not support audio.
          </audio>

          <br />

          <a href={audioUrl} download="speech.wav">
            Download Audio
          </a>
        </div>
      )}
    </div>
  );
}

export default App;