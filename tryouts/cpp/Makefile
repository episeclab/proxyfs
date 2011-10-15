NAME=proxyfs
SRCS=main.cpp syscall.cpp
OBJS=$(SRCS:.cpp=.o)
MFLAGS=-D_FILE_OFFSET_BITS=64 -DFUSE_USE_VERSION=27
CFLAGS+=-O2
LDFLAGS=-lfuse

all: $(OBJS)
	g++ $(OBJS) -o $(NAME) $(LDFLAGS)

.cpp.o:
	g++ $(CFLAGS) $(MFLAGS) -c  $< -o $@

clean:
	rm -f *~
	rm -f *.o

fclean: clean
	rm -f $(NAME)

re: fclean all