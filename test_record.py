#!/usr/bin/env python
#-*- coding: utf-8 -*-
import sys 
sys.path.append("../")
from audio import Audio
from vad import Vad 
import threading

class StreamParser(Vad):
    def __init__(self):
        self.record = Audio(chuck=256)
        self.active = False
        self.play =Audio()
        Vad.__init__(self)
   
    def start_mic(self):
        print "start recording"
        t = threading.Thread(target=self.mic_record)
        t.setDaemon(True)
        t.start()

    def mic_record(self):
        self.record.record_stream_start()
        self.active = True
        print "The microphone has opened"
        while self.active: 
            data = self.record.record_read()
            self.cache_frames.append(data)
        self.record.record_stream_end()

    def close_mic(self):
        print "close_mic() enable"
        if self.record:
            self.active = False

    def play_stream(self, data):
        self.play.play_stream(data)

if __name__ == "__main__":
    
   stream_test = StreamParser()
   stream_test.start_mic()
   stream_test.run(fun=stream_test.play_stream)





