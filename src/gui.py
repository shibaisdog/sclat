import pygame,time
import pygame.scrap
from pyvidplayer2 import Video
################################
from src.down import download
import src.win.screen
import src.win.setting
search = ""
def run(url:str):
    fns, fn = download.install(url)
    src.win.screen.vid = Video(fn)
    src.win.screen.font = pygame.font.Font(None, 25)
    src.win.screen.reset(src.win.screen.vid.current_size)
    pygame.display.set_caption(src.win.screen.vid.name)
    src.win.screen.vid.set_volume(src.win.setting.volume/100)
    msg_vl_info = 0
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
            elif key == "right":
                src.win.screen.vid.seek(15)
            elif key == "left":
                src.win.screen.vid.seek(-15)
            elif key == "up":
                msg_vl_info = time.time()
                if src.win.setting.volume < 100:
                    src.win.setting.volume += 10
                    src.win.screen.vid.set_volume(src.win.setting.volume/100)
            elif key == "down":
                msg_vl_info = time.time()
                if src.win.setting.volume > 0:
                    src.win.setting.volume -= 10
                    src.win.screen.vid.set_volume(src.win.setting.volume/100)
            if src.win.screen.vid.draw(src.win.screen.win, (0, 0), force_draw=True):
                if time.time() - msg_vl_info <= 2:
                    text_surface = src.win.screen.font.render(f"Set Volume > {src.win.setting.volume}%", True, (255,255,255))
                    text_rect = text_surface.get_rect(center=(80,10)) 
                    src.win.screen.win.blit(text_surface, text_rect)
                pygame.display.update()
        pygame.time.wait(16)
    src.win.screen.vid.close()
    download.clear(fns)
    pygame.display.update()

def wait():
    global search
    if src.win.screen.vid == None:
        src.win.screen.reset((700,400))
    else:
        src.win.screen.reset(src.win.screen.vid.current_size)
    pygame.scrap.init()
    while True:
        src.win.screen.win.fill((0, 0, 0))
        key = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
            elif event.type == pygame.KEYDOWN:
                key = pygame.key.name(event.key)
                if event.key == pygame.K_v and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                    if pygame.scrap.get_init():
                        copied_text = pygame.scrap.get(pygame.SCRAP_TEXT)
                        if copied_text:
                            copied_text = copied_text.decode('utf-8').strip('\x00')
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
                        src.win.screen.reset(src.win.screen.vid.current_size)
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