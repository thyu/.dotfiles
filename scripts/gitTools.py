import os
import sys

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
