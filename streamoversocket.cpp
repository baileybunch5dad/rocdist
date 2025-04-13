#include <iostream>
#include <vector>
#include <cstring>
#include <netinet/in.h> 
#include <arpa/inet.h> // For sockets
#include <unistd.h>    // For close()


int main() {
    // Array of doubles to send
    // Declare a vector of doubles with size 1000, initialized to 0.0
    const int n = 5000;
    std::vector<double> array(n, 0.0);

  // Populate the vector with values (e.g., 1.0 to 1000.0)
    for (int i = 0; i < n; ++i) {
        array[i] = static_cast<double>(i + 1);
    }
    // std::vector<double> array = {1.1, 2.2, 3.3, 4.4};

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

    std::cout << "Connected to server." << std::endl;

    int nCalls = 1000000;
    std::cout << "Make " << nCalls << " calls passing " << n << " doubles" << std::endl;
    for(int j=0;j<nCalls;j++) {
        // Send the size of the array
        uint32_t array_size = array.size();
        // uint32_t size_network_order = htonl(array_size); // Convert to network byte order
        // send(sock, &size_network_order, sizeof(size_network_order), 0);
        send(sock, &array_size, sizeof(array_size), 0);

        send(sock, (char*) array.data(), array_size * sizeof(double), 0);
        // Send the array of doubles
        // for (double value : array) {
            // send(sock, &value, sizeof(value), 0);
            // uint64_t value_bits;
            // memcpy(&value_bits, &value, sizeof(value)); // Convert double to bits
            // uint64_t network_order = htonll(value_bits); // Convert to network byte order
            // send(sock, &network_order, sizeof(network_order), 0);
        // }
    }
    uint32_t zero = 0;
    send(sock, &zero, sizeof(zero), 0);

    // Close the socket
    close(sock);
    std::cout << "Array sent to server." << std::endl;

    return 0;
}
