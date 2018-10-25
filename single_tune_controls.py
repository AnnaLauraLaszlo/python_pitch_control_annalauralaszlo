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
nmd_of_items_in_past = 5



def listen_single_tune():
    while True:
        CHUNK = 2048 #2 bit
        FORMAT = pyaudio.paInt16 #16 bit representation
        CHANNELS = 2
        RATE = 44100  # 44 kHz mintavétel, megméri a feszültségét
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


        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)): #beolvasás
            data = stream.read(int(CHUNK/2)) #long string with data
            indata = numpy.array(wave.struct.unpack("%dh" % (len(data) / swidth), \
                                                    data)) * window

            # Take fft and square each value
            fftData= abs(numpy.fft.rfft(indata)) ** 2 #fast fourier transformation
            # find the max
            which = fftData[1:].argmax() + 1

            if which != len(fftData)-1:  #legdominnsabb frekvencia
                y0,y1,y2 = numpy.log(fftData[which - 1:which + 2:])
                x1 = (y2 - y0) * .5 / (2 * y1 - y2 - y0)
                # find the frequency and output it
                sound_frequence = (which+x1)*RATE/CHUNK #el van tolva, amit visszakapok
            else:
                sound_frequence = which*RATE/CHUNK
                #which = index
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
    C_note = list(range(290, 305)) #bal
    D_note = list(range(310, 335)) #jobb
    E_note = list(range(345, 375)) #le
    F_note = list(range(376, 405)) #fel
    G_note = list(range(420, 455)) #ctrl
    A_note = list(range(460, 504)) #enter
    B_note = list(range(516, 544))
    H_note = list(range(545, 570))
    hC_note = list(range(575, 596))

    if command in C_note:
        print("C")
        control_functions.press_key('right')


        #pyautogui.moveRel(-20, 0, 2, pyautogui.easeInQuad)

    if command in D_note:
        #pyautogui.moveRel(0, 0, 2, pyautogui.easeInQuad)
        print("D")
        control_functions.press_key('left')


    if command in E_note:
        print("E")
        control_functions.press_key('down')


    if command in F_note:
        print("F")
        control_functions.press_key('up')


    if command in G_note:
        print("G")
        control_functions.press_key('ctrl')


    if command in A_note:
        print("A")
        control_functions.press_key('enter')


    if command in B_note:
        print("B")

    if command in H_note:
        print("H")

    if command in hC_note:
        print("hC")

