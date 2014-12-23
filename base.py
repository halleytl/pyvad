#!/usr/bin/env python
#-*- coding: utf-8 -*-
from time import sleep
import math
import wave
import numpy as np
import matplotlib.pyplot as plt
import pyaudio
import sys
import os

class Audio(object):
    def __init__(self, chuck=1024):
        self.p = pyaudio.PyAudio()
        self.chunk = chuck
        self.r_stream = None
   
    def read_file_data(self, filename):
        fw = wave.open(filename, "r")
        params = fw.getparams()
        nchannels, sampwidth, framerate, nframes = params[:4]
        data = fw.readframes(nframes)
        return nchannels, sampwidth, framerate, data

    def play_file(self, filename):
        print "播放文件:\n%s" % filename
        wf = wave.open(filename, 'rb')
        stream = self.p.open(format=self.p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)

        data = wf.readframes(self.chunk)
        while data != '':
            stream.write(data)
            data = wf.readframes(self.chunk)

        stream.stop_stream()
        stream.close()
  
    def play_stream(self, data, format=pyaudio.paInt16, channels=1, rate=16000):
        print "播放音频流:\nformat=%s\nchannels=%s\nrate=%s" % (format, channels, rate)
        stream = self.p.open(format=format,
                channels=channels,
                rate=rate,
                output=True)
        stream.write(data)
        stream.stop_stream()
        stream.close()

    def record_file(self, filename, seconds=10, format=pyaudio.paInt16, channels=1, rate=16000, buffer=None):
        if buffer is None:
            buffer = self.chunk
        print """开始录制文件:
filename = %s
record time = %s
format = %s
channels = %s
rate = %s
buffer = %s
        """ % (filename, seconds, format, channels, rate, buffer)
        if os.path.isfile(filename):
            print "文件名%s 已经存在" % filename
            sys.exit(1)
        stream = self.p.open(format=format,
                channels=channels,
                rate=rate,
                input=True,
                frames_per_buffer=buffer)
        frames = []
    
        print rate*1.0 / buffer * seconds
        for i in range(int(rate*1.0 / buffer * seconds)+3):
            data = stream.read(buffer)
            frames.append(data)
        stream.stop_stream()
        stream.close()
        wf = wave.open(filename, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(self.p.get_sample_size(format))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))
        wf.close()

    def record_stream_start(self, format=pyaudio.paInt16, channels=1, rate=16000, buffer=None):
        print "开始录音"
        if buffer is None:
            buffer = self.chunk
        else:
            self.chunk = buffer
        if self.r_stream:
            self.record_stream_end()
        self.r_stream = self.p.open(format=format,
                channels=channels,
                rate=rate,
                input=True,
                frames_per_buffer=buffer)

    def record_stream_end(self):
        if self.r_stream is not None:
            self.r_stream.stop_stream()
            self.r_stream.close()
        self.r_stream = None
    
    def record_read(self, num=1):
        return self.r_stream.read(self.chunk*num)
 
if __name__ == "__main__":
    #_file = sys.argv[1]
    """
    # 1 test play file
    #os.system("mplayer %s" % _file)
    Audio().play_file(_file)
    # 2 test play stream
    fw = wave.open(_file,'r')
    params = fw.getparams()
    nchannels, sampwidth, framerate, nframes = params[:4]
    data = fw.readframes(nframes)
    fw.close() 
    Audio().play_stream(data)
    """
    # 3 test record file
    record = Audio()
    play = Audio()
    record.record_stream_start()
    frames = []
    count = 0
    while 1:
        data = record.record_read()
        frames.append(data)
        count +=1
        print count
        if count%5 == 0:
            record.record_stream_end()
            play.play_stream(b"".join(frames))
            frames = []
            count = 0
            record.record_stream_start()
       
        

    
