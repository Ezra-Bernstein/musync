from scipy.io.wavfile import read, write
import numpy as np

file1 = 'a.wav'
file2 = 'b.wav'

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

fs, x = read(file1)
f2, y = read(file2)
time1 = cutter(file1)
time2 = cutter(file1)
x = x[time1:]
y = y[time2:]
if(x.size>y.size):
    temp = y
    y = x
    x = temp
#x < y
z = y.copy()
z[:x.shape[0]] +=  x
write('merged.wav', fs, z)
