#include <Python.h>
#include <fstream>
#include <iostream>
#include <string>
#include <cstring>
#include <sys/socket.h>
#include <arpa/inet.h>

void createPickleFile(const std::string& filePath) {
    Py_Initialize();

    PyObject* pickle = PyImport_ImportModule("pickle");
    PyObject* dataDict = PyDict_New(); // Create a sample dictionary to serialize.


    PyDict_SetItemString(dataDict, "key1", PyUnicode_FromString("value1"));
    PyDict_SetItemString(dataDict, "key2", PyLong_FromLong(42));

    PyObject* serializedData = PyObject_CallMethod(pickle, "dumps", "O", dataDict);

    if (serializedData) {
        const char* pickleData = PyBytes_AsString(serializedData);
        std::ofstream pickleFile(filePath, std::ios::binary);
        pickleFile.write(pickleData, PyBytes_Size(serializedData));
        pickleFile.close();
        Py_DECREF(serializedData);
    }

    Py_DECREF(dataDict);
    Py_DECREF(pickle);
    Py_Finalize();
}

void sendPickleFile(const std::string& filePath, const std::string& serverIP, int port) {
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock < 0) {
        std::cerr << "Socket creation failed!" << std::endl;
        return;
    }

    struct sockaddr_in serverAddr;
    serverAddr.sin_family = AF_INET;
    serverAddr.sin_port = htons(port);
    inet_pton(AF_INET, serverIP.c_str(), &serverAddr.sin_addr);

    if (connect(sock, (struct sockaddr*)&serverAddr, sizeof(serverAddr)) < 0) {
        std::cerr << "Connection failed!" << std::endl;
        close(sock);
        return;
    }

    std::ifstream pickleFile(filePath, std::ios::binary);
    if (!pickleFile.is_open()) {
        std::cerr << "Failed to open pickle file!" << std::endl;
        close(sock);
        return;
    }

    char buffer[1024];
    while (!pickleFile.eof()) {
        pickleFile.read(buffer, sizeof(buffer));
        int bytesRead = pickleFile.gcount();
        send(sock, buffer, bytesRead, 0);
    }

    pickleFile.close();
    close(sock);
}

int main() {
    createPickleFile("data.pickle");
    sendPickleFile("data.pickle", "127.0.0.1", 12345);
    return 0;
}