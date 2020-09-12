from scipy.io.wavfile import read, write
import numpy as np
import subprocess

#2 mp4 files to 2 wav files
#subprocess.call(['C:\\Users\\ayush\\Documents\\Extra\\Random Projects\\pennapps2020\\ffmpeg-20200831-4a11a6f-win64-static\\ffmpeg-20200831-4a11a6f-win64-static\\bin\\ffmpeg', '-i', "C:\\Users\\ayush\\Documents\\Extra\\Random Projects\\pennapps2020\\tough_time.mp4", "C:\\Users\\ayush\\Documents\\Extra\\Random Projects\\pennapps2020\\aa.wav"])
#subprocess.call(['C:\\Users\\ayush\\Documents\\Extra\\Random Projects\\pennapps2020\\ffmpeg-20200831-4a11a6f-win64-static\\ffmpeg-20200831-4a11a6f-win64-static\\bin\\ffmpeg', '-i', "C:\\Users\\ayush\\Documents\\Extra\\Random Projects\\pennapps2020\\slowclap.mp4", "C:\\Users\\ayush\\Documents\\Extra\\Random Projects\\pennapps2020\\bb.wav"])
file1 = 'a.wav'
file2 = 'b.wav'
file3 = 'c.wav'
file4 = 'd.wav'

def cutter(filename):
    sf, data = read(filename)
    SCAN_TIME = 10 #how many seconds in the beginning do you scan the clap for?
    THRESH_CAP = .8
    MEMORY_LEN = .3#How many seconds it has to be < threshold before it registers a separate clap
    data = list(map(abs, data[:SCAN_TIME*sf]))
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
f3, z = read(file3)
f4, d = read(file4)
time1 = cutter(file1)
sec1 = time1/fs
time2 = cutter(file2)
sec2 = time2/f2
time3 = cutter(file3)
sec3 = time3/f3
time4 = cutter(file4)
sec4 = time4/f4
x = x[time1:]
y = y[time2:]
z = z[time3:]
d = d[time4:]
#if(x.size>y.size):
#    temp = y
#    y = x
#    x = temp
#z = y.copy()
#z[:x.shape[0]] +=  x
write('clipAA.wav', fs, x)
write('clipBB.wav', f2, y)
write('clipCC.wav', f3, z)
write('clipDD.wav', f4, d)

#merge the cut files into a single wav file
from pydub import AudioSegment
from pydub.playback import play
sound1 = AudioSegment.from_wav("clipAA.wav")
sound2 = AudioSegment.from_wav("clipBB.wav")
sound3 = AudioSegment.from_wav("clipCC.wav")
sound4 = AudioSegment.from_wav("clipDD.wav")
tmpsound = sound1.overlay(sound2, position=0)
tmpsound2 = sound3.overlay(tmpsound, position=0)
tmpsound3 = sound4.overlay(tmpsound2, position=0)
tmpsound3.export("mixed_sounds.wav", format="wav")

#seconds1 = str(sec1) # has to be a string
#seconds2 = str(sec2) # has to be a string
#subprocess.call(['C:\\Users\\ayush\\Documents\\Extra\\Random Projects\\pennapps2020\\ffmpeg-20200831-4a11a6f-win64-static\\ffmpeg-20200831-4a11a6f-win64-static\\bin\\ffmpeg', '-i', "C:\\Users\\ayush\\Documents\\Extra\\Random Projects\\pennapps2020\\tough_time.mp4", '-ss', seconds1, "C:\\Users\\ayush\\Documents\\Extra\\Random Projects\\pennapps2020\\clippedAA.mp4"])
#subprocess.call(['C:\\Users\\ayush\\Documents\\Extra\\Random Projects\\pennapps2020\\ffmpeg-20200831-4a11a6f-win64-static\\ffmpeg-20200831-4a11a6f-win64-static\\bin\\ffmpeg', '-i', "C:\\Users\\ayush\\Documents\\Extra\\Random Projects\\pennapps2020\\slowclap.mp4", '-ss', seconds2, "C:\\Users\\ayush\\Documents\\Extra\\Random Projects\\pennapps2020\\clippedBB.mp4"])

