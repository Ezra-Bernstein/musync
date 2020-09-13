from scipy.io.wavfile import read, write
from pydub import AudioSegment
import numpy as np
import subprocess
import os

#get the time of clap
def cutter(filename):
    sf, data = read(filename)
    SCAN_TIME = 51 #how many seconds in the beginning do you scan the clap for?
    THRESH_CAP = .4
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
    temp.export("./tmp/mixed.wav", format="wav")

#merge one cut file into the main wav file
def merge1(f1):
    s1 = AudioSegment.from_wav(f1)
    st = AudioSegment.from_wav("./tmp/mixed.wav")
    temp = s1.overlay(st, position=0)
    temp.export("./tmp/mixed.wav", format="wav")

#everything
def mp4merger(fnames):    
    #preprocessing (mp4 to wav)
    #fnames = ["v1.mp4","v2.mp4","v3.mp4"]
    for i in range(len(fnames)):
        command = "ffmpeg -i /tmp/" + fnames[i] + " /tmp/" + str(i) + ".wav"
        subprocess.call(command, shell=True)
#        subprocess.call(['C:\\Users\\ayush\\Documents\\Extra\\Random Projects\\pennapps2020\\ffmpeg-20200831-4a11a6f-win64-static\\ffmpeg-20200831-4a11a6f-win64-static\\bin\\ffmpeg','-i', os.getcwd()+"\\tmp\\"+fnames[i], os.getcwd()+"\\tmp\\"+str(i)+".wav"])
  
    #cut both to start at clap
    times = []
    secs = []
    for i in range(len(fnames)):
        fs, x = read("./tmp/"+str(i)+".wav")
        times.append(cutter("./tmp/"+str(i)+".wav"))
        secs.append(times[i]/fs)
        write("./tmp/"+str(i)+"_clipped.wav", fs, x[times[i]:])

    #create a combined mixed.wav file
    merge2("./tmp/0_clipped.wav", "./tmp/1_clipped.wav")
    for i in range(2, len(fnames)):
        merge1("./tmp/"+str(i)+"_clipped.wav")

    #cut the video portions of original files and save with "new_" before the original name
    for i in range(len(fnames)):
        command = "ffmpeg -i /tmp/" + fnames[i] + " -ss " + str(secs[i]) + " /tmp/new_" + fnames[i]
        subprocess.call(command, shell=True)
#        subprocess.call(['C:\\Users\\ayush\\Documents\\Extra\\Random Projects\\pennapps2020\\ffmpeg-20200831-4a11a6f-win64-static\\ffmpeg-20200831-4a11a6f-win64-static\\bin\\ffmpeg','-i', os.getcwd()+"\\tmp\\"+fnames[i], '-ss', str(secs[i]), os.getcwd()+"\\tmp\\new_"+fnames[i]])

# mp4merger(["v1.mp4","v2.mp4","v3.mp4"])         
