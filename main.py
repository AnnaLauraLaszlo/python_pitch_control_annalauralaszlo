import pyaudio
import wave
import sys
import struct
import math
import numpy
import control_functions
import pyautogui
import common
import single_tune_controls
import multi_tune_controls



if __name__ == '__main__':
    user_inputs = input("Press 1 for three-pitch mode, press 2 for single pitch activation, 3 to close")
    if user_inputs == '1':
        multi_tune_controls.listen_multi_tune()
    elif user_inputs == '2':
        single_tune_controls.listen_single_tune()
    else:
        exit()

