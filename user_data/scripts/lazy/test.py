import os
import sys
import subprocess
import shlex

class op:
    def __init__(self, name):
        self.name = name
        pass
    def run():
        pass

class shellOp:
    def __init__(self, name):
        self.name = 'shellCommand'
        # do translation
    def run():
        pass

class opFactory():
    pass

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

def sourceConfigInProfile(rc, sourceLine):
    rcSectionHead = '#### Run .dotfilesrc (automatically generated, do not edit)'
    try:
        # search for generated secion
        # TODO: search substring instead of exact
        startIdx = rc.index(rcSectionHead)
        rc[startIdx + 1] = sourceLine
    except:
        # if not found, append section
        rc = rc + [rcSectionHead, sourceLine]
    return rc

def saveToRC(rc):
    with open(os.path.join(getHomeDir(), '.bashrc'), 'w') as f:
        f.write('\n'.join(rc))

def writeConfigFile(configLines):
    with open(os.path.join(getHomeDir(), 'user_data/.dotrc'), 'w') as f:
        f.write('\n'.join(configLines))

def installBashPowerline():

    root = os.path.join(getHomeDir(), '.dotfiles')
    
    commands = [
        'rm -rf ' + os.path.join(root, 'user_data/packages/bash-powerline/'),
        'git clone https://github.com/riobard/bash-powerline ' + os.path.join(root, 'user_data/packages/bash-powerline/')
    ]

    for command in commands:
        runCommand(command)

    # setup .dotfilesrc file
    rc = readShellRC()
    rc = sourceConfigInProfile(rc, 'source ~/user_data/.dotrc')
    saveToRC(rc)

    # write .dotfilesrc
    configLines = ['source ~/userdata/packages/bash-powerline/bash-powerline.sh']
    writeConfigFile(configLines)
