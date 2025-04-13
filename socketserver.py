import cProfile
import socket
import struct
from DynamicDist import DynamicDist


def receive_full_buffer(sock, buffer_size):
    """Receives data from the socket until the buffer is full.

    Args:
        sock: The socket object.
        buffer_size: The size of the buffer to fill.

    Returns:
        A bytes object containing the received data, or None if an error occurred.
    """
    buffer = bytearray()
    while len(buffer) < buffer_size:
        try:
            data = sock.recv(buffer_size - len(buffer))
            if not data:
                # Connection closed prematurely
                if buffer:
                    return bytes(buffer)
                else:
                    return None
            buffer.extend(data)
        except socket.error as e:
            print(f"Socket error: {e}")
            return None
    return bytes(buffer)

def Main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))  # Host and port
    server_socket.listen(1)
    print("Server listening on port 12345...")

    conn, addr = server_socket.accept()
    print(f"Connection from {addr}")

    dd = DynamicDist()
    dd.add(1.)
    while True:
        # Read the size of the array
        data = conn.recv(4)
        array_size = struct.unpack('I', data)[0]  # Unpack as unsigned int
        # print(f"Array size: {array_size}")
        if array_size == 0:
            break

        # Read the array of doubles
        # data = conn.recv(array_size * 8)  # Each double is 8 bytes
        data = receive_full_buffer(conn, array_size * 8)
        array = struct.unpack(f'{array_size}d', data)  # Unpack as double array
        # print(f"Received array: {array}")
        # dd.add_many(array)

    conn.close()
    server_socket.close()
    h,b = dd.histogram(n_bins=10)
    print(h)
    print(b)

if __name__ == "__main__":
    # start_server()
    cProfile.run('Main()')
