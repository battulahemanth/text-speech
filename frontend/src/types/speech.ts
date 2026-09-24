export type SpeechRecognitionResultLike = {
  isFinal: boolean;
  0: {
    transcript: string;
  };
};

export type SpeechRecognitionEventLike = {
  resultIndex: number;
  results: ArrayLike<SpeechRecognitionResultLike>;
};

export type SpeechRecognitionInstance = {
  continuous: boolean;
  interimResults: boolean;
  lang: string;

  start: () => void;
  stop: () => void;

  onresult:
    | ((event: SpeechRecognitionEventLike) => void)
    | null;

  onend:
    | (() => void)
    | null;

  onerror:
    | ((event: { error: string }) => void)
    | null;
};

export type SpeechRecognitionConstructor =
  new () => SpeechRecognitionInstance;

