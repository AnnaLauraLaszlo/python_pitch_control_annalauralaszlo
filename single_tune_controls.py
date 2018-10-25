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



def listen_single_tune(keys_pressed):
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
                    keypressed = single_tune_control(command, keys_pressed)
            else:
                active = False
            #check for command completion

        stream.stop_stream()
        stream.close()
        p.terminate()




def single_tune_control(command, keys_pressed):
    command = int(command)
    C_note = list(range(290, 305)) #le
    D_note = list(range(310, 335)) #jobb
    E_note = list(range(345, 375)) #bal
    F_note = list(range(375, 405)) #fel
    G_note = list(range(420, 455)) #ctrl
    A_note = list(range(460, 510)) #enter
    B_note = list(range(516, 520))
    H_note = list(range(521, 570))
    hC_note = list(range(575, 615))
    hD_note = list(range(640, 670))
    hE_note = list(range(720, 750))
    hF_note = list(range(770, 800))
    hG_note = list(range(860, 890))

    if command in C_note:
        key = 'down'
        print("C")
        control_functions.keep_pressing_key(key)
        if key not in keys_pressed:
            keys_pressed.append('down')

    elif command in D_note:
        key = 'right'
        #pyautogui.moveRel(0, 0, 2, pyautogui.easeInQuad)
        print("D")
        control_functions.keep_pressing_key(key)
        if key not in keys_pressed:
            keys_pressed.append('right')

    elif command in E_note:
        key = 'left'
        print("E")
        control_functions.keep_pressing_key(key)
        if key not in keys_pressed:
            keys_pressed.append('left')

    elif command in F_note:
        key = 'up'
        print("F")
        control_functions.keep_pressing_key(key)
        if key not in keys_pressed:
            keys_pressed.append('up')


    elif command in G_note:
        print("G")
        for key in keys_pressed:
            control_functions.release_key(key)
            keys_pressed.remove(key)


    elif command in A_note:
        print("A")
        control_functions.press_key('space')


    elif command in B_note:
        print("B")
        control_functions.press_key('capslock')

    elif command in H_note:
        print("H")
        control_functions.press_key('enter')

    elif command in hC_note:
        print("hC")
        control_functions.press_key('esc')

    elif command in hD_note:
        print("hD")
        control_functions.press_key('down')

    elif command in hE_note:
        print("hE")
        control_functions.press_key('right')

    elif command in hF_note:
        print("hF")
        control_functions.press_key('left')

    elif command in hG_note:
        print("hG")
        control_functions.press_key('up')

    print(keys_pressed)
    return keys_pressed