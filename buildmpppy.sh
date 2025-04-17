## sudo yum update
## sudo yum install python3-devel
## sudo yum install platform-python-devel
## sudo yum groupinstall "Development Tools"
## sudo yum install -y build-essential autoconf libtool pkg-config

echo Compiling

g++ -o mpppy embeddedmultiprocesspython.cpp $(python3.11-config --cflags --ldflags --embed)

# g++ -o mpppy embeddedmultiprocesspython.cpp \
#   -I/usr/include/python3.11 \
#   -Wno-unused-result -Wsign-compare  -O2 -g -pipe -Wall \
#   -Werror=format-security -Wp,-D_FORTIFY_SOURCE=2 -Wp,-D_GLIBCXX_ASSERTIONS \
#   -fexceptions -fstack-protector-strong -grecord-gcc-switches \
#   -m64 -mtune=generic -fasynchronous-unwind-tables -fstack-clash-protection \
#   -fcf-protection -D_GNU_SOURCE -fPIC -fwrapv  -DDYNAMIC_ANNOTATIONS_ENABLED=1 \
#   -DNDEBUG  -O2 -g -pipe -Wall -Werror=format-security -Wp,-D_FORTIFY_SOURCE=2 \
#   -Wp,-D_GLIBCXX_ASSERTIONS -fexceptions -fstack-protector-strong -grecord-gcc-switches \
#   -m64 -mtune=generic -fasynchronous-unwind-tables -fstack-clash-protection \
#   -fcf-protection -D_GNU_SOURCE -fPIC -fwrapv \
#   -L/usr/lib64 -lpython3.11 -lpthread -ldl  -lutil -lm  -Xlinker -export-dynamic

if [ $? -ne 0 ]; then
exit $?
fi

echo Running
time ./mpppy
