import subprocess

def extract_wav(infile, outfile):
    
    command = "ffmpeg -i " + infile + " " + outfile
    subprocess.call(command, shell=True)
