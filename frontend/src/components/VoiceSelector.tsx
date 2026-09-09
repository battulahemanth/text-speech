import type { Voice, Voices } from "../services/ttsService";

type Props = {
  voices: Voices;
  selectedVoice: string;
  onVoiceChange: (voice: string) => void;
};

const languageLabels: Record<keyof Voices, string> = {
  english: "English",
  hindi: "Hindi",
  telugu: "Telugu",
};

export default function VoiceSelector({
  voices,
  selectedVoice,
  onVoiceChange,
}: Props) {
  return (
    <label className="voice-field">
      <span>Voice</span>
      <select
        value={selectedVoice}
        onChange={(event) => onVoiceChange(event.target.value)}
      >
        {(Object.keys(languageLabels) as Array<keyof Voices>).map((language) => (
          <optgroup key={language} label={languageLabels[language]}>
            {voices[language].map((voice: Voice) => (
              <option key={voice.id} value={voice.id} disabled={!voice.available}>
                {voice.name}{voice.available ? "" : " (download required)"}
              </option>
            ))}
          </optgroup>
        ))}
      </select>
    </label>
  );
}
