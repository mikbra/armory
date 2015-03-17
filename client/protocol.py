__author__ = 'kra869'
from collections import namedtuple

import struct
import math
import sys
import os
import urlparse

Message = namedtuple('Message', ['msg', 'params'])
Push = namedtuple('Push', "package, hash");

HEADER_STRUCT = "BL"

NAME=str(os.getpid())

def debug(msg):
    sys.stderr.write(NAME+":"+msg+"\n")

def write_msg(output, msg):
    length = "{0:0{1}x}".format(len(msg) + 2, 3)
    n = output.write(length+" "+msg+"\n")
    output.flush()
    
    return n
    
    
def read_msg(input):
    line = input.readline().split();
    params = []
    if len(line) < 2:
        return Message(msg="error", params=params)
        
    if len(line) > 2:
        params = line[2:]
    
    return Message(msg=line[1], params=params)
    
def write_file(output, file, hash):
    BLOCKSIZE = 65000
    pack_size = os.path.getsize(file)
    
    debug("writing block header")
    header = struct.pack(HEADER_STRUCT, 10, pack_size)
    output.write(header);
    debug("pack_size="+str(pack_size)+" header="+str(len(header)));
    output.flush();
    
    with open(file, 'rb') as f:
        buf = f.read(BLOCKSIZE)
        while len(buf) > 0:
            output.write(buf)
            output.flush()
            buf = f.read(BLOCKSIZE)
            
            
    return pack_size
    
def write_empty_file(output, hash):
    pack_size = 0
    
    debug("writing block header")
    header = struct.pack(HEADER_STRUCT, 10, pack_size)
    output.write(header);
    debug("pack_size="+str(pack_size)+" header="+str(len(header)));
    output.flush();
    
    return pack_size
    
def read_file(input, dest_file, hash):
    
    BLOCKSIZE = 65000

    header_size = struct.calcsize(HEADER_STRUCT)
    debug("reading header="+str(header_size))
    header = struct.unpack(HEADER_STRUCT, input.read(header_size));
    
    remaining = header[1];
    debug("total="+str(remaining))
    
    with open(dest_file, "w+") as f:
        while remaining > 0:
            
            N = min(BLOCKSIZE, remaining)
            buf = input.read(N);
            remaining -= len(buf);
            f.write(buf)
    
    return header[0]