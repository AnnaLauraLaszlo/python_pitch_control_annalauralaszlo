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
nmb_of_items_in_past = 10


def listen_multi_tune():
    while True:
        CHUNK = 2048
        FORMAT = pyaudio.paInt16
        CHANNELS = 2
        RATE = 44100
        RECORD_SECONDS = 100

        window = numpy.blackman(CHUNK)
        swidth = 2

        past = [-1] * nmb_of_items_in_past
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
                    command.append(numpy.mean(past))
                    active = True
                    print(command)
            else:
                active = False
            #check for command completion
            if len(command) == 3:
                # convert command to string
                command_letters = common.three_pitch_activation(command, tolerance)
                command = []
                common.get_command(command_letters)


        stream.stop_stream()
        stream.close()
        p.terminate()
