import os,pygame,shutil
from pytubefix import YouTube,Search
from pytubefix.cli import on_progress
####################################
import src.win.screen

def convert_size(bytes):
    for unit in ['Byte', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB']:
        if bytes < 1024.0:
            return f"{bytes:.2f} {unit}"
        bytes /= 1024.0

def progress_function(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage = (bytes_downloaded / total_size) * 100
    on_progress(stream, chunk, bytes_remaining)
    src.win.screen.load = 1
    
    width = stream.width if stream.width else 800
    height = stream.height if stream.height else 600
    
    src.win.screen.reset((width, height+5))
    pygame.display.set_caption(f"Downloading: {convert_size(bytes_downloaded)} of {convert_size(total_size)} ({percentage:.2f}%)")
    text_surface = src.win.screen.font.render(f"Downloading: {convert_size(bytes_downloaded)} of {convert_size(total_size)} ({percentage:.2f}%)", True, (255,255,255))
    text_rect = text_surface.get_rect(center=(int(width/2), int(height/2)))
    src.win.screen.win.blit(text_surface, text_rect)
    pygame.display.update()

def after(a,b):
    src.win.screen.load = 2

def search(q:str,result:int):
    list = Search(query=q)
    return list.videos

def search_infos(videos):
    res = []
    for video in videos:
        res.append(video_info(f"https://www.youtube.com/watch?v={video.watch_url}"))
    return res

def video_info(url:str):
    return YouTube(url).streaming_data

def install(url:str):
    os.makedirs("./src/down/storage/", exist_ok=True)
    yt = YouTube(url, on_progress_callback = progress_function, on_complete_callback=after)
    fns = f"./src/down/storage/{yt.length}/"
    os.makedirs(fns, exist_ok=True)
    if not os.path.exists(fns):
        os.makedirs(fns)
    fn = f"{fns}{yt.title}.mp4"
    yt = yt.streams.filter(file_extension='mp4').get_highest_resolution()
    yt.download(filename=fn)
    return fns, fn

def install_nogui(url:str):
    os.makedirs("./src/down/storage/", exist_ok=True)
    yt = YouTube(url, on_progress_callback=progress_function)
    fn = f"./src/down/storage/{yt.title}"
    audio = yt.streams.filter(only_audio=True).first()
    audio.download(filename=fn+".mp3")
    return fn

def clear(folder_path):
    if os.path.exists(folder_path):
        if os.path.isdir(folder_path):
            shutil.rmtree(folder_path)
    os.makedirs(folder_path, exist_ok=True)