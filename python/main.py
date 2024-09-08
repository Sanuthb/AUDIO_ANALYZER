import requests
import io
import speech_recognition as sr
import re
import os

file_id = "1_LO6BtPBSArKLR0-qoPk-sgsQ4eer356"
# file_id="1ofDU34nlVbMgH7chanp38-iBEhU1mSnL"
drive_link = f"https://drive.google.com/uc?export=download&id={file_id}"

recognizer = sr.Recognizer()

response = requests.get(drive_link, stream=True)
response.raise_for_status()  

filename="downloaded_audio.wav"

audio_data = io.BytesIO()
for chunk in response.iter_content(chunk_size=8192):
    if chunk:
        audio_data.write(chunk)

audio_data.seek(0)

with open(filename, 'wb') as f:
    f.write(audio_data.getbuffer())

print("print download successfull")

with sr.AudioFile(filename) as source:
    audio = recognizer.record(source)

try:
    text = recognizer.recognize_google(audio)
    print(f"Recognized Text: {text}")
    
    phone_number_pattern = r'\b(?:\d{1,4}[-.\s]?)?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}\b'
    
    phone_numbers = re.findall(phone_number_pattern, text)
    print(f"Detected Phone Numbers: {phone_numbers}")

except sr.UnknownValueError:
    print("Google Speech Recognition could not understand the audio")
except sr.RequestError as e:
    print(f"Could not request results from Google Speech Recognition service; {e}")


os.remove(filename)

print(f"{filename} successfully removed")




# https://drive.google.com/file/d/1_LO6BtPBSArKLR0-qoPk-sgsQ4eer356/view?usp=drive_link