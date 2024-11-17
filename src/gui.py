import pygame,chardet,time,re
import pygame.scrap
from pyvidplayer2 import Video
import cv2
################################
from src.down import download
import src.down
import src.down.download
import src.win.screen
import src.win.setting
import src.size
search = ""
pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
def is_url(url: str) -> bool:
    match = re.search(pattern, url)
    return bool(match)

def frame_to_ascii(frame, width=100):
    ASCII_CHARS = ["$", "@", "B", "%", "8", "&", "W", "M", "#", "*", "o", "a", "h", "k", "b", "d", 
               "p", "q", "w", "m", "Z", "O", "0", "Q", "L", "C", "J", "U", "Y", "X", "z", "c",
               "v", "u", "n", "x", "r", "j", "f", "t", "/", "\\", "|", "(", ")", "1", "{", "}",
               "[", "]", "?", "-", "_", "+", "~", "<", ">", "i", "!", "l", "I", ";", ":", ",",
               "\"", "^", "`", "'", ".", " "]
    height, new_width = frame.shape[:2]
    aspect_ratio = height / new_width
    new_height = int(width * aspect_ratio * 0.55)
    resized_image = cv2.resize(frame, (width, new_height))
    ascii_chars = []
    colors = []
    scale = 256 / len(ASCII_CHARS)
    pixels = resized_image.reshape(-1, 3)
    for pixel in pixels:
        brightness = int(pixel.mean())
        index = int(brightness / scale)
        ascii_chars.append(ASCII_CHARS[index])
        colors.append(tuple(pixel.astype(int)))
    ascii_image = []
    for i in range(0, len(ascii_chars), width):
        line_chars = ascii_chars[i:i+width]
        line_colors = colors[i:i+width]
        ascii_image.append((line_chars, line_colors))
    return ascii_image

cap = None
ascii_mode = False
font_size = 14
font = None

def run(url:str):
    fns, fn = download.install(url)
    src.win.screen.vid = Video(fn)
    src.win.screen.reset((src.win.screen.vid.current_size[0],src.win.screen.vid.current_size[1]+5))
    pygame.display.set_caption(src.win.screen.vid.name)
    src.win.screen.vid.set_volume(src.win.setting.volume/100)
    msg_info = 0
    msg_value = ""
    global ascii_mode, cap, font_size, font
    font = pygame.font.SysFont("Courier", font_size)
    cap = cv2.VideoCapture(fn)
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
            elif key == "a":
                ascii_mode = not ascii_mode
                if ascii_mode:
                    #cap = cv2.VideoCapture(fn)
                    video_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                    video_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                    ascii_width = 80
                    ascii_height = int(ascii_width * video_height / video_width)
                    window_width = ascii_width * font_size * 0.6
                    window_height = ascii_height * font_size * 0.58
                    src.win.screen.win = pygame.display.set_mode((int(window_width), int(window_height)))
                    font = pygame.font.SysFont("Courier", font_size)
                else:
                    if cap:
                        cap.release()
                        cap = None
                    src.win.screen.reset((src.win.screen.vid.current_size[0], src.win.screen.vid.current_size[1]+5))
            current_time = src.win.screen.vid.get_pos()
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_number = int(current_time * fps)
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
            ret, frame = cap.read()
            frame = src.size.sizeup(frame,pygame.display.get_window_size())
            if ascii_mode and cap:
                if ret:
                    ascii_frame = frame_to_ascii(frame, width=ascii_width)
                    src.win.screen.win.fill((0, 0, 0))
                    for i, (line_chars, line_colors) in enumerate(ascii_frame):
                        x = 0
                        for char, color in zip(line_chars, line_colors):
                            color = (color[2], color[1], color[0])
                            text_surface = font.render(char, False, color)
                            src.win.screen.win.blit(text_surface, (x, i * font_size))
                            x += font_size * 0.6
                    if time.time() - msg_info <= 2:
                        if msg_value == "volume":
                            text_surface = src.win.screen.font.render(f"Set Volume > {src.win.setting.volume}%", True, (255,255,255))
                        elif msg_value == "loop":
                            text_surface = src.win.screen.font.render(f"Set Loop > {src.win.setting.loop}", True, (255,255,255))
                        else:
                            text_surface = src.win.screen.font.render("", True, (255,255,255))
                        text_rect = text_surface.get_rect(center=(80,10)) 
                        src.win.screen.win.blit(text_surface, text_rect)
                    total_length = src.win.screen.vid.duration
                    rect_coords = (0, src.win.screen.win.get_size()[1] - 5, src.win.screen.win.get_size()[0], 5)
                    pygame.draw.rect(src.win.screen.win, (100, 100, 100), rect_coords)
                    linebar = (current_time / total_length) * src.win.screen.win.get_size()[0]
                    rect_coords = (0, src.win.screen.win.get_size()[1] - 5, linebar, 5)
                    pygame.draw.rect(src.win.screen.win, (255, 0, 0), rect_coords)
                    caps = f"[{current_time:.2f}s / {total_length:.2f}s] {src.win.screen.vid.name}"
                    pygame.display.set_caption(caps)
                    pygame.display.update()
                    src.win.screen.vid.draw(src.win.screen.win, (0, 0))
            else:
                frame_surface = pygame.surfarray.make_surface(frame)
                src.win.screen.win.blit(frame_surface, (0, 0))
                if time.time() - msg_info <= 2:
                    if msg_value == "volume":
                        text_surface = src.win.screen.font.render(f"Set Volume > {src.win.setting.volume}%", True, (255, 255, 255))
                    elif msg_value == "loop":
                        text_surface = src.win.screen.font.render(f"Set Loop > {src.win.setting.loop}", True, (255, 255, 255))
                    else:
                        text_surface = src.win.screen.font.render("", True, (255, 255, 255))
                    text_rect = text_surface.get_rect(center=(80, 10))
                    src.win.screen.win.blit(text_surface, text_rect)
                total_length = src.win.screen.vid.duration
                rect_coords = (0, src.win.screen.win.get_size()[1] - 5, src.win.screen.win.get_size()[0], 5)
                pygame.draw.rect(src.win.screen.win, (100, 100, 100), rect_coords)
                linebar = (current_time / total_length) * src.win.screen.win.get_size()[0]
                rect_coords = (0, src.win.screen.win.get_size()[1] - 5, linebar, 5)
                pygame.draw.rect(src.win.screen.win, (255, 0, 0), rect_coords)
                caps = f"[{current_time:.2f}s / {total_length:.2f}s] {src.win.screen.vid.name}"
                pygame.display.set_caption(caps)
                pygame.display.update()
                src.win.screen.vid.draw(src.win.screen.win, (0, 0))
        pygame.time.wait(16)
    if cap:
        cap.release()
        cap = None
    src.win.screen.vid.close()
    pygame.display.set_caption("Sclat Video Player")
    download.clear(fns)
    pygame.display.update()

def wait():
    global search
    if src.win.screen.vid == None:
        src.win.screen.reset((700,400))
    else:
        src.win.screen.reset((src.win.screen.vid.current_size[0],src.win.screen.vid.current_size[1]+5))
    pygame.scrap.init()
    pygame.display.set_caption("Sclat Video Player")
    pygame.key.set_text_input_rect(pygame.Rect(0, 0, 0, 0))
    while True:
        src.win.screen.win.fill((0, 0, 0))
        key = None
        if len(src.win.setting.video_list) == 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    pygame.quit()
                    return  # 함수 종료
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        search = search[:-1]
                    elif event.key == pygame.K_RETURN:
                        key = "return"
                    elif event.key == pygame.K_v and (pygame.key.get_mods() & pygame.KMOD_CTRL):
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
                elif event.type == pygame.TEXTINPUT:
                    search += event.text
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
                                pygame.quit()
                                return  # 함수 종료
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