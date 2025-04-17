import grpc
import time
from concurrent import futures
import double_array_pb2
import double_array_pb2_grpc

class DoubleArrayServiceServicer(double_array_pb2_grpc.DoubleArrayServiceServicer):
    def SendDoubleArray(self, request, context):
        # Process the received array of doubles
        values = request.values
        count = len(values)
        
        print(f"Server received array with {count} elements:")
        print(values)
        
        # Return the count response
        return double_array_pb2.CountResponse(count=count)

def serve():
    # Create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    # Add the servicer to the server
    double_array_pb2_grpc.add_DoubleArrayServiceServicer_to_server(
        DoubleArrayServiceServicer(), server)
    
    # Listen on port 50051
    server.add_insecure_port('[::]:50051')
    server.start()
    
    print("Server started on port 50051")
    
    try:
        # Keep the server running
        while True:
            time.sleep(86400)  # One day in seconds
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()