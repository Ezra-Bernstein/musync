from scipy.io.wavfile import read, write
import numpy as np

sf, data = read("test2.wav")

SCAN_TIME = 10 #how many seconds in the beginning do you scan the clap for?
THRESH_CAP = .8
MEMORY_LEN = .3#How many seconds it has to be < threshold before it registers a separate clap
data = list(map(abs, data[:SCAN_TIME*sf, 0]))
threshold = max(data)*THRESH_CAP

timestamps = []
last = -99999999999
for i in range(len(data)):
    if data[i] >= threshold and i > last + MEMORY_LEN * sf:
        last = i
        timestamps.append(i/sf)

        




print(timestamps)
