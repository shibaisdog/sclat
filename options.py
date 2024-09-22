import sys,time
import gui,nogui
args = sys.argv[1:]

nogui_op = False
once_op = False
playlist_op = False
playlist_url = []
for arg in args:
    if not arg.startswith("--") and playlist_op:
        playlist_url.append(arg)
    elif arg.startswith("--") and arg != "--play":
        playlist_op = False
    if arg == "--nogui":
        nogui_op = True
    if arg == "--once":
        once_op = True
    if arg == "--play":
        playlist_op = True

while True:
    if len(playlist_url) == 0:
        url = input("Please enter the URL to play the video (youtube url) : ")
    else:
        url = playlist_url[0]
        playlist_url.remove(url)
    if nogui_op:
        trys = 0
        while True:
            try:
                nogui.run(url)
                break
            except Exception as e:
                if trys >= 10:
                    print("fail")
                    break
                print(f"An error occurred during playback. Trying again... ({trys}/10) > \n{e}")
                time.sleep(0.5)
                trys += 1
    else:
        trys = 0
        while True:
            try:
                gui.run(url)
                break
            except Exception as e:
                if trys >= 10:
                    print("fail")
                    break
                print(f"An error occurred during playback. Trying again... ({trys}/10) > \n{e}")
                time.sleep(0.5)
                trys += 1
    if once_op:
        break