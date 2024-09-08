import pyaudio
import wave
import sys
import os

def record_audio(filename, duration=5, channels=1, rate=44100, chunk=1024):
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=channels,
                    rate=rate,
                    input=True,
                    frames_per_buffer=chunk)

    frames = []
    for _ in range(0, int(rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    # Ensure the directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    # Save the audio file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()

    return filename

if __name__ == "__main__":
    output_directory = "pythonoutput"
    output_filename = os.path.join(output_directory, "output.wav")
    record_audio(output_filename, duration=10)
    print("output.wav")
    sys.stdout.flush()
