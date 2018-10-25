import pyautogui, sys


pyautogui.size()
(1920, 1080)
pyautogui.position()
(187, 567)


print('Press Ctrl-C to quit.')
pyautogui.moveTo(100, 200, 2)
pyautogui
try:
    while True:
        x, y = pyautogui.position()
        positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
        print(positionStr, end='')
        print('\b' * len(positionStr), end='', flush=True)
except KeyboardInterrupt:
    print('\n')

