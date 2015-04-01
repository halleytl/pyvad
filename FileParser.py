#!/usr/bin/env python
#-*- coding: utf-8 -*-
import sys
sys.path.append("../")
from vad import Vad
from util import read_file_data
import os
import threading
SUCCESS = 0
FAIL = 1

class FileParser(Vad):
    def __init__(self):
        self.block_size = 256
        Vad.__init__(self)
    def read_file(self, filename):
        print "filename"
        if not os.path.isfile(filename):
            print "文件%s不存在" % filename
            return FAIL
        datas = read_file_data(filename)[-1]     
        datas_size = len(datas)
        tmp =  len(datas)*1.0/self.block_size
        blocks = int(tmp)
        print blocks
        for i in range(blocks):
             self.cache_frames.append(datas[i*self.block_size:(i+1)*self.block_size])
        else:
             end = i+1
             if tmp > int(tmp):
                 pass
             self.cache_frames.append(-1)
                 #data = datas[end*block_size:len(datas_size)]+"\0"*256
                 #self.cache_frames.append(data[:256])
        return SUCCESS

if __name__ == "__main__":
   from audio import Audio
   play = Audio()
   _files = sys.argv[1:] 
   stream_test = FileParser()
   for _file in _files:
       if stream_test.read_file(_file) == SUCCESS:
           print _file
   
   t = threading.Thread(target=stream_test.run)
   #t = threading.Thread(target=stream_test.run, kwargs={"fun":play.play_stream})
   #t.setDaemon(True)
   t.start()
   t.join()
       






