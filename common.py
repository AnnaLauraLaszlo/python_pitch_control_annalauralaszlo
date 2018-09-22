import control_functions


def create_command(tolerance):
    pass



def get_command(command, tolerance):
    command_options = ['uu', 'dd', 'nn', 'ud', 'du']
    if len(command) == 3:
        # convert command to string
        command_letters = ''
        for i in range(len(command) - 1):
            t = command[i + 1] - command[i]
            if abs(t) < tolerance:
                command_letters += 'n'
            elif t > 0:
                command_letters += 'u'
            else:
                command_letters += 'd'
            print(command_letters)
        if command_letters in command_options:
            if command_letters == 'uu':
                control_functions.press_key('w')
                # control_functions.open_website('https://www.facebook.com/')
            if command_letters == 'dd':
                control_functions.press_key('s')
                # control_functions.open_website('https://www.youtube.com/')
            if command_letters == 'ud':
                control_functions.press_key('d')
                # control_functions.press_key('HEllo world!!!')
            if command_letters == 'du':
                control_functions.press_key('a')
            if command_letters == 'nn':
                pass
            print(command_letters)
        command = []