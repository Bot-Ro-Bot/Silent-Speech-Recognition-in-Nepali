import socket

HEADER = 64
PORT = 5050
# SERVER = socket.gethostbyname(socket.gethostname())
SERVER = "192.168.0.112"
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def receive_prediction(conn):
    message = None
    msg_length = conn.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        message = conn.recv(msg_length).decode(FORMAT)
    conn.close()
    return str(message)


def start():
    
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    conn, addr = server.accept()
    print("[STARTING] server is starting...")
    print(f"[NEW CONNECTION] {addr} connected.")
    return conn

if __name__=="__main__":
    conn = start()
    print(receive_prediction(conn))