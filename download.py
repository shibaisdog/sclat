from pytubefix import YouTube
import time,os
def progress_function(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage = (bytes_downloaded / total_size) * 100
    print(f"Downloaded: {bytes_downloaded} of {total_size} bytes ({percentage:.2f}%)")

def install(url:str):
    yt = YouTube(url, on_progress_callback=progress_function)
    fn = f"storage/{time.time()}"
    video = yt.streams.filter(file_extension='mp4').first()
    video.download(filename=fn+".mp4")
    audio = yt.streams.filter(only_audio=True).first()
    audio.download(filename=fn+".mp3")
    return fn

def install_nogui(url:str):
    yt = YouTube(url, on_progress_callback=progress_function)
    fn = f"storage/{time.time()}"
    audio = yt.streams.filter(only_audio=True).first()
    audio.download(filename=fn+".mp3")
    return fn

def clear(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(f"Error removing file {file_path}: {e}")
    else:
        print(f"The folder {folder_path} does not exist or is not a directory.")