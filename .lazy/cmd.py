import os
import sys
import subprocess
import shlex

# TODO: command runner
def runCommand(cmd, verbose = False):
    print('Running command "{}" ... '.format(cmd))
    args = shlex.split(cmd)
    stdoutRedirection = subprocess.PIPE if not verbose else None
    stderrRedirection = None
    kwargs = {
        'bufsize' : 0,                  # unbuffered
        'executable' : None,            # executable replacement, rarely used
        'stdin' : None,                 # stdin redirection
        'stdout' : stdoutRedirection,   # stdout redirection
        'stderr' : stderrRedirection    # stderr redirection
    }
    process = subprocess.Popen( args, **kwargs )
    return process.communicate()

def getHomeDir():
    return os.path.expanduser('~')

def readShellRC():
    rc = open(os.path.join(getHomeDir(), '.bashrc'), 'r').readlines()
    rc = [line.strip() for line in rc]
    return rc

def insertToRC(rc, lines):
    if (not isinstance(lines, list)):
        lines = [ lines ]
    _generatedStart = '#### << .LAZY GENERATED CONTENT BEGINS >> ####'
    _generatedEnd = '#### << .LAZY GENERATED CONTENT ENDS >> ####'
    try:
        # search for generated secion
        # TODO: search substring instead of exact
        startIds = rc.index(_generatedStart)
        endIdx = rc.index(_generatedEnd)
    except:
        # if not found, append section
        rc = rc + [_generatedStart, _generatedEnd]
        startIdx = len(rc) - 2
        endIdx = len(rc) - 1
    generatedRcLines = rc[startIdx + 1:endIdx]
    rc[startIdx + 1 : startIdx + 1] = lines
    print('\n'.join(generatedRcLines))
    return rc

def saveToRC(rc):
    with open(os.path.join(getHomeDir(), '.bashrc'), 'w') as f:
        f.write('\n'.join(rc))

def main():

    root = os.path.expanduser('~/.dotfiles')

    commands = [
        'rm -rf ' + os.path.join(root, '.scripts/bash-powerline'),
        'git clone https://github.com/riobard/bash-powerline ' + os.path.join(root, '.scripts/bash-powerline')
    ]

    for command in commands:
        runCommand(command)

    rc = readShellRC()
    rc = insertToRC(rc, '. ~/.scripts/bash-powerline/bash-powerline.sh')
    saveToRC(rc)

if __name__ == '__main__':
    main()
