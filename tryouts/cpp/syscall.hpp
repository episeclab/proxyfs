#ifndef __SYSCALL_HPP__
# define __SYSCALL_HPP__

extern "C"
{
#include <fuse.h>
};

namespace ProxyFS
{
  int GetAttr(const char *, struct stat *);
  int Open(const char *, struct fuse_file_info *);
  int Read(const char *, char *, size_t, off_t,
	   struct fuse_file_info *);
  int Write(const char *, const char *, size_t, off_t,
	    struct fuse_file_info *);
  int ReadDir(const char *, void *, fuse_fill_dir_t, off_t,
	      struct fuse_file_info *);

}

#endif
