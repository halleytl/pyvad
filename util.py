#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
基础工具
"""
from datetime import datetime
import wave
import os

def read_file_data(filename):
    """
    输入:需要读取的文件名
    返回:（声道，量化位数，采样率，数据)
    """
    read_file = wave.open(filename, "r")
    params = read_file.getparams()
    nchannels, sampwidth, framerate, nframes = params[:4]
    data = read_file.readframes(nframes)
    return nchannels, sampwidth, framerate, data

def save_file(data, filename=None, sampwidth=2, channels=1, rate=16000):
    """
    保存数据流文件
    """
    if filename is None:
        filename = datetime.now().strftime("%Y%m%d%H%M%S") + "_%s.pcm"
        flag = 0
        while 1:
            tmp = filename % flag
            if os.path.isfile(tmp):
                flag += 1
            else:
                filename = tmp
                break
    print "开始写入数据到文件%s" % filename
    write_file = wave.open(filename, 'wb')
    write_file.setnchannels(channels)
    write_file.setsampwidth(sampwidth)
    write_file.setframerate(rate)
    write_file.writeframes(data)
    write_file.close()
    return filename

        

    
