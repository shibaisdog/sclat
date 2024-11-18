import src.utils.json as json
json_file_path = "./setting.json"
def init_file():
    data = {}
    data['volume'] = 10
    return data
def change_setting_data(key:str,value):
    data = json.read(json_file_path)
    if data == None:
        data = init_file()
    data[key] = value
    json.write(json_file_path,data)
    reload_setting_file()
def reload_setting_file():
    global volume
    data = json.read(json_file_path)
    if data == None:
        data = init_file()
        json.write(json_file_path,data)
    volume = data['volume']
volume = None
loop = False
video_list = []
SEARCH_PATTERN = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
PLAYLIST_SEARCH_PATTERN = r"(?:list=)([A-Za-z0-9_-]{34})"
MESSAGE_DISPLAY_TIME = 2.0
ASCII_CHARS = ["$", "@", "B", "%", "8", "&", "W", "M", "#", "*", "o", "a", "h", "k", "b", "d", 
               "p", "q", "w", "m", "Z", "O", "0", "Q", "L", "C", "J", "U", "Y", "X", "z", "c",
               "v", "u", "n", "x", "r", "j", "f", "t", "/", "\\", "|", "(", ")", "1", "{", "}",
               "[", "]", "?", "-", "_", "+", "~", "<", ">", "i", "!", "l", "I", ";", ":", ",",
               "\"", "^", "`", "'", ".", " "]
reload_setting_file()