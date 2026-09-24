import { useEffect, useRef, useState } from "react";
import TextComposer from "../components/TextComposer";
import VoiceSelector from "../components/VoiceSelector";
import AudioFileUploader from "../components/AudioFileUploader";
import EmotionPanel from "../components/EmotionPanel";
import AudioPlayer from "../components/AudioPlayer";
import {
  analyzeText,
  generateSpeech,
  transcribeAudioFile,
  type EmotionSentence,
} from "../services/ttsApi";
import { getVoices, type Voices } from "../services/ttsService";

type SpeechRecognitionResultLike = {
  isFinal: boolean;
  0: { transcript: string };
};

type SpeechRecognitionEventLike = {
  resultIndex: number;
  results: ArrayLike<SpeechRecognitionResultLike>;
};

type SpeechRecognitionInstance = {
  continuous: boolean;
  interimResults: boolean;
  lang: string;
  start: () => void;
  stop: () => void;
  onresult: ((event: SpeechRecognitionEventLike) => void) | null;
  onend: (() => void) | null;
  onerror: ((event: { error: string }) => void) | null;
};

declare global {
  interface Window {
    SpeechRecognition?: new () => SpeechRecognitionInstance;
    webkitSpeechRecognition?: new () => SpeechRecognitionInstance;
  }
}

function HomePage() {
  const [text, setText] = useState("");
  const [voices, setVoices] = useState<Voices | null>(null);
  const [selectedVoice, setSelectedVoice] = useState("en_US-lessac-medium");
  const [voiceSpeed, setVoiceSpeed] = useState(1);
  const [audioUrl, setAudioUrl] = useState("");
  const [emotions, setEmotions] = useState<EmotionSentence[]>([]);
  const [analyzing, setAnalyzing] = useState(false);
  const [loading, setLoading] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [isRecording, setIsRecording] = useState(false);
  const [transcribingFile, setTranscribingFile] = useState(false);
  const [liveTranscript, setLiveTranscript] = useState("");
  const [speechSupported, setSpeechSupported] = useState(true);
  const [selectedAudioFile, setSelectedAudioFile] = useState<File | null>(null);
  const [error, setError] = useState("");
  const recognitionRef = useRef<SpeechRecognitionInstance | null>(null);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const mediaStreamRef = useRef<MediaStream | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);
  const [recordedAudioUrl, setRecordedAudioUrl] = useState("");

  useEffect(() => {
    getVoices()
      .then((voiceCatalog) => setVoices(voiceCatalog))
      .catch(() => setError("Could not load voices. Is the backend running?"));

    const SpeechRecognitionClass =
      window.SpeechRecognition ?? window.webkitSpeechRecognition;

    if (!SpeechRecognitionClass) {
      setSpeechSupported(false);
      return;
    }

    const recognition = new SpeechRecognitionClass();
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.lang = "en-US";

    recognition.onresult = (event: SpeechRecognitionEventLike) => {
      let interimText = "";
      let finalText = "";

      for (let index = event.resultIndex; index < event.results.length; index += 1) {
        const result = event.results[index];
        const transcript = result[0].transcript.trim();

        if (!transcript) continue;

        if (result.isFinal) {
          finalText = finalText ? `${finalText} ${transcript}` : transcript;
        } else {
          interimText = interimText ? `${interimText} ${transcript}` : transcript;
        }
      }

      if (finalText) {
        setText((currentText) => {
          const separator =
            currentText && !currentText.trimEnd().endsWith(" ") ? " " : "";
          return `${currentText}${separator}${finalText}`;
        });
        setLiveTranscript("");
      } else if (interimText) {
        setLiveTranscript(interimText);
      }
    };

    recognition.onerror = (event: { error: string }) => {
      setError(`Speech recognition error: ${event.error}`);
      setIsListening(false);
    };

    recognition.onend = () => {
      setIsListening(false);
      setLiveTranscript("");
    };

    recognitionRef.current = recognition;

    return () => {
      recognition.stop();
      recognition.onresult = null;
      recognition.onerror = null;
      recognition.onend = null;
    };
  }, []);

  const stopRecordingMedia = () => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state !== "inactive") {
      mediaRecorderRef.current.stop();
    }

    if (mediaStreamRef.current) {
      mediaStreamRef.current.getTracks().forEach((track) => track.stop());
      mediaStreamRef.current = null;
    }

    mediaRecorderRef.current = null;
    setIsRecording(false);
  };

  const toggleSpeechToText = async () => {
    if (!speechSupported || !recognitionRef.current) {
      setError("Speech-to-text is not supported in this browser.");
      return;
    }

    if (isListening) {
      recognitionRef.current.stop();
      setIsListening(false);
      setLiveTranscript("");
      stopRecordingMedia();
      return;
    }

    try {
      setError("");
      setLiveTranscript("");
      audioChunksRef.current = [];

      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaStreamRef.current = stream;

      const recorder = new MediaRecorder(stream);
      mediaRecorderRef.current = recorder;

      recorder.ondataavailable = (event: BlobEvent) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      recorder.onstop = () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: "audio/webm" });

        if (recordedAudioUrl) {
          URL.revokeObjectURL(recordedAudioUrl);
        }

        setRecordedAudioUrl(URL.createObjectURL(audioBlob));
      };

      recorder.start();
      setIsRecording(true);
      recognitionRef.current.start();
      setIsListening(true);
    } catch {
      setIsListening(false);
      setIsRecording(false);
      setError("Microphone access is blocked or unavailable. Please allow access and try again.");
    }
  };

  const handleAudioFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0] ?? null;
    setSelectedAudioFile(file);

    if (file) {
      setError("");
    }
  };

  const handleFileTranscription = async () => {
    if (!selectedAudioFile) {
      setError("Select an audio file before transcribing.");
      return;
    }

    try {
      setTranscribingFile(true);
      setError("");
      const transcript = await transcribeAudioFile(selectedAudioFile);
      setText((currentText) => {
        const trimmed = transcript.trim();
        if (!trimmed) {
          return currentText;
        }
        const separator =
          currentText && !currentText.trimEnd().endsWith(" ") ? " " : "";
        return `${currentText}${separator}${trimmed}`;
      });
    } catch (requestError) {
      setError(
        requestError instanceof Error
          ? requestError.message
          : "Failed to transcribe the selected file.",
      );
    } finally {
      setTranscribingFile(false);
    }
  };

  const handleGenerate = async () => {
    if (!text.trim()) {
      setError("Enter some text before generating speech.");
      return;
    }

    try {
      setLoading(true);
      setError("");

      const audioBlob = await generateSpeech(text, selectedVoice, voiceSpeed);

      if (audioUrl) {
        URL.revokeObjectURL(audioUrl);
      }

      setAudioUrl(URL.createObjectURL(audioBlob));
    } catch (requestError) {
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
        <TextComposer
          text={text}
          onTextChange={setText}
          isListening={isListening}
          speechSupported={speechSupported}
          liveTranscript={liveTranscript}
          onToggleSpeech={toggleSpeechToText}
        />

        <AudioFileUploader
          selectedAudioFile={selectedAudioFile}
          transcribingFile={transcribingFile}
          onFileSelect={handleAudioFileSelect}
          onTranscribe={handleFileTranscription}
        />

        <div className="settings-grid">
          {voices ? (
            <VoiceSelector
              voices={voices}
              selectedVoice={selectedVoice}
              onVoiceChange={setSelectedVoice}
            />
          ) : (
            <p className="status">Loading voices...</p>
          )}

          <label className="voice-field speed-field">
            <span>Voice Speed</span>
            <select
              value={voiceSpeed}
              onChange={(event) => setVoiceSpeed(Number(event.target.value))}
            >
              <option value={0.5}>0.5x</option>
              <option value={1}>1x</option>
              <option value={1.5}>1.5x</option>
            </select>
          </label>
        </div>

        <button
          type="button"
          className="secondary-button"
          onClick={handleAnalyze}
          disabled={analyzing || !text.trim()}
        >
          {analyzing ? "Analyzing..." : "Analyze Emotions"}
        </button>

        <EmotionPanel emotions={emotions} />

        <button
          type="button"
          className="generate-button"
          onClick={handleGenerate}
          disabled={loading || !voices || isListening}
        >
          {loading ? "Generating..." : "Generate Speech"}
        </button>

        {error && <p className="error" role="alert">{error}</p>}
      </section>

      <AudioPlayer
        audioUrl={audioUrl}
        title="Generated Audio"
        downloadName="speech.wav"
      />

      {recordedAudioUrl && (
        <section className="audio-panel">
          <div>
            <p className="eyebrow">Recorded audio</p>
            <h2>Your speech recording</h2>
          </div>

          <audio controls src={recordedAudioUrl}>
            Your browser does not support audio.
          </audio>

          <a className="download-link" href={recordedAudioUrl} download="recording.webm">
            Download recording
          </a>
        </section>
      )}
    </main>
  );
}

export default HomePage;