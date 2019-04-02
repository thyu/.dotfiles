from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

# TODO: better printout
# TODO: better prompt
# TODO: interactive
# TODO: bash-line

import os
import sys
import subprocess
import tempfile
import shutil

HOME_DIR = os.path.expanduser('~')
DOT_DIR = os.path.dirname(os.path.realpath(__file__)).replace('\\','/')
GIT = 'git'
LN = 'ln'

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

def makeDirectories(path):
    if not os.path.exists(path):
        os.makedirs(path)

def removePath(path):
    if os.path.exists(path):
        if os.path.islink(path):
            os.unlink(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)

def github(path = ''):
    return os.path.join('https://github.com/' + path)

def dotPath(name = ''):
    return os.path.join(DOT_DIR, name)

def pkgPath(name = ''):
    return dotPath(os.path.join('data/packages', name))

def homePath(name = ''):
    return os.path.join(HOME_DIR, name)

def vimPath(name = ''):
    return dotPath(os.path.join('vim', name))

def syncFolder(srcDir, dstDir, blacklist = []):
    print('Updating from {} to {}'.format(srcDir, dstDir))
    # compute sync paths
    syncPaths = []
    for root, dirs, files in os.walk(srcDir, topdown=True):
        for name in files:
            srcFileFullPath = os.path.join(root, name)
            relativePath = os.path.relpath(srcFileFullPath, srcDir)
            if all([x not in srcFileFullPath for x in blacklist]):
                syncPaths.append(relativePath)
    print('Copying file to {}: '.format(dstDir), end = '')
    for p in syncPaths:
        pSrcFile = os.path.join(srcDir, p)
        pDstFile = os.path.join(dstDir, p)
        pDstDir = os.path.dirname(pDstFile);
        if not os.path.exists(pDstDir):
            makeDirectories(pDstDir)
        shutil.copy2(pSrcFile, pDstFile)
        print('*', end = '')
    print()

def runCommand(args = [], cwd = None, verbose = False, check = True):
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
    print('Run command {}'.format(' '.join(args)))
    process = subprocess.Popen(args, **kwargs)
    poutput = process.communicate()
    if check and process.returncode != 0:
        print('Command failed due to the following error:\n{}'.format(poutput[1]))
    return process.returncode

def isGitInstalled():
    return True

def isGitRepository(path):
    return runCommand([GIT,'-C', path, 'rev-parse'], check = False) == 0

def updateGit(path, originURL = None):
    if (isGitRepository(path)):
        runCommand([GIT,'-C', path, 'fetch', 'origin', 'master', 'master'])
        runCommand([GIT,'-C', path, 'checkout', 'master'])
        runCommand([GIT,'-C', path, 'rebase', 'origin/master'])
    else:
        if not originURL:
            print('Origin URL is not provided, skipping git pull')
            return
        if os.path.exists(path):
            print('Path {} already exists, skipping git clone')
        makeDirectories(path)
        runCommand([GIT,'-C', path, 'init'])
        runCommand([GIT,'-C', path, 'remote', 'add', 'origin', originURL])
        runCommand([GIT,'-C', path, 'fetch', 'origin', 'master', 'master'])
        runCommand([GIT,'-C', path, 'checkout', 'master'])
        runCommand([GIT,'-C', path, 'rebase', 'origin/master'])

def bootstrap():
    defaultBlacklist = ['.git', 'README.md', 'LICENSE', '.gitignore', '.travis.yml']
    # booststrap vim: install pathogen
    updateGit(pkgPath('vim-pathogen'), github('tpope/vim-pathogen'))
    syncFolder(pkgPath('vim-pathogen/autoload'), vimPath('autoload'), defaultBlacklist)
    # colorschemes
    updateGit(pkgPath('vim-colorschemes'), github('flazz/vim-colorschemes.git'))
    syncFolder(pkgPath('vim-colorschemes/colors'), vimPath('colors'), defaultBlacklist)
    # vim airline
    updateGit(pkgPath('vim-airline'), github('vim-airline/vim-airline'))
    syncFolder(pkgPath('vim-airline'), vimPath('bundle/vim-airline'), defaultBlacklist)
    updateGit(pkgPath('vim-airline-themes'), github('vim-airline/vim-airline-themes'))
    syncFolder(pkgPath('vim-airline-themes'), vimPath('bundle/vim-airline-themes'), defaultBlacklist)
    # nerd tree
    updateGit(pkgPath('nerdtree'), github('scrooloose/nerdtree'))
    syncFolder(pkgPath('nerdtree'), vimPath('bundle/nerdtree'), defaultBlacklist)
    # fugitive
    updateGit(pkgPath('vim-fugitive'), github('tpope/vim-fugitive'))
    syncFolder(pkgPath('vim-fugitive'), vimPath('bundle/vim-fugitive'), defaultBlacklist)
    # TODO: indent
    # highlight
    updateGit(pkgPath('vim-cpp-enhanced-highlight'), github('octol/vim-cpp-enhanced-highlight'))
    syncFolder(pkgPath('vim-cpp-enhanced-highlight'), vimPath('bundle/syntax'), defaultBlacklist)
    # ctrlp
    updateGit(pkgPath('ctrlp.vim'), github('ctrlpvim/ctrlp.vim'))
    syncFolder(pkgPath('ctrlp.vim'), vimPath('bundle/ctrlp'), defaultBlacklist)
    # goyo + limelight
    updateGit(pkgPath('goyo.vim'), github('junegunn/goyo.vim'))
    syncFolder(pkgPath('goyo.vim'), vimPath('bundle/goyo.vim'), defaultBlacklist)
    updateGit(pkgPath('limelight.vim'), github('junegunn/limelight.vim'))
    syncFolder(pkgPath('limelight.vim'), vimPath('bundle/limelight'), defaultBlacklist)
    # trailing-whitespace
    updateGit(pkgPath('vim-trailing-whitespace'), github('bronson/vim-trailing-whitespace'))
    syncFolder(pkgPath('vim-trailing-whitespace'), vimPath('bundle/vim-trailing-whitespace'), defaultBlacklist)

def createLink(target, linkname):
    if not os.path.exists(target):
        raise Exception('[ERROR][createLink()] Target does not exist')
    removePath(linkname)
    print('Creating symbolic link:')
    print('{} -> {}'.format(target, linkname))
    runCommand([LN, '-s', target, linkname])

def updateResourceFile(tag, values, commentPrefix = '#'):
    pass

print('+------------------------------------------+')
print('|            .dotfiles Setup               |')
print('+------------------------------------------+')
if (confirmUser()):
    bootstrap()
    createLink(vimPath(), homePath('.vim'))
    createLink(dotPath('vimrc'), homePath('.vimrc'))
    createLink(dotPath('tmux.conf'), homePath('.tmux.conf'))
    print('Installation completed.')
else:
    print('Installation canceled.')
