import src.utils.json as json
json_file_path = "./server.json"
max_client = 0
last_server = ''
def init_file():
    data = {}
    data['max-client'] = 5
    data['last-server'] = ""
    return data
def change_setting_data(key:str,value):
    data = json.read(json_file_path)
    if data == None:
        data = init_file()
    data[key] = value
    json.write(json_file_path,data)
    reload_setting_file()
def reload_setting_file():
    global max_client, last_server
    data = json.read(json_file_path)
    if data == None:
        data = init_file()
        json.write(json_file_path,data)
    max_client = data['max-client']
    last_server = data['last-server']
#####################
reload_setting_file()