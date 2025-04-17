#include <iostream>
#include <memory>
#include <string>
#include <vector>

#include <grpcpp/grpcpp.h>
#include "double_array.grpc.pb.h"

using grpc::Channel;
using grpc::ClientContext;
using grpc::Status;
using doublearrayservice::DoubleArrayRequest;
using doublearrayservice::CountResponse;
using doublearrayservice::DoubleArrayService;

class DoubleArrayClient {
public:
    DoubleArrayClient(std::shared_ptr<Channel> channel)
        : stub_(DoubleArrayService::NewStub(channel)) {}

    // Sends an array of doubles to the server and returns the count response
    int SendDoubleArray(const std::vector<double>& values) {
        // Create request message
        DoubleArrayRequest request;
        for (const double& value : values) {
            request.add_values(value);
        }

        // Response object
        CountResponse response;

        // Context for the client
        ClientContext context;

        // Make the call to the server
        Status status = stub_->SendDoubleArray(&context, request, &response);

        if (status.ok()) {
            return response.count();
        } else {
            std::cout << "RPC failed: " << status.error_code() << ": " 
                      << status.error_message() << std::endl;
            return -1;
        }
    }

private:
    std::unique_ptr<DoubleArrayService::Stub> stub_;
};

int main() {
    // Create a client
    DoubleArrayClient client(
        grpc::CreateChannel("localhost:50051", grpc::InsecureChannelCredentials()));

    // Create an array of doubles to send
    std::vector<double> doubles = {1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7};
    
    std::cout << "Sending " << doubles.size() << " doubles to server:" << std::endl;
    for (const auto& value : doubles) {
        std::cout << value << " ";
    }
    std::cout << std::endl;

    // Call the RPC
    int count = client.SendDoubleArray(doubles);
    
    if (count >= 0) {
        std::cout << "Server response: array has " << count << " elements" << std::endl;
    }

    return 0;
}