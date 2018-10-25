import pyaudio
import wave
import sys
import struct
import math
import numpy
import control_functions
import pyautogui
import common


tolerance = 100
not_usable_tune = 0.1
nmd_of_items_in_past = 10



def listen_single_tune():
    while True:
        CHUNK = 2048
        FORMAT = pyaudio.paInt16
        CHANNELS = 2
        RATE = 44100
        RECORD_SECONDS = 100

        window = numpy.blackman(CHUNK)
        swidth = 2

        past = [-1] * nmd_of_items_in_past
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
            data = stream.read(int(CHUNK/2)) #long string with data
            indata = numpy.array(wave.struct.unpack("%dh" % (len(data) / swidth), \
                                                    data)) * window

            # Take fft and square each value
            fftData= abs(numpy.fft.rfft(indata)) ** 2
            # find the max
            which = fftData[1:].argmax() + 1

            if which != len(fftData)-1:
                y0,y1,y2 = numpy.log(fftData[which - 1:which + 2:])
                x1 = (y2 - y0) * .5 / (2 * y1 - y2 - y0)
                # find the frequency and output it
                sound_frequence = (which+x1)*RATE/CHUNK
            else:
                sound_frequence = which*RATE/CHUNK

            #update past
            past.pop(0)
            past.append(sound_frequence)
                #check for part of command
            if common.rms(data)>not_usable_tune:
                if not active and max(past) - min(past) < tolerance:
                    command = int(numpy.mean(past))
                    active = True
                    print(command)
                    singel_tune_control(command)
            else:
                active = False
            #check for command completion

        stream.stop_stream()
        stream.close()
        p.terminate()


def singel_tune_control(command):
    command = int(command)
    C = 0
    D = 1
    E = 2
    F = 3
    B = 4
    A = list(range(360, 400))
    G = 392
    if command == A:
        pyautogui.moveRel(-200, 0, 2, pyautogui.easeInQuad)

    if command == G:
        pyautogui.moveRel(+200, 0, 2, pyautogui.easeInQuad)