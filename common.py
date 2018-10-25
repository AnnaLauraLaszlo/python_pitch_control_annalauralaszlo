import control_functions
import pyautogui
import pyaudio
import pytchcontrol
import wave
import sys
import struct
import math
import numpy
import common



def create_command_list(data, command, past, tolerance):
    usable_sound = 0.01
    active = False
    if not active and pytchcontrol.rms(data) > usable_sound:
        if max(past) - min(past) < tolerance:
            print("numpy.mean(past):%s" % numpy.mean(past))
            command.append(numpy.mean(past))  # arithmetic mean
            active = True
            print("command:%s" % command)
        else:
            active = False

    return command



def get_command(command_letters):
    print(command_letters)
    command_options = ['uu', 'dd', 'nn', 'ud', 'du', 'un', 'dn', 'nd', 'nu']
    if command_letters in command_options:
        if command_letters == 'uu':
            #pyautogui.moveTo(100, 200, 2, pyautogui.easeInQuad)
            pyautogui.moveRel(-200, 0, 2, pyautogui.easeInQuad)
            #control_functions.press_key('w')
            #control_functions.open_website('https://www.facebook.com/')
        elif command_letters == 'dd':
            #control_functions.press_key('s')
            #pyautogui.moveTo(300, 500, 2, pyautogui.easeInQuad)
            pyautogui.moveRel(200, 0, 2, pyautogui.easeInQuad)
            #control_functions.open_website('https://www.youtube.com/')
        elif command_letters == 'ud':
            #pyautogui.moveTo(600, 400, 2, pyautogui.easeInQuad)
            pyautogui.moveRel(0, 200, 2, pyautogui.easeInQuad)
            #control_functions.press_key('d')
            # control_functions.press_key('HEllo world!!!')
        elif command_letters == 'du':
            #pyautogui.moveTo(1000, 1000, 2, pyautogui.easeInQuad)
            pyautogui.moveRel(0, -200, 2, pyautogui.easeInQuad)
            #control_functions.press_key('a')
        else:
            pyautogui.moveTo(700, 380, 2, pyautogui.easeInQuad)
            #control_functions.open_website('https://www.youtube.com/')

            #control_functions.press_key('not yet implemented')


def three_pitch_activation(command, tolerance):
    # check for command completion
        # convert command to string
    command_letters = ''
    for i in range(len(command) - 1):  # checking if the commands are higher or lower in the list_of_command
        difference_of_pitch = command[i + 1] - command[i]
        print("pitchdifference: %s" % difference_of_pitch)
        if abs(difference_of_pitch) < tolerance:
            command_letters += 'n'
        elif t > 0:
            command_letters += 'u'
        else:
            command_letters += 'd'
    return command_letters