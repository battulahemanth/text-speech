type TextComposerProps = {
  text: string;
  onTextChange: (text: string) => void;

  isListening: boolean;
  speechSupported: boolean;

  liveTranscript: string;

  onToggleSpeech: () => void;
};

function TextComposer({
  text,
  onTextChange,
  isListening,
  speechSupported,
  liveTranscript,
  onToggleSpeech,
}: TextComposerProps) {
  return (
    <>
      <label className="text-field">
        <span className="text-label-row">
          <span>Text</span>

          {speechSupported && (
            <button
              type="button"
              className="microphone-button"
              onClick={onToggleSpeech}
            >
              {isListening
                ? "Stop Recording"
                : "Start Recording"}
            </button>
          )}
        </span>

        <textarea
          value={text}
          onChange={(event) =>
            onTextChange(event.target.value)
          }
          placeholder="Enter text here..."
          rows={10}
          maxLength={5000}
        />

        <small>
          {text.length}/5000
        </small>
      </label>

      {liveTranscript && (
        <p className="status">
          Listening: {liveTranscript}
        </p>
      )}

      {!speechSupported && (
        <p className="status">
          Voice-to-text is not supported in this
          browser. Try Chrome or Edge.
        </p>
      )}
    </>
  );
}

export default TextComposer;

