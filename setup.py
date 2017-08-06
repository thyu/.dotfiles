from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import sys
import shutil
import subprocess
import time 

SYNC_SRC = '.'

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
            os.makedirs(dstDir, 0711)
        print('>>> Copying file [{:4d} / {:4d}] {:<64}' .format(i + 1, len(dstFilePaths), os.path.basename(dstFilePaths[i])), end = '\r')
        sys.stdout.flush()
        shutil.copy2(srcFilePaths[i], dstFilePaths[i])
    print()

def _runCommand(args):
    process = subprocess.Popen(args)
    return process.communicate()

def updateFromGit():
    print('>>> Fetching updates from git...')
    print(_runCommand(['git','fetch','origin']))
    print('>>> Checking out the latest master...')
    print(_runCommand(['git','checkout','master']))
    print('>>> Rebasing the lastest master...')
    print(_runCommand(['git','rebase','origin/master']))

def confirmUser():
    print('>>> WARNING: This may overwrite existing files in your home directory!')
    while True:
        answer = _input('>>> Are you sure (y/n)? ').lower()
        if (answer == 'y') or (answer == 'n'):
            break
        print('>>> Invalid input, please respond with "y" or "n"')
    return True if answer == 'y' else False

# TODO: use .lazy to setup instead of copy files
def install():
    pass

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
        updateFromGit()
        install()
        syncFolder(SYNC_SRC, SYNC_DST, IGNORE)

if __name__ == '__main__':
    main()
