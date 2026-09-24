import type { Voices } from "../services/ttsService";

type VoiceSelectorProps = {
voices: Voices;
selectedVoice: string;
onVoiceChange: (voice: string) => void;
};

function VoiceSelector({
voices,
selectedVoice,
onVoiceChange,
}: VoiceSelectorProps) {
return ( <label className="voice-field"> <span>Voice</span>

  <select
    value={selectedVoice}
    onChange={(event) =>
      onVoiceChange(event.target.value)
    }
  >
    {Object.entries(voices).map(
      ([language, languageVoices]) => (
        <optgroup
          key={language}
          label={language}
        >
          {languageVoices
            .filter((voice) => voice.available)
            .map((voice) => (
              <option
                key={voice.id}
                value={voice.id}
              >
                {voice.name}
              </option>
            ))}
        </optgroup>
      ),
    )}
  </select>
</label>

);
}

export default VoiceSelector;
