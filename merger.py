from scipy.io.wavfile import read, write
import numpy as np

file1 = 'a.wav'
file2 = 'b.wav'

def cutter(sf, data):
    SCAN_TIME = 10 #how many seconds in the beginning do you scan the clap for?
    THRESH_CAP = .8
    #MEMORY_LEN = .3#How many seconds it has to be < threshold before it registers a separate clap
    data = list(map(abs, data[:SCAN_TIME*sf, 0]))
    threshold = max(data)*THRESH_CAP
    last = -99999999999
    for i in range(len(data)):
        if data[i] >= threshold:
            return i

def merge(files, outfile):
    fs = []
    datas = []
    maxlength = 0
    for file in files:
        a, b = read(file)
        fs.append(a)

        time = cutter(a, b)
        datas.append(b[time:])
        maxlength = max(maxlength, len(datas[-1]))

    output = []
    for i in range(maxlength):
        newsample = np.asarray([0,0])
        for data in datas:
            if i < len(data):
                newsample += data[i]
        newsample //= len(datas)
        output.append(newsample)
    print(np.asarray(output))
    write(outfile, fs, np.asarray(output))
