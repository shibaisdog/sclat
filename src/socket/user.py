import socket, requests
def get_external_ip():
    try:
        response = requests.get("https://api.ipify.org?format=json")
        if response.status_code == 200:
            return response.json()['ip']
        else:
            return '?:?:?:?'
    except requests.RequestException as e:
        return '?:?:?:?'
    
def get_internal_ip():
    try:
        hostname = socket.gethostname()
        internal_ip = socket.gethostbyname(hostname)
        return internal_ip
    except socket.error as e:
        return '?:?:?:?'