from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import sys
import shutil
import subprocess
import time 

# import in-house packages
thisDir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(thisDir, 'user_data/scripts'))

import lazy

SYNC_SRC = thisDir

SYNC_DST = os.path.expanduser('~')

IGNORE = [
        '.git', 
        '.DS_Store', 
        '.gitignore',
        'setup.py',
        'README.md',
        'LICENSE'
        ]

def _input(msg):
    return input(msg) if sys.version_info[0] >= 3 else raw_input(msg)

def _recursiveListDir(dirPath, ignore):
    filteredPaths = [p for p in os.listdir(dirPath) if not any(word in p for word in ignore)]
    fullFilteredPaths = [os.path.join(dirPath, p) for p in filteredPaths]
    dirPaths = [p for p in fullFilteredPaths if os.path.isdir(p)]
    filePaths = [p for p in fullFilteredPaths if not os.path.isdir(p)]
    for dirPath in dirPaths:
        filePaths = filePaths + _recursiveListDir(dirPath, ignore)
    return filePaths

def _relativeDstPaths(paths, srcRoot, dstRoot):
    rSrcPaths = [os.path.relpath(p, srcRoot) for p in paths]
    dstPaths = [os.path.join(dstRoot, p) for p in rSrcPaths]
    return dstPaths

def _copyPaths(srcFilePaths, dstFilePaths):
    assert(len(srcFilePaths) == len(dstFilePaths))
    for i in range(0, len(srcFilePaths)):
        dstDir = os.path.dirname(dstFilePaths[i])
        if not os.path.exists(dstDir) or not os.path.isdir(dstDir):
            os.makedirs(dstDir, 0o711)
        print('>>> Copying file [{:4d} / {:4d}] {:<64}' .format(i + 1, len(dstFilePaths), os.path.basename(dstFilePaths[i])), end = '\r')
        sys.stdout.flush()
        shutil.copy2(srcFilePaths[i], dstFilePaths[i])
    print()
    print('Finished copying {} files'.format(len(dstFilePaths)))

def confirmUser():
    print('>>> WARNING: This may overwrite existing files in your home directory!')
    while True:
        answer = _input('>>> Are you sure (y/n)? ').lower()
        if (answer == 'y') or (answer == 'n'):
            break
        print('>>> Invalid input, please respond with "y" or "n"')
    return True if answer == 'y' else False

def install():
    installation = [
        [
            '#mkdir ~/.dotfiles/',
            'cd ~/.dotfiles/',
            '#gitupdate .'
        ],
        {
            'bash-powerline' : [
                '#mkdir ~/.dotfiles/user_data/packages',
                'cd ~/.dotfiles/user_data/packages',
                '#gitupdate ~/.dotfiles/user_data/packages/bash-powerline https://github.com/riobard/bash-powerline',
                '#config ~/.dotfiles/user_data/.dotrc bash-powerline "source ~/user_data/packages/bash-powerline/bash-powerline.sh"'
            ],
            'config' : [
                '#config ~/.bashrc "dotfiles-autorun" "source ~/user_data/.dotrc"'
            ]
        }
    ]
    lazy.run(installation)

# TODO: keep backup?
def syncFolder(srcDir, dstDir, ignore):
    srcFilePaths =  _recursiveListDir(srcDir, ignore)
    dstFilePaths = _relativeDstPaths(srcFilePaths, srcDir, dstDir)
    _copyPaths(srcFilePaths, dstFilePaths)

def main():
    print('+------------------------------------------+')
    print('|            .dotfiles Setup               |')
    print('+------------------------------------------+')
    if (confirmUser()):
        install()
        syncFolder(SYNC_SRC, SYNC_DST, IGNORE)
        print('\nSetup complete, please restart your shell for the applied changes to take effect.')

if __name__ == '__main__':
    main()
