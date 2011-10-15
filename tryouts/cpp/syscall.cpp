#include "syscall.hpp"


#include <fcntl.h>
#include <sys/types.h>
#include <dirent.h>

#include <iostream>

namespace ProxyFS
{
  int GetAttr(const char *path, struct stat *st)
  {
    std::cout << "getattr" <<  std::endl;
    return 0;
  }

  int Open(const char *path, struct fuse_file_info *info)
  {
    std::cout << "open" << std::endl;
    return 0;
  }

  int Read(const char *, char *, size_t, off_t,
	   struct fuse_file_info *)
  {
    std::cout << "read"  << std::endl;
    return 0;
  }

  int Write(const char *path, const char *test, size_t size, off_t offset,
	    struct fuse_file_info *info)
  {
    std::cout << path << " : "  << test << " : " << size << " : " << offset << std::endl;
    return 0;
  }

  int ReadDir(const char *, void *, fuse_fill_dir_t, off_t,
	      struct fuse_file_info *)
  {
    std::cout << "readdir" << std::endl;
    return 0;
  }

}
