from transformers import pipeline

def analyze_emotions(text):
    emotion_classifier = pipeline('text-classification', model='bhadresh-savani/distilbert-base-uncased-emotion', top_k=None, device=0)
    emotion_scores = emotion_classifier(text)
    
    return emotion_scores

if __name__ == "__main__":
    text = "I am feeling depressed"
    emotions = analyze_emotions(text)
    print(emotions)
    print(f"Text: {text}")
    for emotion in emotions[0]:
        print(f"Emotion: {emotion['label']}, Score: {emotion['score']:.4f}")
