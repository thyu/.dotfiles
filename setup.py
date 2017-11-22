from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import sys
import subprocess
import json

THIS_DIR = os.path.dirname(os.path.realpath(__file__)).replace('\\','/')
SYNC_SRC = THIS_DIR
SYNC_DST = os.path.expanduser('~').replace('\\','/')
IGNORE = [ '.git', '.DS_Store', '.gitignore', 'setup.py', 'README.md', 'LICENSE', 'TODO']

def _input(msg):
    return input(msg) if sys.version_info[0] >= 3 else raw_input(msg)

def confirmUser():
    print('>>> WARNING: This may overwrite existing files in your home directory!')
    while True:
        answer = _input('>>> Are you sure (y/n)? ').lower()
        if (answer == 'y') or (answer == 'n'):
            break
        print('>>> Invalid input, please respond with "y" or "n"')
    return True if answer == 'y' else False

def setupDotfiles():
    pass

print('+------------------------------------------+')
print('|            .dotfiles Setup               |')
print('+------------------------------------------+')
if (confirmUser()):
    if (setupDotfiles()):
        print('\nSetup complete, please restart your shell for the applied changes to take effect.')
    else:
        print('\nSetup failed!')
else:
    print('Installation canceled.')
