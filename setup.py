from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import sys
import subprocess
import json

thisDir = os.path.dirname(os.path.realpath(__file__)).replace('\\','/')

# try to import LAZY (https://www.github.com/thyu/lazy)
sys.path.append(thisDir)
import lazy

SYNC_SRC = thisDir
SYNC_DST = os.path.expanduser('~').replace('\\','/')
IGNORE = [ '.git', '.DS_Store', '.gitignore', 'setup.py', 'README.md', 'LICENSE', 'TODO', 'install.json' ]

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

print('+------------------------------------------+')
print('|            .dotfiles Setup               |')
print('+------------------------------------------+')
if (confirmUser()):
    content = json.load(open(os.path.join(thisDir, 'install.json'), 'r'))
    lazy.run(content, sync_src =  SYNC_SRC, sync_dst = SYNC_DST, ignoreList = ' '.join(IGNORE))
    print('\nSetup complete, please restart your shell for the applied changes to take effect.')
else:
    print('Installation canceled.')
