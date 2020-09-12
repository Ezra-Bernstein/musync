from scipy.io.wavfile import read, write
import numpy as np
import subprocess

#2 mp4 files to 2 wav files
subprocess.call(['C:\\Users\\ayush\\Documents\\Extra\\Random Projects\\pennapps2020\\ffmpeg-20200831-4a11a6f-win64-static\\ffmpeg-20200831-4a11a6f-win64-static\\bin\\ffmpeg', '-i', "C:\\Users\\ayush\\Documents\\Extra\\Random Projects\\pennapps2020\\putin.mp4", "C:\\Users\\ayush\\Documents\\Extra\\Random Projects\\pennapps2020\\aa.wav"])
subprocess.call(['C:\\Users\\ayush\\Documents\\Extra\\Random Projects\\pennapps2020\\ffmpeg-20200831-4a11a6f-win64-static\\ffmpeg-20200831-4a11a6f-win64-static\\bin\\ffmpeg', '-i', "C:\\Users\\ayush\\Documents\\Extra\\Random Projects\\pennapps2020\\slowclap.mp4", "C:\\Users\\ayush\\Documents\\Extra\\Random Projects\\pennapps2020\\bb.wav"])
file1 = 'aa.wav'
file2 = 'bb.wav'

def cutter(filename):
    sf, data = read(filename)
    SCAN_TIME = 10 #how many seconds in the beginning do you scan the clap for?
    THRESH_CAP = .8
    MEMORY_LEN = .3#How many seconds it has to be < threshold before it registers a separate clap
    data = list(map(abs, data[:SCAN_TIME*sf,0]))
    threshold = max(data)*THRESH_CAP
    last = -99999999999
    for i in range(len(data)):
        if data[i] >= threshold and i > last + MEMORY_LEN * sf:
            last = i
            break
    return last

#cut both to start at clap
fs, x = read(file1)
f2, y = read(file2)
time1 = cutter(file1)
sec1 = time1/fs
time2 = cutter(file1)
sec2 = time2/f2
x = x[time1:]
y = y[time2:]
if(x.size>y.size):
    temp = y
    y = x
    x = temp
z = y.copy()
z[:x.shape[0]] +=  x
write('merged.wav', fs, z)
seconds = str(sec1) # has to be a string
subprocess.call(['C:\\Users\\ayush\\Documents\\Extra\\Random Projects\\pennapps2020\\ffmpeg-20200831-4a11a6f-win64-static\\ffmpeg-20200831-4a11a6f-win64-static\\bin\\ffmpeg', '-i', "C:\\Users\\ayush\\Documents\\Extra\\Random Projects\\pennapps2020\\putin.mp4", '-ss', seconds, "C:\\Users\\ayush\\Documents\\Extra\\Random Projects\\pennapps2020\\putinCLIPPED.mp4"])

