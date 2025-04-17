// cpp_client.cpp
#include <iostream>
#include <memory>
#include <string>

#include <grpcpp/grpcpp.h>
#include "message.grpc.pb.h"

using grpc::Channel;
using grpc::ClientContext;
using grpc::Status;
using message::MessageRequest;
using message::MessageReply;
using message::MessageService;

class MessageClient {
 public:
  MessageClient(std::shared_ptr<Channel> channel)
      : stub_(MessageService::NewStub(channel)) {}

  // Sends a message to the server
  std::string SendMessage(const std::string& message) {
    // Data to send to server
    MessageRequest request;
    request.set_message(message);

    // Container for server response
    MessageReply reply;

    // Context for the client
    ClientContext context;

    // Send RPC
    Status status = stub_->SendMessage(&context, request, &reply);

    // Return reply or error message
    if (status.ok()) {
      return reply.reply();
    } else {
      std::cout << "RPC failed: " << status.error_code() << ": " << status.error_message() << std::endl;
      return "RPC failed";
    }
  }

 private:
  std::unique_ptr<MessageService::Stub> stub_;
};

int main(int argc, char** argv) {
  // Create a channel to the server
  std::string target_address("localhost:50051");
  MessageClient client(grpc::CreateChannel(target_address, grpc::InsecureChannelCredentials()));
  
  // User input or hardcoded message
  std::string message = "Hello from C++ client!";
  if (argc > 1) {
    message = argv[1];
  }
  
  // Send message and print response
  std::string reply = client.SendMessage(message);
  std::cout << "Server responded: " << reply << std::endl;
  
  return 0;
}