import os
import sys

def tidyPath(path):
    if os.path.isabs(path):
        return path
    else:
        return os.path.normpath(os.path.expanduser(path))

# TODO: command runner class
def runCommand(args, verbose = False):
    import subprocess
    print('Running command "{}" ... '.format(' '.join(args)))
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
    sectionMarker = '#>'
    globalSectionName = '__global__'
    startupScriptObj = {}
    startupScriptLines = [] 
    if os.path.exists(tidyPath(startupScriptPath)):
        startupScriptLines = open(tidyPath(startupScriptPath), 'r').readlines()
        startupScriptLines = [line.strip() for line in startupScriptLines]
        currentSection = globalSectionName
        startupScriptObj[currentSection] = []
        for l in startupScriptLines:
            if l.startswith(sectionMarker):
                currentSection = l[len(sectionMarker):].strip()
                startupScriptObj[currentSection] = []
            elif l:
                startupScriptObj[currentSection].append(l)
            else:
                if currentSection == globalSectionName: # for __global__, also insert blank lines
                    startupScriptObj[currentSection].append(l)
                currentSection = globalSectionName
    return startupScriptObj

def writeStartupScript(startupScriptPath, startupScriptObj):
    sectionMarker = '#>'
    globalSectionName = '__global__'
    print(startupScriptObj)
    with open(tidyPath(startupScriptPath), 'w') as f:
        if globalSectionName in startupScriptObj:
            if (len(startupScriptObj[globalSectionName]) > 0):
                f.write('\n'.join(startupScriptObj[globalSectionName]) + '\n')
        for sectionName in startupScriptObj:
            if sectionName != globalSectionName:
                f.write('{} {}\n'.format(sectionMarker, sectionName))
                f.write('\n'.join(startupScriptObj[sectionName]) + '\n\n')

def updateStartupScript(startupScriptPath, section, content):
    startupScriptObj = readStartupScript(startupScriptPath)
    startupScriptObj[section] = content
    writeStartupScript(startupScriptPath, startupScriptObj)
    return startupScriptObj
