from concurrent import futures
import grpc
import dataframe_pb2
import dataframe_pb2_grpc

class DataFrameServiceServicer(dataframe_pb2_grpc.DataFrameServiceServicer):
    def SendDataFrame(self, request, context):
        for column_name, column_data in request.columns.items():
            print(f"Column: {column_name}")
            print("Doubles:", column_data.double_array)
            print("Strings:", column_data.string_array)
        return request

server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
dataframe_pb2_grpc.add_DataFrameServiceServicer_to_server(DataFrameServiceServicer(), server)
server.add_insecure_port('[::]:50051')
server.start()
server.wait_for_termination()