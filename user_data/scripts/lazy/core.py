from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import sys
import copy

from . import util
from . import op
from . import constants
from . import disp

class LazyNode(object):
    
    def __init__(self, env = {}):
        self.id = util.NodeId.getNextId()
        if not env:
            env = {}
        self.env = env
        if (constants.CWD not in self.env):
            # for better support in "modern" windows, replace \ with /
            self.env[constants.CWD] = os.path.expanduser(constants.DEFAULT_STARTING_CWD).replace('\\'.'/') 

    def __del__(self):
        disp.log(tags = ['Node {:03d}'.format(self.id)], 
                 txts = 'Task finished, cleaning up...')

    def parseCmd(self, cmd):
        import shlex
        buildList = {
            '#shell' : lambda args: op.ShellOp(args),
            '#gitupdate' : lambda args: op.GitupdateOp(args),
            '#cd' : lambda args: op.ChdirOp(args),
            'cd' : lambda args: op.ChdirOp(args),
            '#mkdir' : lambda args : op.MkdirOp(args),
            '#config' : lambda args : op.ConfigOp(args),
            '#sleep' : lambda args : op.SleepOp(args),
            '#set' : lambda args: op.SetOp(args),
            '#dirsync' : lambda args: op.DirSyncOp(args)
        }
        cmdArgs = shlex.split(cmd) 
        if not cmdArgs:
            return None
        if cmdArgs[0] in buildList:
            operator = buildList[cmdArgs[0]](cmdArgs[1:])
        else:
            operator = op.ShellOp(cmdArgs)
        return operator
   
    def runCommand(self, command):
        translatedCommand = command.format(**self.env)
        runOp = self.parseCmd(translatedCommand)
        if runOp:
            disp.log(tags = 'Node {:03d}'.format(self.id), 
                     txts = 'Run Cmd ' + runOp.__str__())
            runOp.run(self.env)
            op.SleepOp('0.2').run(self.env)

    def run(self, lazyScript):
        if isinstance(lazyScript, dict):
            for key in lazyScript:
                disp.log(tags = ['Node {:03d}'.format(self.id) ], 
                         txts = 'Entering section "{}"'.format(key))
                # TODO: run parallel?
                newState = copy.deepcopy(self.env)
                newNode = LazyNode(newState)
                newNode.run(lazyScript[key])
        elif isinstance(lazyScript, list):
            for command in lazyScript:
                if isinstance(command, (list, dict)):
                    newState = copy.deepcopy(self.env)
                    newNode = LazyNode(newState)
                    newNode.run(command)
                else:
                    self.runCommand(command)
        else:
            self.runCommand(lazyScript) # run a command

def run(lazyScript, env = {}):
    runner = LazyNode(env)
    runner.run(lazyScript)
