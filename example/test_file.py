#!/usr/bin/env python
#-*- coding: utf-8 -*-
import sys
sys.path.append("../")
from FileParser import FileParser
import threading
SUCCESS = 0
FAIL = 1

if __name__ == "__main__":
   #from audio import Audio
   #play = Audio()
   _files = sys.argv[1:] 
   if not _files:
       print "需要执行命令\"python %s 1.pcm\"" % __file__
       sys.exit(1)
   stream_test = FileParser()
   for _file in _files:
       if stream_test.read_file(_file) == SUCCESS:
           print _file
   
   t = threading.Thread(target=stream_test.run)
   #t = threading.Thread(target=stream_test.run, kwargs={"fun":play.play_stream})
   #t.setDaemon(True)
   t.start()
   t.join()
       






