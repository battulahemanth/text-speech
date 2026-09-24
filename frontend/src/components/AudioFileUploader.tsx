type AudioFileUploaderProps = {
selectedAudioFile: File | null;
transcribingFile: boolean;

onFileSelect: (
event: React.ChangeEvent<HTMLInputElement>,
) => void;

onTranscribe: () => void;
};

function AudioFileUploader({
selectedAudioFile,
transcribingFile,
onFileSelect,
onTranscribe,
}: AudioFileUploaderProps) {
return (
<> <div className="file-upload-row"> <label className="file-picker"> <span>Select audio file</span>

      <input
        type="file"
        accept="audio/*"
        onChange={onFileSelect}
      />
    </label>

    <button
      type="button"
      className="secondary-button"
      onClick={onTranscribe}
      disabled={
        !selectedAudioFile ||
        transcribingFile
      }
    >
      {transcribingFile
        ? "Transcribing..."
        : "Transcribe File"}
    </button>
  </div>

  {selectedAudioFile && (
    <p className="status">
      Selected file:{" "}
      {selectedAudioFile.name}
    </p>
  )}
</>


);
}

export default AudioFileUploader;

