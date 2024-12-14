import src.socket.server
import src.socket.client
import threading

client = False
server = False

def Start_Server():
    global server
    server = True
    socket_thread = threading.Thread(target=src.socket.server.start_server)
    socket_thread.daemon = True
    socket_thread.start()

def Start_Client(server_ip):
    global client
    client = True
    socket_thread = threading.Thread(target=src.socket.client.start_client, args=(server_ip,))
    socket_thread.daemon = True
    socket_thread.start()