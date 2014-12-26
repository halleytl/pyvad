#!/usr/bin/env python
#-*- coding: utf-8 -*-
import sys 
sys.path.append("../")
from RecordParser import StreamParser

if __name__ == "__main__":
    
   stream_test = StreamParser()
   stream_test.start_mic()
   stream_test.run(fun=stream_test.play_stream)





