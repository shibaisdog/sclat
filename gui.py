import ffmpeg
import cv2
import pygame
import download
import time

pygame.init()
pygame.mixer.init()

download.clear("storage")
url = input("Please enter the URL to play the video (youtube url) : ")
fn = download.install(url)
cap = cv2.VideoCapture(fn+".mp4")
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption(url)
clock = pygame.time.Clock()
fps = cap.get(cv2.CAP_PROP_FPS)
running = True
start_time = time.time()
ffmpeg.input(fn+".mp3").output(fn+".wav").run(overwrite_output=True)
pygame.mixer.music.load(fn+".wav")
pygame.mixer.music.play()
while running:
    ret, frame = cap.read()
    if not ret:
        break 
    frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
    frame = cv2.flip(frame, 0)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = pygame.surfarray.make_surface(frame)
    screen.blit(frame, (0, 0))
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    clock.tick(fps)
cap.release()
pygame.quit()