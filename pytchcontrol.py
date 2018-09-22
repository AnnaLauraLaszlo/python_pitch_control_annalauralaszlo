import pyaudio
import wave
import sys
import struct
import math
import numpy as np
import control_functions
import pyautogui
import common



#--------CONSTANTS----------
tolerance = 100
THRESH = 0.1
N = 10


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

        print("* waiting for command")

        
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
                    sound_frequence = (which+x1)*RATE/CHUNK
                else:
                    sound_frequence = which*RATE/CHUNK

                #update past
                past.pop(0)
                past.append(sound_frequence)
                #check for part of command
                if rms(data)>THRESH:
                    if not active and max(past) - min(past) < tolerance:
                        command.append(np.mean(past))
                        active = True
                        print(command)
                else:
                    active = False
                #check for command completion

                common.get_command(command, tolerance)

    print("* done")


    stream.stop_stream()
    stream.close()
    p.terminate()


if __name__ == '__main__':
    user_inputs = input("Press 1 for wasd mode, press 2 for single ")
    if user_inputs == '1':
        listen()
    elif user_inputs == '2':
        pass

