
from pytubefix import YouTube
from pytubefix.cli import on_progress
import time,os
import shutil



def progress_function(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage = (bytes_downloaded / total_size) * 100
    print(f"Downloaded: {bytes_downloaded} of {total_size} bytes ({percentage:.2f}%)")

def install(url:str):
    yt = YouTube(url, on_progress_callback = on_progress)
    # print(yt.title)
    
    # video = yt.streams.get_highest_resolution()
    fns = f"./src/down/storage/{yt.length}/"

    if not os.path.exists(fns):
        os.makedirs(fns)


    fn = f"{fns}{yt.title}.mp4"
    yt = yt.streams.filter(file_extension='mp4').get_highest_resolution()

    yt.download(filename=fn)

    # video = yt.streams.filter(file_extension='mp4').first()
    # video.download(filename=fn+".mp4")
    # audio = yt.streams.filter(only_audio=True).first()
    # audio.download(filename=fn+".mp3")
    return fns, fn

def install_nogui(url:str):
    yt = YouTube(url, on_progress_callback=progress_function)
    fn = f"./src/down/storage/{yt.title}"
    audio = yt.streams.filter(only_audio=True).first()
    audio.download(filename=fn+".mp3")
    return fn

def clear(folder_path):
    # if not os.path.exists(folder_path):
    #     os.makedirs(folder_path)
    if os.path.exists(folder_path) and os.path.isdir(folder_path):

        shutil.rmtree(folder_path)

            
    else:
        print(f"The folder {folder_path} does not exist or is not a directory.")
