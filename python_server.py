# python_server.py
import grpc
import time
from concurrent import futures
import message_pb2
import message_pb2_grpc

# Implement the service defined in our proto file
class MessageServicer(message_pb2_grpc.MessageServiceImpl):
    def SendMessage(self, request, context):
        print(f"Received message: {request.message}")
        return message_pb2.MessageReply(reply=f"Server received: '{request.message}'")

def serve():
    # Create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    # Add our service to the server
    message_pb2_grpc.add_MessageServiceServicer_to_server(
        MessageServicer(), server)
    
    # Listen on port 50051
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started, listening on port 50051")
    
    try:
        while True:
            time.sleep(86400)  # One day in seconds
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()