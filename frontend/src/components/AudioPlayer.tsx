type AudioPlayerProps = {
audioUrl: string;
title?: string;
downloadName?: string;
};

function AudioPlayer({
audioUrl,
title = "Generated Audio",
downloadName = "speech.wav",
}: AudioPlayerProps) {
if (!audioUrl) {
return null;
}

return ( <section className="audio-panel"> <div> <p className="eyebrow">
Ready to listen </p>


    <h2>{title}</h2>
  </div>

  <audio controls src={audioUrl}>
    Your browser does not support audio.
  </audio>

  <a
    className="download-link"
    href={audioUrl}
    download={downloadName}
  >
    Download WAV
  </a>
</section>

);
}

export default AudioPlayer;

