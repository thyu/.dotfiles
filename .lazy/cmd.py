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
    rc = open(os.path.join(getHomeDir(), '.bashrc'), 'r').read()

def main():
    commands = [
        'rm -r -f -v .dotfiles', 
        'git clone https://www.github.com/thyu/.dotfiles'
    ]
    for command in commands:
        runCommand(command)
    readShellRC()

if __name__ == '__main__':
    main()
