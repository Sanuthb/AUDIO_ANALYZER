import sys
import speech_recognition as sr
import re
import json

class AudioAnalyzer:
    def __init__(self, file_path):
        self.file_path = file_path
        self.text = self.transcribe_audio()

    def transcribe_audio(self):
        recognizer = sr.Recognizer()
        with sr.AudioFile(self.file_path) as source:
            audio = recognizer.record(source)
        try:
            return recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            return "Could not understand audio"
        except sr.RequestError:
            return "Could not request results"

    def find_phone_numbers(self):
        phone_numbers = re.findall(r'\b(?:\d{1,4}[-.\s]?)?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}\b', self.text)
        return phone_numbers

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: analyze_audio.py <audio_file_path>")
        sys.exit(1)

    audio_file_path = sys.argv[1]
    analyzer = AudioAnalyzer(audio_file_path)
    result = {
        "transcription": analyzer.text,
        "phone_numbers": analyzer.find_phone_numbers()
    }
    # Output JSON
    print(json.dumps(result))
    sys.stdout.flush()
