extern "C"
{
#include <fuse.h>
};

#include "syscall.hpp"
#include <string>
#include <iostream>

std::string g_realPath;

static struct fuse_operations proxy_operations = {0};

int main(int argc, char *argv[])
{

  if (argc < 3)
    {
      std::cerr << "Usage: proxyfs <realpath> <mountpoint>\n" << std::endl;
      return (1);
    }

  proxy_operations.getattr = &ProxyFS::GetAttr;
  proxy_operations.readdir = &ProxyFS::ReadDir;
  proxy_operations.open = &ProxyFS::Open;
  proxy_operations.read = &ProxyFS::Read;
  proxy_operations.write = &ProxyFS::Write;
  
  g_realPath = std::string(argv[1]);
  argv++;
  argc--;

  std::cout << "mounting FS in " << argv[1] << ", real storage is " << g_realPath << std::endl;

  return fuse_main(argc, argv, &proxy_operations, NULL);
}
