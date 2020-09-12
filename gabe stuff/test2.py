from scipy.io.wavfile import read, write
import numpy as np

sf, data = read("test.wav")

data /= 2

write("new.wav", sf, data)

