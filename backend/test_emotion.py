from app.services.emotion import analyze_text


text = """
I couldn't believe it—today was the happiest day of my life!
I finally got the job I had dreamed about for years.
But suddenly, my brother called and told me that our father was very sick.
Tears slowly filled my eyes.
Why didn't you tell me earlier? I shouted angrily.
I took a deep breath and tried to stay calm.
Everything will be alright.
"""


for item in analyze_text(text):
    print(f"\nSentence: {item['sentence']}")
    print(f"Emotion: {item['emotion']}")
