from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import sys
import subprocess
import tempfile
import shutil

THIS_DIR = os.path.dirname(os.path.realpath(__file__)).replace('\\','/')
SYNC_SRC = os.path.join(THIS_DIR, '.install')
SYNC_DST = os.path.realpath(os.path.expanduser('~').replace('\\','/'))
BLACKLIST = []

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

def syncFolder(srcDir, dstDir, blacklist):
    print('Updating from {} to {}'.format(srcDir, dstDir))
    # compute sync paths
    syncPaths = []
    for root, dirs, files in os.walk(srcDir, topdown=True):
        for name in files:
            srcFileFullPath = os.path.join(root, name)
            relativePath = os.path.relpath(srcFileFullPath, srcDir)
            if all([x not in srcFileFullPath for x in blacklist]):
                syncPaths.append(relativePath)
    for p in syncPaths:
        pSrcFile = os.path.join(srcDir, p)
        pDstFile = os.path.join(dstDir, p)
        pDstDir = os.path.dirname(pDstFile);
        if not os.path.exists(pDstDir):
            print('mkdir ' + pDstDir)
        print('Copying file \"{}\"'.format(p))

def runCommand(scriptPath, args = [], cwd = None, verbose = True, check = True):
    print('run script ' + scriptPath)
    args.insert(0, scriptPath)
    stdoutRedirection = subprocess.PIPE if not verbose else None
    stderrRedirection = subprocess.PIPE if not verbose else None
    if not cwd:
        cwd = os.getcwd()
    kwargs = {
        'bufsize' : 0,                  # unbuffered
        'executable' : None,            # executable replacement, rarely used
        'stdin' : None,                 # stdin redirection
        'stdout' : stdoutRedirection,   # stdout redirection
        'stderr' : stderrRedirection,   # stderr redirection
        'cwd' : cwd
    }
    process = subprocess.Popen(args, **kwargs)
    poutput = process.communicate()
    if check and process.returncode != 0:
        print('Command failed due to the following error:\n{}'.format(poutput[1]))
    return process.returncode

def isGitInstalled():
    return True

def isGitRepository(path):
    return runCommand(['git','-C', path, 'rev-parse']) == 0

def updateGit(path, originURL = None):
    if (isGitRepository(path)):
        runCommand(['git','-C', path, 'fetch', 'origin'])
        runCommand(['git','-C', path, 'checkout', 'master'])
        runCommand(['git','-C', path, 'rebase', 'origin/master'])
        runCommand(['git','-C', path, 'submodule', 'update'])
    else:
        if not originURL:
            print('Origin URL is not provided, skipping git pull')
            return
        if os.path.exists(path):
            print('Path {} already exists, skipping git clone')
        runCommand(['git','-C', path, 'init'])
        runCommand(['git','-C', path, 'remote', 'add', 'origin', originURL])
        runCommand(['git','-C', path, 'fetch', 'origin'])
        runCommand(['git','-C', path, 'checkout', 'master'])
        runCommand(['git','-C', path, 'rebase', 'origin/master'])
        runCommand(['git','-C', path, 'submodule', 'update', '--init'])

def updateResourceFile(tag, values, commentPrefix = '#'):
    pass

print('+------------------------------------------+')
print('|            .dotfiles Setup               |')
print('+------------------------------------------+')
if (confirmUser()):
    # syncFolder(SYNC_SRC, SYNC_DST, BLACKLIST)
    # runCommand(os.path.join(THIS_DIR, 'scripts/bootstrap/install_vim_plugins.sh'))
    # install pathogen
    tempdir = tempfile.mkdtemp()
    updateGit(os.path.join(tempdir, 'vim-pathogen'), 'https://github.com/tpope/vim-pathogen')
    shutil.rmtree(tempdir)
else:
    print('Installation canceled.')
