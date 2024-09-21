import ffmpeg
import cv2
import pygame
import download
import time

pygame.init()
pygame.mixer.init()

download.clear("storage")
url = input("Please enter the URL to play the video (youtube url) : ")
fn = download.install_nogui(url)
ffmpeg.input(fn+".mp3").output(fn+".wav").run(overwrite_output=True)
sound = pygame.mixer.Sound(fn+".wav")
sound.play()
while pygame.mixer.get_busy(): 
    pygame.time.delay(100)
pygame.quit()