from gtts import gTTS
import os
import re

class AudioAgent:
    def _sanitize_text(self, text):
        """
        Remove or replace characters that gTTS can't handle.
        Keeps ASCII printable characters, basic punctuation, and spaces.
        """
        sanitized = re.sub(r'[^\x20-\x7E]', ' ', text)  
        sanitized = re.sub(r'\s+', ' ', sanitized).strip()
        return sanitized

    def generate_podcast(self, text, output_path):
        clean_text = self._sanitize_text(text)
        if not clean_text:
            clean_text = "No content available for audio generation."
        tts = gTTS(text=clean_text, lang='en')
        tts.save(output_path)
        return output_path