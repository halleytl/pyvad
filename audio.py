#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
实现对pyaudio的封装

控制mic 模块
实现录制音频
播放音频文件
播放音频流数据
"""
from util import save_file
import pyaudio
import wave
import os

SUCCCESS = 0
FAIL = 1

class Audio(object):
    """
    mic 相关
    pyaudio 封装
    """
    def __init__(self, chuck=1024):
        self.audio = pyaudio.PyAudio()
        self.chunk = chuck
        self.r_stream = None
   
    def play_file(self, filename):
        """
        播放音乐文件
        返回：0 成功， 1 失败
        """
        if not os.path.isfile(filename):
            print "文件名%s不存在" % filename
            return 1
        read_file = wave.open(filename, 'rb')
        stream = self.audio.open(format=self.audio.get_format_from_width( \
                                    read_file.getsampwidth()), \
                             channels=read_file.getnchannels(), \
                             rate=read_file.getframerate(), \
                             output=True)
        print "播放文件:\n%s" % filename
        data = read_file.readframes(self.chunk)
        while data != '':
            stream.write(data)
            data = read_file.readframes(self.chunk)
        stream.stop_stream()
        stream.close()
        return SUCCCESS
  
    def play_stream(self, data, format=8, channels=1, rate=16000):
        """
        播放流数据
        """
        print ("播放音频流:\n"
               "format=%s\n"
               "channels=%s\n"
               "rate=%s" )% (format, channels, rate)
        stream = self.audio.open(format=format,
                channels=channels,
                rate=rate,
                output=True)
        stream.write(data)
        stream.stop_stream()
        stream.close()
        return SUCCCESS

    def record_file(self, filename, seconds=10, format=pyaudio.paInt16, \
                    channels=1, rate=16000, buffer=None):
        """
        录制音频到指定文件
        """
        if buffer is None:
            buffer = self.chunk
        print ("开始录制文件:\n"
               "filename = %s\n"
               "record time = %s\n"
               "format = %s\n"
               "channels = %s\n"
               "rate = %s\n"
               "buffer = %s\n") % (filename, seconds, format, channels, rate, 
                                   buffer)
        if filename and os.path.isfile(filename):
            print "文件名%s 已经存在" % filename
            return 1
        stream = self.audio.open(format=format,
                channels=channels,
                rate=rate,
                input=True,
                frames_per_buffer=buffer)
        frames = []
    
        for _num in range(int(rate*1.0 / buffer * seconds)+3):
            data = stream.read(buffer)
            frames.append(data)
        stream.stop_stream()
        stream.close()
        return save_file(b''.join(frames), filename, 
                         self.audio.get_sample_size(format), channels, rate)

    def record_stream_start(self, format=pyaudio.paInt16, channels=1, 
                            rate=16000, buffer=None):
        """
        开启mic 
        """ 
        if buffer is None:
            buffer = self.chunk
        else:
            self.chunk = buffer
        if self.r_stream:
            self.record_stream_end()
        self.r_stream = self.audio.open(format=format,
                channels=channels,
                rate=rate,
                input=True,
                frames_per_buffer=buffer)
        print "开始录音"
        return SUCCCESS

    def record_stream_end(self):
        """
        关闭mic
        """
        if self.r_stream is not None:
            self.r_stream.stop_stream()
            self.r_stream.close()
            print "录音关闭"
        self.r_stream = None
    
    def record_read(self, num=1):
        """ 
        读取指定块数数据
        """
        return self.r_stream.read(self.chunk*num)
