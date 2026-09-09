from app.services.tts_engine import generate_emotional_speech


text = """
I couldn't believe it—today was the happiest day of my life!
I finally got the job I had dreamed about for years.
But suddenly, my brother called and told me that our father was very sick.
Tears slowly filled my eyes.
Why didn't you tell me earlier? I shouted angrily.
I took a deep breath and tried to stay calm.
Everything will be alright.
"""


generate_emotional_speech(
    text=text,
    voice_model="en_US-lessac-medium",
    output_file="speech.wav",
)

print("Speech generated successfully!")