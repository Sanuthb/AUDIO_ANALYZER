import requests
import re
import os
import threading
import tkinter as tk
from tkinter import messagebox
from moviepy.editor import AudioFileClip
import speech_recognition as sr
from googletrans import Translator
from concurrent.futures import ThreadPoolExecutor, as_completed

def convert_to_wav(input_file_path, output_file_path):

    try:
        audio = AudioFileClip(input_file_path)
        audio.write_audiofile(output_file_path, codec='pcm_s16le')
        return True
    except Exception as e:
        print(f"Error during conversion: {e}")
        return False

def download_audio(file_id, output_path):

    drive_link = f"https://drive.google.com/uc?export=download&id={file_id}"
    try:
        response = requests.get(drive_link, stream=True)
        response.raise_for_status()
        with open(output_path, 'wb') as f:
            f.write(response.content)
        return True
    except requests.RequestException as e:
        print(f"Error during download: {e}")
        return False

def detect_language(audio_path):
 
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_path) as source:
            audio = recognizer.record(source)
        text = recognizer.recognize_google(audio, show_all=True)
        if not text:
            return None
        return text.get('language', 'en')
    except Exception as e:
        print(f"Error during language detection: {e}")
        return None

def recognize_and_translate(audio_path, language_code, translations, phone_numbers):

    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_path) as source:
            audio = recognizer.record(source)
        
        try:
            recognizer.recognize_google(audio, show_all=True)
        except sr.UnknownValueError:
            return 'No audio'
        
        text = recognizer.recognize_google(audio, language=language_code)
        if not text.strip():
            return 'No audio'

        phone_number_pattern = r'\b(?:\d{1,4}[-.\s]?)?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}\b'
        numbers = re.findall(phone_number_pattern, text)
        if numbers:
            phone_numbers.append(numbers[0])

        if not phone_numbers:
            translator = Translator()
            translated_text = translator.translate(text, src=language_code, dest='en').text
            translations[language_code] = translated_text

        return 'Processed successfully'

    except sr.UnknownValueError:
        return 'No audio'
    except sr.RequestError as e:
        print(f"Request error for {language_code}: {e}")
        return 'Error'

def process_audio():
    full_link = entry.get()
    file_id_match = re.search(r'/d/([a-zA-Z0-9_-]+)', full_link)
    if not file_id_match:
        messagebox.showerror("Error", "Invalid Google Drive link format.")
        return

    file_id = file_id_match.group(1)
    input_file = "downloaded_audio.m4a"
    converted_file = "downloaded_audio.wav"

    result.set("Downloading and processing audio...")

    if not download_audio(file_id, input_file):
        messagebox.showerror("Error", "Failed to download the audio file.")
        return
    
    if not convert_to_wav(input_file, converted_file):
        messagebox.showerror("Error", "Failed to convert audio file to WAV format.")
        return

    detected_language = detect_language(converted_file)
    if not detected_language:
        messagebox.showerror("Error", "Could not detect the language of the audio.")
        return

    languages = ['en', 'ta', 'kn']

    translations = {}
    phone_numbers = []

    with ThreadPoolExecutor(max_workers=len(languages)) as executor:
        future_to_lang = {executor.submit(recognize_and_translate, converted_file, lang, translations, phone_numbers): lang for lang in languages}
        for future in as_completed(future_to_lang):
            status = future.result()
            print(f"Processing status: {status}")

    if phone_numbers:
        result.set(f"Best Phone Number: {phone_numbers[0]}")
    else:
        best_translation = translations.get(detected_language, 'No translation found')
        result.set(f"Best Translation: {best_translation}")

    os.remove(input_file)
    os.remove(converted_file)

root = tk.Tk()
root.title("Audio Processor")

tk.Label(root, text="Enter Google Drive Link:").pack(pady=10)
entry = tk.Entry(root, width=50)
entry.pack(pady=5)

result = tk.StringVar()
tk.Label(root, textvariable=result, wraplength=500).pack(pady=10)

tk.Button(root, text="Process Audio", command=process_audio).pack(pady=20)

root.mainloop()
