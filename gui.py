import ffmpeg
import cv2
import pygame
import download
import time
volume = 20
def run(url:str):
    global volume
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.set_volume(volume/100)
    font = pygame.font.Font(None, 25)
    download.clear("storage")
    fn = download.install(url)
    cap = cv2.VideoCapture(fn+".mp4")
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(url)
    clock = pygame.time.Clock()
    fps = cap.get(cv2.CAP_PROP_FPS)
    running = True
    ffmpeg.input(fn+".mp3").output(fn+".wav").run(overwrite_output=True)
    pygame.mixer.music.load(fn+".wav")
    pygame.mixer.music.play()
    msg_vl_info = 0
    while running:
        ret, frame = cap.read()
        if not ret:
            break 
        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        frame = cv2.flip(frame, 0)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = pygame.surfarray.make_surface(frame)
        screen.blit(frame, (0, 0))
        if time.time() - msg_vl_info <= 2:
            text_surface = font.render(f"Set Volume > {volume}%", True, (255,255,255))
            text_rect = text_surface.get_rect(center=(80,10)) 
            screen.blit(text_surface, text_rect)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    msg_vl_info = time.time()
                    if volume < 100:
                        volume += 10
                        pygame.mixer.music.set_volume(volume/100)
                elif event.key == pygame.K_DOWN:
                    msg_vl_info = time.time()
                    if volume > 0:
                        volume -= 10
                        pygame.mixer.music.set_volume(volume/100)
        clock.tick(fps)
    cap.release()
    pygame.quit()