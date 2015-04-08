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
        if not os.path.isfile(filename):
            print "文件%s不存在" % filename
            return FAIL
        datas = read_file_data(filename)[-1]     
        self.add(datas, False)

if __name__ == "__main__":
   #from audio import Audio
   #play = Audio()
   _file = sys.argv[1] 
   stream_test = FileParser()
   stream_test.read_file(_file)
   
   t = threading.Thread(target=stream_test.run)
   #t = threading.Thread(target=stream_test.run, kwargs={"fun":play.play_stream})
   #t.setDaemon(True)
   t.start()
   t.join()
       






