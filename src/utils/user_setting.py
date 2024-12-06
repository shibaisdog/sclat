import src.utils.json as json
json_file_path = "./setting.json"
def init_file():
    data = {}
    data['discord_RPC'] = True
    data['volume'] = 10
    data['file-save-dir'] = './src/storage'
    return data
def change_setting_data(key:str,value):
    data = json.read(json_file_path)
    if data == None:
        data = init_file()
    data[key] = value
    json.write(json_file_path,data)
    reload_setting_file()
def reload_setting_file():
    global discord_RPC,volume,file_save_dir
    data = json.read(json_file_path)
    if data == None:
        data = init_file()
        json.write(json_file_path,data)
    discord_RPC = data['discord_RPC']
    volume = data['volume']
    file_save_dir = data['file-save-dir']
#####################
discord_RPC = None
volume = None
file_save_dir = None
reload_setting_file()