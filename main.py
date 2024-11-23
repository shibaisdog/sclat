import sys,time
from src import gui, nogui
import src.win.screen
import src.discord.client
args = sys.argv[1:]

nogui_op = False
once_op = False
playlist_op = False
for arg in args:
    if not arg.startswith("--") and playlist_op:
        src.win.setting.video_list.append(arg)
    elif arg.startswith("--") and arg != "--play":
        playlist_op = False
    if arg == "--nogui":
        nogui_op = True
    if arg == "--once":
        once_op = True
    if arg == "--play":
        playlist_op = True

src.discord.client.RPC.connect()
src.discord.client.update(time.time(),"waiting...")
while True:
    src.win.screen.load = 0
    if nogui_op:
        nogui.wait(once_op)
        break
    else:
        gui.wait(once_op)
        break
src.discord.client.RPC.close()