
import ffmpeg
import cv2
import pygame
from src.down import download
import time




# volume = 20
# def run(url:str):
#     global volume
#     pygame.init()
#     pygame.mixer.init()
#     pygame.mixer.music.set_volume(volume/100)
#     font = pygame.font.Font(None, 25)
#     download.clear("./src/down/storage/")
#     fn = download.install(url)
#     cap = cv2.VideoCapture(fn+".mp4")
#     width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#     height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
#     screen = pygame.display.set_mode((width, height))
#     pygame.display.set_caption(url)
#     clock = pygame.time.Clock()
#     fps = cap.get(cv2.CAP_PROP_FPS)
#     # clock = pygame.time.Clock()
#     running = True
#     ffmpeg.input(fn+".mp3").output(fn+".wav").run(overwrite_output=True)
#     pygame.mixer.music.load(fn+".wav")
#     pygame.mixer.music.play()
#     msg_vl_info = 0
#     while running:
#         ret, frame = cap.read()
#         if not ret:
#             break 




#         frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
#         frame = cv2.flip(frame, 0)
#         frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         frame = pygame.surfarray.make_surface(frame)
#         screen.blit(frame, (0, 0))
#         if time.time() - msg_vl_info <= 2:
#             text_surface = font.render(f"Set Volume > {volume}%", True, (255,255,255))
#             text_rect = text_surface.get_rect(center=(80,10)) 
#             screen.blit(text_surface, text_rect)
#         pygame.display.update()
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
#             if event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_UP:
#                     msg_vl_info = time.time()
#                     if volume < 100:
#                         volume += 10
#                         pygame.mixer.music.set_volume(volume/100)
#                 elif event.key == pygame.K_DOWN:
#                     msg_vl_info = time.time()
#                     if volume > 0:
#                         volume -= 10
#                         pygame.mixer.music.set_volume(volume/100)
#             elif event.type == pygame.WINDOWMINIMIZED:
#                 # 창이 최소화 되었을 때 (처리할 게 없으면 최소한의 일을 진행)
#                 pygame.display.flip()
#             elif event.type == pygame.WINDOWFOCUSLOST:
#                 pygame.display.flip()

#         clock.tick(fps)

#     cap.release()
#     pygame.display.update()
#     pygame.display.flip()
#     pygame.init()
#     pygame.mixer.init()
#     # pygame.quit()



import pygame
from pyvidplayer2 import Video, PostProcessing




volume = 10
def run(url:str):
    global volume
# create video object
    # download.clear("./src/down/storage/")
    fns, fn = download.install(url)
    # cap = cv2.VideoCapture(fn+".mp4")
    # vids = Video(fn+".mp4")
    # 
    print()
    print()
    print()
    vid = Video(fn)

    win = pygame.display.set_mode(vid.current_size, pygame.RESIZABLE)
    font = pygame.font.Font(None, 25)
    # font = pygame.font.SysFont("arial", 30)
    # surfs = [font.render("Sharpen", True, "white")]



    # cap = cv2.VideoCapture(fn+".mp4")
    # width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
    # height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # win = pygame.display.set_mode(vid.current_size)
    pygame.display.set_caption(vid.name)
    vid.set_volume(volume/100)




    msg_vl_info = 0
    while vid.active:


        key = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                vid.stop()
            elif event.type == pygame.KEYDOWN:
                key = pygame.key.name(event.key)

        if key == "r":
            vid.restart()           #rewind video to beginning
        elif key == "p":
            vid.toggle_pause()      #pause/plays video
        elif key == "m":
            vid.toggle_mute()       #mutes/unmutes video
        elif key == "right":
            vid.seek(15)            #skip 15 seconds in video
        elif key == "left":
            vid.seek(-15)           #rewind 15 seconds in video
        elif key == "up":
            msg_vl_info = time.time()
            if volume < 100:
                volume += 10
                vid.set_volume(volume/100)
        elif key == "down":
            msg_vl_info = time.time()
            if volume > 0:
                volume -= 10
                vid.set_volume(volume/100)
        elif key == "tab":
            vid.toggle_pause() 
            text = input("Stop == [0], Search == [1], add == [2] : ")
            if text == "0":
                vid.stop()
                vid.close()
                download.clear(fns)
                pygame.display.update()
                # pygame.display.flip()
                pygame.init()
                pygame.mixer.init()
        # only draw new frames, and only update the screen if something is drawn
        # pygame.display.flip()
        if vid.draw(win, (0, 0), force_draw=True):#False
            if time.time() - msg_vl_info <= 2:
                text_surface = font.render(f"Set Volume > {volume}%", True, (255,255,255))
                text_rect = text_surface.get_rect(center=(80,10)) 
                win.blit(text_surface, text_rect)
            # durat = float(vid.num_frames) / float(fps)
            # duration = font.render(f"{vid.duration}", True, (255,255,255))
            # text_rect = duration.get_rect(center=(80,50)) 
            # win.blit(text_surface, text_rect)

            # for i, surf in enumerate(surfs):
            #     x = 320 * i
            #     vid.draw(win, (x, 0))
            #     pygame.draw.rect(win, "black", (x, 0, *surf.get_size()))
            #     win.blit(surf, (x, 0))

            pygame.display.update()

        pygame.time.wait(16) # around 60 fps


    # close video when done

    vid.close()
    download.clear(fns)
    pygame.display.update()
    # pygame.display.flip()
    pygame.init()
    pygame.mixer.init()