import requests
import io
import speech_recognition as sr
import re
import os
from moviepy.editor import AudioFileClip

def convert_to_wav(input_file_path, output_file_path):
    try:
        audio = AudioFileClip(input_file_path)
        
        audio.write_audiofile(output_file_path, codec='pcm_s16le')
        print(f"Conversion successful: {output_file_path}")
    except Exception as e:
        print(f"Error: {e}")

def download_audio(file_id, output_path):
    drive_link = f"https://drive.google.com/uc?export=download&id={file_id}"
    response = requests.get(drive_link, stream=True)
    response.raise_for_status()  
    
    with open(output_path, 'wb') as f:
        f.write(response.content)

    print("Download successful")

file_id = "1_LO6BtPBSArKLR0-qoPk-sgsQ4eer356"
input_file = "downloaded_audio.m4a"
converted_file = "downloaded_audio.wav"

download_audio(file_id, input_file)

convert_to_wav(input_file, converted_file)

recognizer = sr.Recognizer()

try:
    with sr.AudioFile(converted_file) as source:
        audio = recognizer.record(source)

    text = recognizer.recognize_google(audio)
    print(f"Recognized Text: {text}")
    
    phone_number_pattern = r'\b(?:\d{1,4}[-.\s]?)?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}\b'
    phone_numbers = re.findall(phone_number_pattern, text)
    print(f"Detected Phone Numbers: {phone_numbers}")

except sr.UnknownValueError:
    print("Google Speech Recognition could not understand the audio")
except sr.RequestError as e:
    print(f"Could not request results from Google Speech Recognition service; {e}")

os.remove(input_file)
print(f"{input_file} successfully removed")

os.remove(converted_file)
print(f"{converted_file} successfully removed")
