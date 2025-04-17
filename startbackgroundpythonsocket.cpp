#include <Python.h>
#include <thread>
#include <iostream>
#include <vector>
#include <cstring>
#include <netinet/in.h> 
#include <arpa/inet.h> // For sockets
#include <unistd.h>    // For close()

void startPythonListener() {
    // Initialize the Python interpreter
    Py_Initialize();

    FILE *fp;
    fp = fopen("pythoncontroller", "r");
    if (fp == NULL) {
        fprintf(stderr, "Cannot open file\n");
        return 1;
    }

    PyRun_SimpleFile(fp, "script.py");
    fclose(fp);
    auto pyCode = R"ROCCO(
import socket

HOST = "localhost"
PORT = 12345

def read_until_empty(sock, buffer_size=1024):
    data_buffer = b""
    while True:
        data = sock.recv(buffer_size)
        if not data:
            break 
        data_buffer += data
    return data_buffer

if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((HOST, PORT))
        sock.listen()
        conn, addr = sock.accept()
        with conn:
            print(f"Connected by {addr}")
            data = read_until_empty(conn, buffer_size=1024)
            print(f"Received: {data.decode()}")
    )ROCCO";

    std::cout << pyCode << std::endl;
    int rc = PyRun_SimpleString(pyCode);
    std::cout << "Return code " << rc << std::endl;

    Py_Finalize();
}

int getPythonSocket(int port) {
       // Create a socket
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock < 0) {
        std::cerr << "Failed to create socket." << std::endl;
        return 1;
    }

    // Server address
    sockaddr_in server_addr;
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(12345); // Port
    inet_pton(AF_INET, "127.0.0.1", &server_addr.sin_addr); // Localhost

    // Connect to the server
    if (connect(sock, (struct sockaddr*)&server_addr, sizeof(server_addr)) < 0) {
        std::cerr << "Failed to connect to server." << std::endl;
        close(sock);
        return 1;
    }

    return sock;
}

int main() {
    std::cout << "Starting embedded Python listener in background..." << std::endl;

     


    sleep(1);

    std::cout << "C++ application running concurrently..." << std::endl;

    int sock = getPythonSocket(12345);

    std::string message = "Hello from C++!";
    send(sock, message.c_str(), message.size(), 0);

    std::cout << "Sent: " << message << std::endl;

    close(sock);

    sleep(1);

    return 0;
}
