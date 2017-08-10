from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import sys
import subprocess
import json

# import in-house packages
thisDir = os.path.dirname(os.path.realpath(__file__)).replace('\\','/')
sys.path.append(os.path.join(thisDir, 'user_data/scripts'))

import lazy

SYNC_SRC = thisDir
SYNC_DST = os.path.expanduser('~').replace('\\','/')
IGNORE = [ '.git', '.DS_Store', '.gitignore', 'setup.py', 'README.md', 'LICENSE', 'TODO' ]

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

def install():
    content = json.load(open('./install.json', 'r'))
    lazy.run(content, {'sync_src' : SYNC_SRC, 'sync_dst' : SYNC_DST, 'ignoreList' : ' '.join(IGNORE)})

print('+------------------------------------------+')
print('|            .dotfiles Setup               |')
print('+------------------------------------------+')
if (confirmUser()):
    install()
    print('\nSetup complete, please restart your shell for the applied changes to take effect.')
else:
    print('Installation canceled.')

