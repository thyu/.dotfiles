from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import sys

from . import constants

class OperatorId():
    __nextId__ = 0
    @staticmethod
    def getNextId():
        thisId = OperatorId.__nextId__ 
        OperatorId.__nextId__ += 1
        return thisId

class NodeId():
    __nextId__ = 0
    @staticmethod
    def getNextId():
        thisId = NodeId.__nextId__ 
        NodeId.__nextId__ += 1
        return thisId

def tidyPath(path, cwd):
    if os.path.isabs(path):
        return path
    else:
        return os.path.join(cwd, os.path.normpath(os.path.expanduser(path)))

# TODO: command runner class
def runCommand(args, verbose = False):
    import subprocess
    stdoutRedirection = subprocess.PIPE if not verbose else None
    stderrRedirection = subprocess.PIPE if not verbose else None
    kwargs = {
        'bufsize' : 0,                  # unbuffered
        'executable' : None,            # executable replacement, rarely used
        'stdin' : None,                 # stdin redirection
        'stdout' : stdoutRedirection,   # stdout redirection
        'stderr' : stderrRedirection,   # stderr redirection
        'cwd' : os.getcwd()             # use python's cwd
    }
    process = subprocess.Popen( args, **kwargs )
    poutput = process.communicate()
    return {'returncode' : process.returncode, 'stdout' : poutput[0], 'stderr' : poutput[1] }

def readStartupScript(startupScriptPath):
    startupScriptObj = {}
    startupScriptLines = [] 
    if os.path.exists(startupScriptPath):
        startupScriptLines = open(startupScriptPath, 'r').readlines()
        startupScriptLines = [line.strip() for line in startupScriptLines]
        currentSection = constants.GLOBAL_SECTION
        startupScriptObj[currentSection] = []
        for l in startupScriptLines:
            if l.startswith(constants.SECTION_MARKER):
                currentSection = l[len(constants.SECTION_MARKER):].strip()
                startupScriptObj[currentSection] = []
            elif l:
                startupScriptObj[currentSection].append(l)
            else:
                if currentSection == constants.GLOBAL_SECTION: # for __global__, also insert blank lines
                    startupScriptObj[currentSection].append(l)
                currentSection = constants.GLOBAL_SECTION
    return startupScriptObj

def writeStartupScript(startupScriptPath, startupScriptObj):
    with open(startupScriptPath, 'w') as f:
        if constants.GLOBAL_SECTION in startupScriptObj:
            if (len(startupScriptObj[constants.GLOBAL_SECTION]) > 0):
                f.write('\n'.join(startupScriptObj[constants.GLOBAL_SECTION]) + '\n')
        for sectionName in startupScriptObj:
            if sectionName != constants.GLOBAL_SECTION:
                f.write('{} {}\n'.format(constants.SECTION_MARKER, sectionName))
                f.write('\n'.join(startupScriptObj[sectionName]) + '\n\n')

def updateStartupScript(startupScriptPath, section, content):
    startupScriptObj = readStartupScript(startupScriptPath)
    startupScriptObj[section] = content
    writeStartupScript(startupScriptPath, startupScriptObj)
    return startupScriptObj

