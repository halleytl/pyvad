#!/usr/bin/env python
#-*- coding: utf-8 -*-
import sys 
sys.path.append("../")
from RecordParser import StreamParser

if __name__ == "__main__":
    
   stream_test = StreamParser()
   stream_test.open_mic()
   stream_test.callback = stream_test.play_stream
   stream_test.run()





