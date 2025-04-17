import socket
import pickle

def listener():
    host = 'localhost'
    port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)

    print("Listening for a connection...")
    conn, addr = server_socket.accept()
    print(f"Connected by {addr}")

    data = b""
    while True:
        chunk = conn.recv(1024)
        if not chunk:
            break
        data += chunk

    print("Received data:")
    deserialized_data = pickle.loads(data)
    print(deserialized_data)

    conn.close()

if __name__ == "__main__":
    listener()