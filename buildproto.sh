python3 -m pip install grpcio grpcio-tools
cd ~
git clone https://github.com/grpc/grpc

# install grpc for c++

#
# first get a current version of cmake

export MY_INSTALL_DIR=$HOME/.local
mkdir -p $MY_INSTALL_DIR
export PATH="$MY_INSTALL_DIR/bin:$PATH"

sudo apt install -y cmake
cmake --version

#
# newer version
#

wget -q -O cmake-linux.sh https://github.com/Kitware/CMake/releases/download/v3.30.3/cmake-3.30.3-linux-x86_64.sh
sh cmake-linux.sh -- --skip-license --prefix=$MY_INSTALL_DIR
rm cmake-linux.sh

# other dev tools

 sudo yum install -y  autoconf libtool pkg-config
 sudo yum groupinstall -y "Development Tools"

 # clone the dev repo

cd ~
git clone --recurse-submodules -b v1.71.0 --depth 1 --shallow-submodules https://github.com/grpc/grpc

cd grpc
mkdir -p cmake/build
pushd cmake/build
cmake -DgRPC_INSTALL=ON \
      -DgRPC_BUILD_TESTS=OFF \
      -DCMAKE_CXX_STANDARD=17 \
      -DCMAKE_INSTALL_PREFIX=$MY_INSTALL_DIR \
      ../..
make -j 4
make install
popd

# https://grpc.io/docs/languages/cpp/quickstart/

cd examples/cpp/helloworld
mkdir -p cmake/build
push cmake/build
cmake -DCMAKE_INSTALL_PREFIX=%MY_INSTALL_DIR% ..\..
cmake --build . --config Release -j 4
popd

cd ~/grpc/examples/cpp/helloworld/cmake/build
# in two terminals
./greeter_server
./greeter_client



