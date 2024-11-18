from moviepy.editor import AudioFileClip
import pygame
from src.down import download
import os

def run(url:str):
    pygame.init()
    pygame.mixer.init()
    download.clear("./src/down/storage/")
    fn = download.install_nogui(url)
    mp3_path = fn + ".mp3"
    wav_path = fn + ".wav"
    if not os.path.exists(mp3_path):
        print(f"Error: MP3 file not found at {mp3_path}")
        return  
    if os.path.getsize(mp3_path) == 0:
        print("Error: Downloaded MP3 file is empty")
        return    
    try:
        audio = AudioFileClip(mp3_path)
        audio.write_audiofile(wav_path, verbose=False, logger=None)
        audio.close()
        if not os.path.exists(wav_path):
            print("Error: WAV conversion failed")
            return
        sound = pygame.mixer.Sound(wav_path)
        sound.play()
        while pygame.mixer.get_busy(): 
            pygame.time.delay(100)
    except Exception as e:
        print(f"Error processing audio: {str(e)}")
    finally:
        pygame.quit()