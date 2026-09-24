import type { EmotionSentence } from "../services/ttsApi";

type EmotionPanelProps = {
emotions: EmotionSentence[];
};

function EmotionPanel({
emotions,
}: EmotionPanelProps) {
if (emotions.length === 0) {
return null;
}

return ( <section
   className="emotion-panel"
   aria-label="Detected emotions"
 > <div> <p className="eyebrow">
Sentence analysis </p>


    <h2>Detected Emotions</h2>
  </div>

  <div className="emotion-list">
    {emotions.map((item, index) => (
      <article
        className="emotion-row"
        key={`${item.sentence}-${index}`}
      >
        <span className="emotion-number">
          {index + 1}
        </span>

        <span className="emotion-sentence">
          {item.sentence}
        </span>

        <strong
          className={`emotion-tag emotion-${item.emotion}`}
        >
          {item.emotion}
        </strong>
      </article>
    ))}
  </div>
</section>

);
}

export default EmotionPanel;
