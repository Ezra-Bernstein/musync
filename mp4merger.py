from scipy.io.wavfile import read, write
from pydub import AudioSegment
import numpy as np
import subprocess
import os

#get the time of clap
def cutter(filename):
    sf, data = read(filename)
    SCAN_TIME = 51 #how many seconds in the beginning do you scan the clap for?
    THRESH_CAP =  .4
    if data.ndim == 1:
        data = list(map(abs, data[:SCAN_TIME*sf]))
    else:
        data = list(map(abs, data[:SCAN_TIME*sf, 0]))
    threshold = max(data)*THRESH_CAP
    for i in range(len(data)):
        if data[i] >= threshold:
            return i
        
#merge two cut files into a single wav file
def merge2(f1, f2):
    s1 = AudioSegment.from_wav(f1)
    s2 = AudioSegment.from_wav(f2)
    temp = s1.overlay(s2, position=0)
    temp.export("/tmp/mixed.wav", format="wav")

#merge one cut file into the main wav file
def merge1(f1):
    s1 = AudioSegment.from_wav(f1)
    st = AudioSegment.from_wav("/tmp/mixed.wav")
    temp = s1.overlay(st, position=0)
    temp.export("/tmp/mixed.wav", format="wav")

#everything
def mp4merger(fnames):    
    #preprocessing (mp4 to wav)
    #fnames = ["v1.mp4","v2.mp4","v3.mp4"]
    for i in range(len(fnames)):
        command = "ffmpeg -i /tmp/" + fnames[i] + " /tmp/" + str(i) + ".wav"
        subprocess.call(command, shell=True)
        
    #cut both to start at clap
    times = []
    secs = []
    tup = []
    for i in range(len(fnames)):
        fs, x = read("/tmp/"+str(i)+".wav")
        times.append(cutter("/tmp/"+str(i)+".wav"))
        secs.append(times[i]/fs)
        write("/tmp/"+str(i)+"_clipped.wav", fs, x[times[i]:])
        tup.append((str(i),len(x[times[i]:])))
    tup.sort(key=lambda x: (x[1]))

    #create a combined mixed.wav fileS        
    merge2("/tmp/"+tup[0][0]+"_clipped.wav", "/tmp/"+tup[1][0]+"_clipped.wav")
    for i in range(2, len(fnames)):
        merge1("/tmp/"+tup[i][0]+"_clipped.wav")

    #cut the video portions of original files and save with "new_" before the original name
    for i in range(len(fnames)):
        bool1 = False
        for j in range(len(fnames[i])):
            if(not bool1 and fnames[i][len(fnames[i])-j-1]=="/"):
                bool1 = True
            elif(fnames[i][len(fnames[i])-j-1]=="/"):
                os.mkdir("/tmp/new_" + fnames[i][:j-2])
                break
        command = "ffmpeg -i /tmp/" + fnames[i] + " -ss " + str(secs[i]) + " /tmp/new_" + fnames[i]
        subprocess.call(command, shell=True)
        
