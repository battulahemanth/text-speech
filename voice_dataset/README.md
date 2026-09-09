# Hemanth Telugu Voice Dataset

This folder is for collecting recordings for the custom Hemanth Telugu voice.

## Recording layout

Place one clean WAV recording per line in `audio/`. Use matching rows in `metadata.csv`:

```csv
audio_file,text,emotion,language,speaker
hemanth_0001.wav,నమస్కారం.,neutral,te-IN,hemanth
```

Recommended recording rules:

- Use 16-bit mono WAV audio.
- Keep the microphone, room, distance, and volume consistent.
- Record one sentence per file with a short silence at the beginning and end.
- Include balanced Telugu samples for neutral, happy, sad, angry, and calm delivery.
- Do not mix background music, clipping, echo, or other speakers into the recordings.

## Phase status

- Phase 1: Hemanth is registered as a Telugu voice in the backend and frontend.
- Phase 2: Add recordings to `audio/` and rows to `metadata.csv`.
- Phase 3: Train or obtain a Piper-compatible model named `hemanth.onnx` with `hemanth.onnx.json`.
- Phase 4: Copy both model files into `backend/voices/`. The existing catalog detects them automatically.
- Phases 5-7: Emotion analysis, speed/pause modulation, and React integration already exist.
- Phase 8: Test Hemanth with happy, sad, angry, and calm Telugu sentences after the model is installed.

A dataset alone is not an ONNX voice model. Training requires a Piper-compatible training workflow and sufficient licensed recordings before Phase 4 can be completed.


backend starting command : python -m uvicorn app.main:app --reload
frontend starting command : npm run dev