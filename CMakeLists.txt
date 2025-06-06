# Copyright 2018 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# cmake build file for C++ helloworld example.
# Assumes protobuf and gRPC have been installed using cmake.
# See cmake_externalproject/CMakeLists.txt for all-in-one cmake build
# that automatically builds all the dependencies before building helloworld.

cmake_minimum_required(VERSION 3.16)

project(Double_Array C CXX)

include(../cmake/common.cmake)

# Proto file
get_filename_component(double_array_proto "/double_array.proto" ABSOLUTE)
get_filename_component(double_array_proto_path "${double_array_proto}" PATH)

# Generated sources
set(double_array_proto_srcs "${CMAKE_CURRENT_BINARY_DIR}/double_array.pb.cc")
set(double_array_proto_hdrs "${CMAKE_CURRENT_BINARY_DIR}/double_array.pb.h")
set(double_array_grpc_srcs "${CMAKE_CURRENT_BINARY_DIR}/double_array.grpc.pb.cc")
set(double_array_grpc_hdrs "${CMAKE_CURRENT_BINARY_DIR}/double_array.grpc.pb.h")
add_custom_command(
      OUTPUT "${double_array_proto_srcs}" "${double_array_proto_hdrs}" "${double_array_grpc_srcs}" "${double_array_grpc_hdrs}"
      COMMAND ${_PROTOBUF_PROTOC}
      ARGS --grpc_out "${CMAKE_CURRENT_BINARY_DIR}"
        --cpp_out "${CMAKE_CURRENT_BINARY_DIR}"
        -I "${double_array_proto_path}"
        --plugin=protoc-gen-grpc="${_GRPC_CPP_PLUGIN_EXECUTABLE}"
        "${double_array_proto}"
      DEPENDS "${double_array_proto}")

# Include generated *.pb.h files
include_directories("${CMAKE_CURRENT_BINARY_DIR}")

# double_array_grpc_proto

add_library(double_array_grpc_proto
  ${double_array_grpc_srcs}
  ${double_array_grpc_hdrs}
  ${double_array_proto_srcs}
  ${double_array_proto_hdrs})
target_link_libraries(double_array_grpc_proto
  absl::check
  ${_REFLECTION}
  ${_GRPC_GRPCPP}
  ${_PROTOBUF_LIBPROTOBUF})

# Targets greeter_[async_](client|server)
foreach(_target
  greeter_client greeter_server
  greeter_callback_client greeter_callback_server
  greeter_async_client greeter_async_client2 greeter_async_server)
  add_executable(${_target} "${_target}.cc")
  target_link_libraries(${_target}
    double_array_grpc_proto
    absl::check
    absl::flags
    absl::flags_parse
    absl::log
    ${_REFLECTION}
    ${_GRPC_GRPCPP}
    ${_PROTOBUF_LIBPROTOBUF})
endforeach()
