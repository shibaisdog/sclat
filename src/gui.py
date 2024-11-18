import chardet, cv2, time, re, os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame, pygame.scrap
from pyvidplayer2 import Video
from dataclasses import dataclass
from typing import Optional
##############################################
from src.down import download
import src.win.screen
import src.win.setting
import src.size


# Global state
@dataclass
class VideoState:
    cap: Optional[cv2.VideoCapture] = None
    ascii_mode: bool = False
    font_size: int = 14
    font: Optional[pygame.font.Font] = None
    search: str = ""
    search_width: int = 0
    search_height: int = 0
    ascii_width: int = 80 
    msg_start_time: float = 0
    msg_text: str = ""

state = VideoState()

def is_url(url: str) -> bool:
    match = re.search(src.win.setting.SEARCH_PATTERN, url)
    return bool(match)
def is_playlist(url: str) -> bool:
    match = re.search(src.win.setting.PLAYLIST_SEARCH_PATTERN, url)
    return bool(match)

def frame_to_ascii(frame, width=100):
    """
    Converts a given image frame to an ASCII representation.

    Args:
        frame (numpy.ndarray): The input image frame to be converted.
        width (int, optional): The width of the ASCII representation. Defaults to 100.

    Returns:
        list of tuples: A list where each tuple contains two lists:
            - A list of ASCII characters representing a line of the image.
            - A list of RGB color tuples corresponding to each ASCII character.
    """
    height, new_width = frame.shape[:2]
    aspect_ratio = height / new_width
    new_height = int(width * aspect_ratio * 0.55)
    resized_image = cv2.resize(frame, (width, new_height))
    ascii_chars = []
    colors = []
    scale = 256 / len(src.win.setting.ASCII_CHARS)
    pixels = resized_image.reshape(-1, 3)
    for pixel in pixels:
        brightness = int(pixel.mean())
        index = int(brightness / scale)
        ascii_chars.append(src.win.setting.ASCII_CHARS[index])
        colors.append(tuple(pixel.astype(int)))
    ascii_image = []
    for i in range(0, len(ascii_chars), width):
        line_chars = ascii_chars[i:i+width]
        line_colors = colors[i:i+width]
        ascii_image.append((line_chars, line_colors))
    return ascii_image

def handle_key_event(key: str) -> None:
    """
    Handles key events for controlling video playback and settings.
    Parameters:
    key (str): The key pressed by the user. Supported keys are:
        - "r": Restart the video.
        - "p": Toggle pause/play state of the video.
        - "m": Toggle mute/unmute state of the video.
        - "l": Toggle loop setting.
        - "up": Increase volume by 10%.
        - "down": Decrease volume by 10%.
        - "right": Seek forward by 15 seconds.
        - "left": Seek backward by 15 seconds.
        - "a": Toggle ASCII mode.
    Returns:
    None
    """
    if not key:
        return

    if key == "r":
        src.win.screen.vid.restart()
        state.msg_text = "Restarted"
    elif key == "p":
        src.win.screen.vid.toggle_pause()
        state.msg_text = "Paused" if src.win.screen.vid.paused else "Playing"
    elif key == "m":
        src.win.screen.vid.toggle_mute()
        state.msg_text = "Muted" if src.win.screen.vid.muted else "Unmuted"
    elif key == "l":
        src.win.setting.loop = not src.win.setting.loop
        state.msg_text = f"Loop: {'On' if src.win.setting.loop else 'Off'}"
    elif key in ["up", "down"]:
        volume_delta = 10 if key == "up" else -10
        if 0 <= src.win.setting.volume + volume_delta <= 100:
            src.win.setting.change_setting_data('volume',src.win.setting.volume + volume_delta)
            src.win.screen.vid.set_volume(src.win.setting.volume/100)
            state.msg_text = f"Volume: {src.win.setting.volume}%"
    elif key in ["right", "left"]:
        seek_amount = 15 if key == "right" else -15
        src.win.screen.vid.seek(seek_amount)
        state.msg_text = f"Seek: {seek_amount:+d}s"
    elif key == "a":
        toggle_ascii_mode()
        state.msg_text = "ASCII Mode" if state.ascii_mode else "Normal Mode"
    else:
        state.msg_text = ""
        
    if state.msg_text:
        state.msg_start_time = time.time()

def toggle_ascii_mode():
    """Toggle between ASCII and normal video mode"""
    state.ascii_mode = not state.ascii_mode
    if state.ascii_mode:
        video_width = int(state.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        video_height = int(state.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        ascii_height = int(state.ascii_width * video_height / video_width)
        window_width = state.ascii_width * state.font_size * 0.6
        window_height = int(ascii_height * state.font_size * 0.56)
        src.win.screen.win = pygame.display.set_mode((int(window_width), int(window_height)))
        state.font = pygame.font.SysFont("Courier", state.font_size)
    else:
        src.win.screen.reset((src.win.screen.vid.current_size[0], src.win.screen.vid.current_size[1]+5), vid=True)
    os.environ['SDL_VIDEO_CENTERED'] = '1'

def draw_overlay(current_time: float):
    """Draws the overlay text on the video screen"""
    if time.time() - state.msg_start_time <= src.win.setting.MESSAGE_DISPLAY_TIME and state.msg_text:
        text_surface = src.win.screen.font.render(state.msg_text, True, (255,255,255))
        text_rect = text_surface.get_rect(topleft=(10, 10))
        src.win.screen.win.blit(text_surface, text_rect)

    total_length = src.win.screen.vid.duration
    window_width = src.win.screen.win.get_size()[0]
    window_height = src.win.screen.win.get_size()[1]
    
    pygame.draw.rect(src.win.screen.win, (100, 100, 100), 
                    (0, window_height - 5, window_width, 5))
    pygame.draw.rect(src.win.screen.win, (255, 0, 0), 
                    (0, window_height - 5, (current_time / total_length) * window_width, 5))

def try_play_video(url: str, max_retries: int = 10) -> None:
    """
    Attempts to play a video from the given URL, retrying up to a specified number of times if an exception occurs.
    Args:
        url (str): The URL of the video to play.
        max_retries (int, optional): The maximum number of retry attempts. Defaults to 10.
    Returns:
        None
    Raises:
        Exception: If the video fails to play after the maximum number of retries, an exception is raised and a message is printed.
    """
    for retry in range(max_retries):
        try:
            run(url)
            return
        except Exception as e:
            if retry == max_retries - 1:
                print("Failed to play video after maximum retries")
                return
            print(f"Retry {retry + 1}/{max_retries}: {str(e)}")
            time.sleep(0.5)

def run(url: str):
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    fns, fn = download.install(url)
    src.win.screen.vid = Video(fn)
    src.win.screen.reset((src.win.screen.vid.current_size[0], src.win.screen.vid.current_size[1] + 5), vid=True)
    pygame.display.set_caption(src.win.screen.vid.name)
    src.win.screen.vid.set_volume(src.win.setting.volume / 100)
    global state
    state.font = pygame.font.SysFont("Courier", state.font_size)
    state.cap = cv2.VideoCapture(fn)
    state.msg_start_time = 0 
    state.msg_text = "" 

    while src.win.screen.vid.active:
        key = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                src.win.screen.vid.stop()
            elif event.type == pygame.KEYDOWN:
                key = pygame.key.name(event.key)
                handle_key_event(key)
        
        if src.win.screen.load == 2:
            current_time = src.win.screen.vid.get_pos()
            total_length = src.win.screen.vid.duration
            fps = state.cap.get(cv2.CAP_PROP_FPS)
            frame_number = int(current_time * fps)
            state.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
            ret, frame = state.cap.read()
            if total_length - current_time <= 0.1:
                if src.win.setting.loop:
                    src.win.screen.vid.restart()
            if not ret:
                break
            if state.ascii_mode and state.cap:
                if ret:
                    ascii_frame = frame_to_ascii(frame, width=state.ascii_width)
                    src.win.screen.win.fill((0, 0, 0))
                    for i, (line_chars, line_colors) in enumerate(ascii_frame):
                        x = 0
                        for char, color in zip(line_chars, line_colors):
                            color = (color[2], color[1], color[0])
                            text_surface = state.font.render(char, False, color)
                            src.win.screen.win.blit(text_surface, (x, i * state.font_size))
                            x += state.font_size * 0.6
                    draw_overlay(current_time)
                    pygame.display.set_caption(f"[{current_time:.2f}s / {total_length:.2f}s] {src.win.screen.vid.name}")
                    pygame.display.update()
                    src.win.screen.vid.draw(src.win.screen.win, (0, 0))
            else:
                frame = src.size.sizeup(frame, pygame.display.get_window_size())
                frame_surface = pygame.surfarray.make_surface(frame)
                src.win.screen.win.blit(frame_surface, (0, 0))
                draw_overlay(current_time)
                pygame.display.set_caption(f"[{current_time:.2f}s / {total_length:.2f}s] {src.win.screen.vid.name}")
                pygame.display.update()
                src.win.screen.vid.draw(src.win.screen.win, (0, 0))
        pygame.time.wait(16)
    if state.cap:
        state.cap.release()
        state.cap = None
    src.win.screen.vid.close()
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    src.win.screen.reset((state.search_width, state.search_height))
    pygame.display.set_caption("Sclat Video Player")
    download.clear(fns)
    pygame.display.update()

def wait():
    global state
    screen_info = pygame.display.Info()
    state.search_width = screen_info.current_w // 2
    state.search_height = int(state.search_width * (9 / 16))
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    if src.win.screen.vid is None:
        src.win.screen.reset((state.search_width, state.search_height))
    else:
        src.win.screen.reset((src.win.screen.vid.current_size[0], src.win.screen.vid.current_size[1] + 5), vid=True)
    pygame.scrap.init()
    icon = pygame.image.load("./asset/sclatIcon.png")
    pygame.display.set_icon(icon)
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
                    return  
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        state.search = state.search[:-1]
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
                                state.search += copied_text
                elif event.type == pygame.TEXTINPUT:
                    state.search += event.text
            if not key:
                text_surface = src.win.screen.font.render(f"search video : {state.search}", True, (255,255,255))
                text_rect = text_surface.get_rect(center=(src.win.screen.win.get_size()[0]/2,src.win.screen.win.get_size()[1]/2)) 
                src.win.screen.win.blit(text_surface, text_rect)
                pygame.display.update()
                continue
            elif key == "backspace":
                state.search = state.search[0:len(state.search)-1]
            elif len(key) == 1:
                state.search = state.search + key
            text_surface = src.win.screen.font.render(f"search video : {state.search}", True, (255,255,255))
            text_rect = text_surface.get_rect(center=(src.win.screen.win.get_size()[0]/2,src.win.screen.win.get_size()[1]/2)) 
            src.win.screen.win.blit(text_surface, text_rect)
            pygame.display.update()
            if key == "enter" or key == "return":
                #  TEST URL 'https://youtube.com/playlist?list=PLWe0uF1Zfq3K4ao8lvh2fM3NDqBAxhdaZ&si=JO4TZBYAokbwWzHe'
                if is_playlist(state.search):
                    video_urls = download.get_playlist_video(state.search)
                    src.win.setting.video_list.extend(video_urls)
                    trys = 0
                    while len(src.win.setting.video_list) != 0:
                        try:
                            run(src.win.setting.video_list[0])
                            src.win.setting.video_list.remove(src.win.setting.video_list[0])
                        except Exception as e:
                            if src.win.screen.vid == None:
                                src.win.screen.reset((state.search_width, state.search_height))
                            else:
                                src.win.screen.reset((src.win.screen.vid.current_size[0],src.win.screen.vid.current_size[1]+5), vid=True)
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
                if is_url(state.search):
                    a = state.search
                    state.search = ""
                    trys = 0
                    while True:
                        try:
                            run(a)
                            break
                        except Exception as e:
                            if src.win.screen.vid == None:
                                src.win.screen.reset((state.search_width, state.search_height))
                            else:
                                src.win.screen.reset((src.win.screen.vid.current_size[0],src.win.screen.vid.current_size[1]+5), vid=True)
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
                    videos = src.down.download.search(state.search,10)[:5]
                    src.win.screen.win.fill((0,0,0))
                    pygame.display.flip()
                    while True:
                        key = ""
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.display.quit()
                                pygame.quit()
                                return  
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
                                    state.search = ""
                                    break
                                except Exception as e:
                                    if src.win.screen.vid == None:
                                        src.win.screen.reset((state.search_width, state.search_height))
                                    else:
                                        src.win.screen.reset((src.win.screen.vid.current_size[0],src.win.screen.vid.current_size[1]+5), vid=True)
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
                        src.win.screen.reset((state.search_width, state.search_height))
                    else:
                        src.win.screen.reset((src.win.screen.vid.current_size[0],src.win.screen.vid.current_size[1]+5), vid=True)
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