from transformers import pipeline
import os

class ClassificationAgent:
    def __init__(self, topics):
        self.topics = topics  # ["AI", "Physics", "Biology"]
        model_path = "./models/bart-large-mnli"
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model not found at {model_path}. Run the download script first.")
        self.classifier = pipeline("zero-shot-classification", model=model_path, device=-1)  # CPU

    def classify(self, content):
        content = content[:1000]
        try:
            result = self.classifier(content, candidate_labels=self.topics)
            return result['labels'][0]
        except Exception as e:
            print(f"Classification error: {e}. Defaulting to {self.topics[0]}.")
            return self.topics[0] 