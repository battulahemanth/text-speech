import { useEffect, useState } from "react";
import VoiceSelector from "./components/VoiceSelector";
import {
  analyzeText,
  generateSpeech,
  type EmotionSentence,
} from "./services/ttsApi";
import {
  getVoices,
  type Voices,
} from "./services/ttsService";

function App() {
  const [text, setText] = useState("");
  const [voices, setVoices] = useState<Voices | null>(null);
  const [selectedVoice, setSelectedVoice] = useState("en_US-lessac-medium");
  const [audioUrl, setAudioUrl] = useState("");
  const [emotions, setEmotions] = useState<EmotionSentence[]>([]);
  const [analyzing, setAnalyzing] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    getVoices()
      .then((voiceCatalog) => setVoices(voiceCatalog))
      .catch(() => setError("Could not load voices. Is the backend running?"));
  }, []);

  const handleGenerate = async () => {
    if (!text.trim()) {
      setError("Enter some text before generating speech.");
      return;
    }

    try {
      setLoading(true);
      setError("");

      const audioBlob = await generateSpeech(text, selectedVoice);

      if (audioUrl) {
        URL.revokeObjectURL(audioUrl);
      }
      const url = URL.createObjectURL(audioBlob);
      setAudioUrl(url);
    } catch (requestError) {
      console.error(requestError);
      setError(
        requestError instanceof Error
          ? requestError.message
          : "Failed to generate speech.",
      );
    } finally {
      setLoading(false);
    }
  };

  const handleAnalyze = async () => {
    if (!text.trim()) {
      setError("Enter some text before analyzing emotions.");
      return;
    }

    try {
      setAnalyzing(true);
      setError("");
      setEmotions(await analyzeText(text));
    } catch (requestError) {
      setError(
        requestError instanceof Error
          ? requestError.message
          : "Failed to analyze emotions.",
      );
    } finally {
      setAnalyzing(false);
    }
  };

  return (
    <main className="app-shell">
      <section className="app-header">
        <p className="eyebrow">Offline Piper Studio</p>
        <h1>Text to Speech</h1>
        <p>Write naturally, choose a downloaded voice, and generate audio locally.</p>
      </section>

      <section className="composer" aria-label="Speech composer">
        <label className="text-field">
          <span>Text</span>
          <textarea
            value={text}
            onChange={(event) => setText(event.target.value)}
            placeholder="Enter text here..."
            rows={8}
            maxLength={5000}
          />
          <small>{text.length}/5000</small>
        </label>

        {voices ? (
          <VoiceSelector
            voices={voices}
            selectedVoice={selectedVoice}
            onVoiceChange={setSelectedVoice}
          />
        ) : (
          <p className="status">Loading voices...</p>
        )}

        <button
          className="secondary-button"
          onClick={handleAnalyze}
          disabled={analyzing || !text.trim()}
        >
          {analyzing ? "Analyzing..." : "Analyze Emotions"}
        </button>

        {emotions.length > 0 && (
          <section className="emotion-panel" aria-label="Detected emotions">
            <div>
              <p className="eyebrow">Sentence analysis</p>
              <h2>Detected Emotions</h2>
            </div>
            <div className="emotion-list">
              {emotions.map((item, index) => (
                <article className="emotion-row" key={`${item.sentence}-${index}`}>
                  <span className="emotion-number">{index + 1}</span>
                  <span className="emotion-sentence">{item.sentence}</span>
                  <strong className={`emotion-tag emotion-${item.emotion}`}>
                    {item.emotion}
                  </strong>
                </article>
              ))}
            </div>
          </section>
        )}

        <button
          className="generate-button"
          onClick={handleGenerate}
          disabled={loading || !voices}
        >
          {loading ? "Generating..." : "Generate Speech"}
        </button>

        {error && <p className="error" role="alert">{error}</p>}
      </section>

      {audioUrl && (
        <section className="audio-panel">
          <div>
            <p className="eyebrow">Ready to listen</p>
            <h2>Generated Audio</h2>
          </div>

          <audio controls src={audioUrl}>
            Your browser does not support audio.
          </audio>

          <a className="download-link" href={audioUrl} download="speech.wav">
            Download WAV
          </a>
        </section>
      )}
    </main>
  );
}

export default App;