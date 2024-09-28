import pygame,chardet,time,re
import pygame.scrap
from pyvidplayer2 import Video
################################
from src.down import download
import src.down
import src.down.download
import src.win.screen
import src.win.setting
search = ""
pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
def is_url(url: str) -> bool:
    match = re.search(pattern, url)
    return bool(match)

def run(url:str):
    fns, fn = download.install(url)
    src.win.screen.vid = Video(fn)
    src.win.screen.reset((src.win.screen.vid.current_size[0],src.win.screen.vid.current_size[1]+5))
    pygame.display.set_caption(src.win.screen.vid.name)
    src.win.screen.vid.set_volume(src.win.setting.volume/100)
    msg_info = 0
    msg_value = ""
    while src.win.screen.vid.active:
        key = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                src.win.screen.vid.stop()
            elif event.type == pygame.KEYDOWN:
                key = pygame.key.name(event.key)
        if src.win.screen.load == 2: # play
            if key == "r":
                src.win.screen.vid.restart()
            elif key == "p":
                src.win.screen.vid.toggle_pause()
            elif key == "m":
                src.win.screen.vid.toggle_mute()
            elif key == "l":
                msg_info = time.time()
                msg_value = "loop"
                src.win.setting.loop = not src.win.setting.loop
            elif key == "right":
                src.win.screen.vid.seek(15)
            elif key == "left":
                src.win.screen.vid.seek(-15)
            elif key == "up":
                msg_info = time.time()
                msg_value = "volume"
                if src.win.setting.volume < 100:
                    src.win.setting.volume += 10
                    src.win.screen.vid.set_volume(src.win.setting.volume/100)
            elif key == "down":
                msg_info = time.time()
                msg_value = "volume"
                if src.win.setting.volume > 0:
                    src.win.setting.volume -= 10
                    src.win.screen.vid.set_volume(src.win.setting.volume/100)
            if src.win.screen.vid.draw(src.win.screen.win, (0, 0), force_draw=True):
                if time.time() - msg_info <= 2:
                    if msg_value == "volume":
                        text_surface = src.win.screen.font.render(f"Set Volume > {src.win.setting.volume}%", True, (255,255,255))
                    elif msg_value == "loop":
                        text_surface = src.win.screen.font.render(f"Set Loop > {src.win.setting.loop}", True, (255,255,255))
                    else:
                        text_surface = src.win.screen.font.render("", True, (255,255,255))
                    text_rect = text_surface.get_rect(center=(80,10)) 
                    src.win.screen.win.blit(text_surface, text_rect)
                current_time = src.win.screen.vid.get_pos()
                total_length = src.win.screen.vid.duration
                rect_coords = (0, src.win.screen.win.get_size()[1] - 5, src.win.screen.win.get_size()[0], 5)
                pygame.draw.rect(src.win.screen.win, (100, 100, 100), rect_coords)
                linebar = (current_time / total_length) * src.win.screen.win.get_size()[0]
                rect_coords = (0, src.win.screen.win.get_size()[1] - 5, linebar, 5)
                pygame.draw.rect(src.win.screen.win, (255, 0, 0), rect_coords)
                pygame.display.update()
                caps = f"[{current_time:.2f}s / {total_length:.2f}s] {src.win.screen.vid.name}"
                pygame.display.set_caption(caps)
        pygame.time.wait(16)
    src.win.screen.vid.close()
    download.clear(fns)
    pygame.display.update()

def wait():
    global search
    if src.win.screen.vid == None:
        src.win.screen.reset((700,400))
    else:
        src.win.screen.reset((src.win.screen.vid.current_size[0],src.win.screen.vid.current_size[1]+5))
    pygame.scrap.init()
    while True:
        src.win.screen.win.fill((0, 0, 0))
        key = None
        if len(src.win.setting.video_list) == 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                elif event.type == pygame.KEYDOWN:
                    key = pygame.key.name(event.key)
                    if event.key == pygame.K_v and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                        if pygame.scrap.get_init():
                            copied_text = pygame.scrap.get(pygame.SCRAP_TEXT)
                            if copied_text:
                                try:
                                    copied_text = copied_text.decode('utf-8').strip('\x00')
                                except UnicodeDecodeError:
                                    detected = chardet.detect(copied_text)
                                    encoding = detected['encoding']
                                    copied_text = copied_text.decode(encoding).strip('\x00')
                                search += copied_text
                                continue
            if not key:
                text_surface = src.win.screen.font.render(f"search video : {search}", True, (255,255,255))
                text_rect = text_surface.get_rect(center=(src.win.screen.win.get_size()[0]/2,src.win.screen.win.get_size()[1]/2)) 
                src.win.screen.win.blit(text_surface, text_rect)
                pygame.display.update()
                continue
            elif key == "backspace":
                search = search[0:len(search)-1]
            elif len(key) == 1:
                search = search + key
            text_surface = src.win.screen.font.render(f"search video : {search}", True, (255,255,255))
            text_rect = text_surface.get_rect(center=(src.win.screen.win.get_size()[0]/2,src.win.screen.win.get_size()[1]/2)) 
            src.win.screen.win.blit(text_surface, text_rect)
            pygame.display.update()
            if key == "enter" or key == "return":
                if is_url(search):
                    a = search
                    search = ""
                    trys = 0
                    while True:
                        try:
                            run(a)
                            break
                        except Exception as e:
                            if src.win.screen.vid == None:
                                src.win.screen.reset((700,400))
                            else:
                                src.win.screen.reset((src.win.screen.vid.current_size[0],src.win.screen.vid.current_size[1]+5))
                            if trys >= 10:
                                print("fail")
                                break
                            print(f"An error occurred during playback. Trying again... ({trys}/10) > \n{e}")
                            text_surface = src.win.screen.font.render(f"An error occurred during playback. Trying again... ({trys}/10) >", True, (255,255,255))
                            text_surface_2 = src.win.screen.font.render(f"{e}", True, (255,255,255))
                            text_rect = text_surface.get_rect(center=(src.win.screen.win.get_size()[0]/2,src.win.screen.win.get_size()[1]/2)) 
                            text_rect_2 = text_surface_2.get_rect(center=(src.win.screen.win.get_size()[0]/2,src.win.screen.win.get_size()[1]/2+30)) 
                            src.win.screen.win.blit(text_surface, text_rect)
                            src.win.screen.win.blit(text_surface_2, text_rect_2)
                            pygame.display.flip()
                            time.sleep(0.5)
                            trys += 1
                else:
                    src.win.screen.win.fill((0,0,0))
                    text_surface = src.win.screen.font.render(f"Searching YouTube videos...", True, (255,255,255))
                    text_rect = text_surface.get_rect(center=(src.win.screen.win.get_size()[0]/2,src.win.screen.win.get_size()[1]/2)) 
                    src.win.screen.win.blit(text_surface, text_rect)
                    pygame.display.flip()
                    load = False
                    choice = 0
                    videos = src.down.download.search(search,10)[:5]
                    src.win.screen.win.fill((0,0,0))
                    pygame.display.flip()
                    while True:
                        key = ""
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.display.quit()
                            elif event.type == pygame.KEYDOWN:
                                key = pygame.key.name(event.key)
                        if key == "up":
                            if choice != 0:
                                choice -= 1
                            else:
                                choice = len(videos) - 1
                        elif key == "down":
                            if choice != len(videos) - 1:
                                choice += 1
                            else:
                                choice = 0
                        src.win.screen.win.fill((0,0,0))
                        for i, video in enumerate(videos):
                            if i == choice:
                                text_surface = src.win.screen.font.render(video.title, True, (0,0,255))
                            else:
                                text_surface = src.win.screen.font.render(video.title, True, (255,255,255))
                            text_rect = text_surface.get_rect()
                            text_rect.centerx = src.win.screen.win.get_size()[0] // 2
                            text_rect.y = i * 30 + 50
                            src.win.screen.win.blit(text_surface, text_rect)
                            if not load:
                                pygame.display.flip()
                        load = True
                        pygame.display.flip()
                        if key == "enter" or key == "return":
                            trys = 0
                            while True:
                                try:
                                    run(f"https://www.youtube.com/watch?v={videos[choice].watch_url}")
                                    search = ""
                                    break
                                except Exception as e:
                                    if src.win.screen.vid == None:
                                        src.win.screen.reset((700,400))
                                    else:
                                        src.win.screen.reset((src.win.screen.vid.current_size[0],src.win.screen.vid.current_size[1]+5))
                                    if trys >= 10:
                                        print("fail")
                                        break
                                    print(f"An error occurred during playback. Trying again... ({trys}/10) > \n{e}")
                                    text_surface = src.win.screen.font.render(f"An error occurred during playback. Trying again... ({trys}/10) >", True, (255,255,255))
                                    text_surface_2 = src.win.screen.font.render(f"{e}", True, (255,255,255))
                                    text_rect = text_surface.get_rect(center=(src.win.screen.win.get_size()[0]/2,src.win.screen.win.get_size()[1]/2)) 
                                    text_rect_2 = text_surface_2.get_rect(center=(src.win.screen.win.get_size()[0]/2,src.win.screen.win.get_size()[1]/2+30)) 
                                    src.win.screen.win.blit(text_surface, text_rect)
                                    src.win.screen.win.blit(text_surface_2, text_rect_2)
                                    pygame.display.flip()
                                    time.sleep(0.5)
                                    trys += 1
                            break
        else:
            if not src.win.setting.loop:
                sc = src.win.setting.video_list[0]
                src.win.setting.video_list.remove(sc)
            else:
                sc = src.win.setting.video_list[0]
            trys = 0
            while True:
                try:
                    run(sc)
                    break
                except Exception as e:
                    if src.win.screen.vid == None:
                        src.win.screen.reset((700,400))
                    else:
                        src.win.screen.reset((src.win.screen.vid.current_size[0],src.win.screen.vid.current_size[1]+5))
                    if trys >= 10:
                        print("fail")
                        break
                    print(f"An error occurred during playback. Trying again... ({trys}/10) > \n{e}")
                    text_surface = src.win.screen.font.render(f"An error occurred during playback. Trying again... ({trys}/10) >", True, (255,255,255))
                    text_surface_2 = src.win.screen.font.render(f"{e}", True, (255,255,255))
                    text_rect = text_surface.get_rect(center=(src.win.screen.win.get_size()[0]/2,src.win.screen.win.get_size()[1]/2)) 
                    text_rect_2 = text_surface_2.get_rect(center=(src.win.screen.win.get_size()[0]/2,src.win.screen.win.get_size()[1]/2+30)) 
                    src.win.screen.win.blit(text_surface, text_rect)
                    src.win.screen.win.blit(text_surface_2, text_rect_2)
                    pygame.display.update()
                    time.sleep(0.5)
                    trys += 1