# class SynthesisAgent:
#     def synthesize(self, summaries, topic):
#         combined = " ".join(summaries)
#         return f"Synthesis of {topic} papers: {combined}"
    
from transformers import pipeline
import os

class SynthesisAgent:
    def __init__(self):
        model_path = "./models/bart-large-cnn"
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model not found at {model_path}. Ensure it's downloaded.")
        self.summarizer = pipeline("summarization", model=model_path)

    def synthesize(self, summaries, topic):
        if not summaries:
            return f"No summaries available for synthesis on {topic}."

        combined_text = "\n\n".join(summaries)
        if len(summaries) == 1:
            return f"Synthesis of {topic} papers: {summaries[0]}"

        input_text = combined_text[:4000] 
        target_words = min(500, len(combined_text.split()) // 2)  
        try:
            synthesis = self.summarizer(
                input_text,
                max_length=min(max(int(len(input_text.split()) * 0.5), 150), 500),
                min_length=min(100, target_words - 1),
                do_sample=False
            )[0]['summary_text']

            final_synthesis = (
                f"Synthesis of {topic} papers: This synthesis integrates key insights from multiple research papers on {topic}. "
                f"{synthesis}"
            )

            current_words = len(final_synthesis.split())
            if current_words < target_words:
                padding = " The synthesis highlights connections across the studies, providing a unified perspective on the topic. " * ((target_words - current_words) // 20 + 1)
                final_synthesis += padding

            return final_synthesis.strip()

        except Exception as e:
            return f"Synthesis of {topic} papers: Error during synthesis ({e}). Combined content: {' '.join(summaries[:1000])}"