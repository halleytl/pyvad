#!/usr/bin/env python
#-*- coding: utf-8 -*-

from time import sleep
import math
import wave
import numpy as np
from base import Audio
import threading 

#需要添加录音互斥功能能,某些功能开启的时候录音暂时关闭
def ZCR(wave_data):
    curFrame = wave_data[np.arange(0, len(wave_data))]
    tmp1 = curFrame[:-1]
    tmp2 = curFrame[1:]
    sings = (tmp1*tmp2<=0)
    diffs = (tmp1-tmp2)>0.02
    zcr = np.sum(sings*diffs)
    return zcr

def short_energy(wave_data):
    curFrame = wave_data[np.arange(0, len(wave_data))]
    amp = np.sum(np.abs(curFrame))
    return amp


def get_text(auth, data):
    auth.session_begin()
    res = auth.get_result(data)
    auth.session_end()
    return res


class Vad(object):
    def __init__(self): #初始短时能量高门限
        self.amp1 = 140
        #初始短时能量低门限
        self.amp2 = 120
        #初始短时过零率高门限
        self.zcr1 = 10
        #初始短时过零率低门限
        self.zcr2 = 5
        #允许最大静音长度
        self.maxsilence = 100
        #语音的最短长度
        self.minlen = 40
        #偏移值
        self.offsets = 40
        self.offsete = 200
        #初始状态为静音
        self.max_en = 20000
        self.status = 0
        self.count = 0
        self.silence = 0
        self.frame_len = 256
        #self.frame_inc = 80
        self.frame_inc = 128
        self.cur_status = 0
        self.frames = []
        self.frames_start = []
        self.frames_start_num = 0
        self.frames_end = []
        self.frames_end_num = 0
        self.record_frames = []
        self.record_frames_num = 0
        self.record = Audio(chuck=self.frame_len)
        self.active = False
        self.end_flag = False
        self.play = Audio()
        #    pass
    def play_data(self, data):
        t= threading.Thread(target=self.play.play_stream, args=(data,))
        t.setDaemon(True)
        t.start()

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
            self.record_frames.append(data)

        self.record.record_stream_end()
 
        #    self.close_mic()
    def close_mic(self):
        print "close_mic() enable"
        if self.record:
            self.active = False
            
    def run(self, fun=None):
        play = Audio()
        #record_stream = self.record.read_file_data("1.pcm")[-1]
        #wave_data = np.fromstring(record_stream, dtype=np.int16)
        step = self.frame_len - self.frame_inc
        num = 0
        while 1:
            #开始端点
            #获得音频文件数字信号
            #print "--record---"
            if len(self.record_frames) <2:
                sleep(1)
                continue
            record_stream = "".join(self.record_frames[:2])
            wave_data = np.fromstring(record_stream, dtype=np.int16)
            #print wave_data[np.arange(0, self.frame_len)]
            #raw_input()
            wave_data = wave_data*1.0/self.max_en  
            data = wave_data[np.arange(0, self.frame_len)]
            speech_data = self.record_frames.pop(0)
            #speech_data = tmpwd[np.arange(num*step, num*step +self.frame_len)]
            #获得音频过零率
            zcr = ZCR(data)
            #获得音频的短时能量, 平方放大
            amp = short_energy(data)**2
            #返回当前音频数据状态
            res = self.speech_status(amp, zcr)
            print res,
            num = num+1
            self.frames_start.append(speech_data)
            self.frames_start_num += 1
            if self.frames_start_num == self.offsets:
                #开始音频开始的缓存部分
                self.frames_start.pop(0)
                self.frames_start_num -=1
            if self.end_flag:  
                 #当音频结束后进行后部缓存
                 self.frames_end_num +=1
                 #下一段语音开始，或达到缓存阀值
                 if res == 2 or self.frames_end_num == self.offsete :
                     self.play.play_stream(b"".join(self.frames+self.frames_end))
                     #数据环境初始化
                     self.end_flag = False
                     self.frames = []
                     self.frames_end_num = 0
                   
                 self.frames_end.append(speech_data) 
            if res == 2:
                if self.cur_status in [0, 1]:
                    #添加开始偏移数据到数据缓存
                    self.frames.append(b"".join(self.frames_start))
                #添加当前的语音数据
                self.frames.append(speech_data)
            if res == 3:
               
                self.frames.append(speech_data)
                #开启音频结束标志
                self.end_flag = True
                #play.play_stream(b"".join(self.frames))
                #加上前后偏移数据后，然后调用相关函数
            self.cur_status = res

    def speech_status(self, amp, zcr):
        status = 0
        # 0= 静音， 1= 可能开始
        if self.cur_status in [0, 1]: 
            # 确定进入语音段
            if amp > self.amp1:       
                status = 2
                self.silence = 0
                self.count += 1
            #可能处于语音段 
            elif amp > self.amp2 or zcr > self.zcr2: 
                status = 1
                self.count += 1
            #静音状态
            else:  
                #amp1 = min(amp1, amp)
                status = 0
                self.count = 0
                self.count =0
        # 2 = 语音段
        elif self.cur_status == 2:              
            # 保持在语音段
            if amp > self.amp2 or zcr > self.zcr2:
                self.count += 1
                status = 2
            #语音将结束
            else:
                #静音还不够长，尚未结束
                self.silence += 1
                if self.silence < self.maxsilence:
                    self.count += 1
                    status = 2
                #语音长度太短认为是噪声
                elif self.count < self.minlen:
                    status = 0
                    self.silence = 0
                    self.count = 0
                #语音结束
                else:
                    status = 3
                    self.silence =0
                    self.count = 0
        return status

if __name__ == "__main__":
    a = Vad()
    a.start_mic()
    a.run()
