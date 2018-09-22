import control_functions


def create_command(command, tolerance):
    pass



def get_command(command_letters):
    print(command_letters)
    command_options = ['uu', 'dd', 'nn', 'ud', 'du', 'un', 'dn', 'nd', 'nu']
    if command_letters in command_options:
        if command_letters == 'uu':
            control_functions.press_key('up')
            # control_functions.open_website('https://www.facebook.com/')
        elif command_letters == 'dd':
            control_functions.press_key('down')
            # control_functions.open_website('https://www.youtube.com/')
        elif command_letters == 'ud':
            control_functions.press_key('right')
            # control_functions.press_key('HEllo world!!!')
        elif command_letters == 'du':
            control_functions.press_key('left')
        else:
            control_functions.press_key('not yet implemented')