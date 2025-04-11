echo Compiling

g++ -o cpp2py embedpython.cpp \
  -I/usr/include/python3.11 \
  -Wno-unused-result -Wsign-compare  -O2 -g -pipe -Wall \
  -Werror=format-security -Wp,-D_FORTIFY_SOURCE=2 -Wp,-D_GLIBCXX_ASSERTIONS \
  -fexceptions -fstack-protector-strong -grecord-gcc-switches \
  -m64 -mtune=generic -fasynchronous-unwind-tables -fstack-clash-protection \
  -fcf-protection -D_GNU_SOURCE -fPIC -fwrapv  -DDYNAMIC_ANNOTATIONS_ENABLED=1 \
  -DNDEBUG  -O2 -g -pipe -Wall -Werror=format-security -Wp,-D_FORTIFY_SOURCE=2 \
  -Wp,-D_GLIBCXX_ASSERTIONS -fexceptions -fstack-protector-strong -grecord-gcc-switches \
  -m64 -mtune=generic -fasynchronous-unwind-tables -fstack-clash-protection \
  -fcf-protection -D_GNU_SOURCE -fPIC -fwrapv \
  -L/usr/lib64 -lpython3.11 -lpthread -ldl  -lutil -lm  -Xlinker -export-dynamic

echo Running

./cpp2py