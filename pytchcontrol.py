import pyaudio
import wave
import sys
import struct
import math
import numpy as np
import control_functions
import pyautogui



#--------CONSTANTS----------
TOLERANCE = 100
THRESH = 0.1
N = 10


#---------COMMANDS----------

# n = neutral, u = up, d = down
commands = ['uu', 'dd','nn','ud', 'du']



def rms(data):
    count = len(data)/2
    format = "%dh"%(count)
    shorts = struct.unpack( format, data )
    sum_squares = 0.0
    for sample in shorts:
        n = sample * (1.0/32768)
        sum_squares += n*n
    return math.sqrt( sum_squares / count )


def listen():
    while True:
        CHUNK = 2048
        FORMAT = pyaudio.paInt16
        CHANNELS = 2
        RATE = 44100
        RECORD_SECONDS = 100

        window = np.blackman(CHUNK)
        swidth = 2

        past = [-1]*N
        command = []
        active = False
        
        p = pyaudio.PyAudio()

        stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

        print("* listening for command")

        
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                data = stream.read(int(CHUNK/2))
                indata = np.array(wave.struct.unpack("%dh"%(len(data)/swidth),\
                                         data))*window
                
                # Take fft and square each value
                fftData=abs(np.fft.rfft(indata))**2
                # find the max
                which = fftData[1:].argmax() + 1
                
                if which != len(fftData)-1:
                    y0,y1,y2 = np.log(fftData[which-1:which+2:])
                    x1 = (y2 - y0) * .5 / (2 * y1 - y2 - y0)
                    # find the frequency and output it
                    thefreq = (which+x1)*RATE/CHUNK
                else:
                    thefreq = which*RATE/CHUNK

                #update past
                past.pop(0)
                past.append(thefreq)
                #check for part of command
                if rms(data)>THRESH:
                    if not active and max(past) - min(past) < TOLERANCE:
                        command.append(np.mean(past))
                        active = True
                        print(command)
                else:
                    active = False
                #check for command completion

                if len(command)==3:
                    #convert command to string
                    comstr = ''
                    for i in range(len(command)-1):
                        t = command[i+1] - command[i]
                        if abs(t)<TOLERANCE:
                            comstr += 'n'
                        elif t > 0:
                            comstr += 'u'
                        else:
                            comstr += 'd'
                    if comstr in commands:
                        if comstr == 'uu':
                           control_functions.press_key('w')
                           #control_functions.open_website('https://www.facebook.com/')
                        if comstr == 'dd':
                            control_functions.press_key('s')
                            #control_functions.open_website('https://www.youtube.com/')
                        if comstr == 'ud':
                            control_functions.press_key('d')
                            #control_functions.press_key('HEllo world!!!')
                        if comstr == 'du':
                            control_functions.press_key('a')
                        if comstr == 'nn':
                            pass
                    command = []

    print("* done")


    stream.stop_stream()
    stream.close()
    p.terminate()


if __name__ == '__main__':
    listen()

