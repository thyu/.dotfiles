import os
import sys

import util
import op

def parseLazyCommand(cmd):
    import shlex
    buildList = {
        '#shell' : lambda args: op.ShellOp(args),
        '#gitupdate' : lambda args: op.GitupdateOp(args),
        '#cd' : lambda args: op.ChdirOp(args),
        'cd' : lambda args: op.ChdirOp(args),
        '#mkdir' : lambda args : op.MkdirOp(args),
        '#config' : lambda args : op.ConfigOp(args),
        '#sleep' : lambda args : op.SleepOp(args)
    }
    args = shlex.split(cmd)
    if args[0] in buildList:
        operator = buildList[args[0]](args[1:])
    else:
        operator = op.ShellOp(args)
    return operator

# run lazy command recursively
def _run(config, vardict = {}):
    if isinstance(config, dict):
        for key in config:
            print('Entering section "{}"'.format(key))
            # TODO: run parallel?
            _run(config[key], vardict)   
    elif isinstance(config, list):
        for command in config:
            _run(command, vardict)
    else:
        print('RUN OPERATOR "{}"'.format(config))
        # replace vardict 
        parseLazyCommand(config).run()

def run(config):
    prevcwd = os.getcwd()
    op.ChdirOp(util.tidyPath('~'))
    _run(config)
    op.ChdirOp(prevcwd).run()
