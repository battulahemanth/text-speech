import { useEffect, useRef, useState } from "react";
import type {
  SpeechRecognitionEventLike,
  SpeechRecognitionInstance,
} from "../types/speech";

declare global {
  interface Window {
    SpeechRecognition?: new () => SpeechRecognitionInstance;
    webkitSpeechRecognition?: new () => SpeechRecognitionInstance;
  }
}

type UseSpeechRecognitionProps = {
  onTranscript: (text: string) => void;
};

export function useSpeechRecognition({
  onTranscript,
}: UseSpeechRecognitionProps) {
  const [isListening, setIsListening] = useState(false);
  const [liveTranscript, setLiveTranscript] = useState("");
  const [speechSupported, setSpeechSupported] = useState(true);
  const [error, setError] = useState("");

  const recognitionRef =
    useRef<SpeechRecognitionInstance | null>(null);

  useEffect(() => {
    const SpeechRecognitionClass =
      window.SpeechRecognition ??
      window.webkitSpeechRecognition;

    if (!SpeechRecognitionClass) {
      setSpeechSupported(false);
      return;
    }

    const recognition = new SpeechRecognitionClass();

    recognition.continuous = true;
    recognition.interimResults = true;

    // Change this later when you add language selection.
    recognition.lang = "en-US";

    recognition.onresult = (
      event: SpeechRecognitionEventLike,
    ) => {
      let interimText = "";
      let finalText = "";

      for (
        let index = event.resultIndex;
        index < event.results.length;
        index += 1
      ) {
        const result = event.results[index];

        const transcript =
          result[0].transcript.trim();

        if (!transcript) {
          continue;
        }

        if (result.isFinal) {
          finalText = finalText
            ? `${finalText} ${transcript}`
            : transcript;
        } else {
          interimText = interimText
            ? `${interimText} ${transcript}`
            : transcript;
        }
      }

      if (finalText) {
        onTranscript(finalText);
        setLiveTranscript("");
      } else if (interimText) {
        setLiveTranscript(interimText);
      }
    };

    recognition.onerror = (event) => {
      setError(
        `Speech recognition error: ${event.error}`,
      );

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
  }, [onTranscript]);

  const startListening = () => {
    if (!recognitionRef.current) {
      setError(
        "Speech recognition is not supported.",
      );
      return;
    }

    try {
      setError("");
      setLiveTranscript("");

      recognitionRef.current.start();
      setIsListening(true);
    } catch (error) {
      console.error(error);

      setError(
        "Could not start speech recognition.",
      );
    }
  };

  const stopListening = () => {
    recognitionRef.current?.stop();

    setIsListening(false);
    setLiveTranscript("");
  };

  const toggleSpeechRecognition = () => {
    if (isListening) {
      stopListening();
    } else {
      startListening();
    }
  };

  return {
    isListening,
    liveTranscript,
    speechSupported,
    error,
    startListening,
    stopListening,
    toggleSpeechRecognition,
  };
}

