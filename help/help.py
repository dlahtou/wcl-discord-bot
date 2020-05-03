from os import getcwd
from os.path import join

PARENT_HELP_FOLDER = 'help'

def help():
    filename = join(getcwd(), PARENT_HELP_FOLDER, 'help.txt')
    
    with open(filename) as open_file:
        text = open_file.read()
    
    return text