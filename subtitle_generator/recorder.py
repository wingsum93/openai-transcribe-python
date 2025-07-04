import sounddevice as sd
import scipy.io.wavfile as wav
import threading
import queue
import datetime
import os

recording_folder = "recordings"
os.makedirs(recording_folder, exist_ok=True)

def record_until_end(filename: str, samplerate=16000, channels=1):
    print("🎙️ 開始錄音，請講話...")

    q = queue.Queue()
    is_recording = True

    def callback(indata, frames, time, status):
        if status:
            print(f"⚠️ 錄音狀態：{status}")
        q.put(indata.copy())

    def wait_for_end():
        nonlocal is_recording
        while True:
            user_input = input('輸入 "end" 然後按 Enter 以結束: ')
            if user_input.strip().lower() == "end":
                is_recording = False
                break

    threading.Thread(target=wait_for_end, daemon=True).start()

    frames = []

    with sd.InputStream(samplerate=samplerate, channels=channels, callback=callback):
        while is_recording:
            frames.append(q.get())

    audio = b''.join([f.tobytes() for f in frames])
    audio_np = b''.join(frames)
    audio_data = b''.join([f.tobytes() for f in frames])

    # Convert to numpy array
    import numpy as np
    audio_array = np.concatenate(frames, axis=0)
    wav.write(filename, samplerate, audio_array)

    print(f"✅ 錄音完成，儲存為：{filename}")
    return filename
