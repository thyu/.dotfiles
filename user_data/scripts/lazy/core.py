import os
import sys
import subprocess
import shlex
import time

def _nicePath(path):
    return os.path.normpath(os.path.expanduser(path))

class Op(object):
    def __init__(self, name, args):
        self.name = name
        if not isinstance(args, list):
            args = [args]
        self.args = args
    def run(self):
        print('RUN!')
        pass

class SleepOp(Op):
    def __init__(self, args):
        super(SleepOp, self).__init__('SleepOp', args)
    def __str__(self):
        return self.name + ' ' + ' '.join(self.args)
    def run(self):
        if not self.args:
            raise Exception('SleepOp requires 1 arguments')
        try:
            time.sleep(float(self.args[0]))
        except:
            raise Exception('Invalid sleep duration')

class ShellOp(Op):
    def __init__(self, args):
        super(ShellOp, self).__init__('ShellOp', args)
    def __str__(self):
        return self.name + ' ' + ' '.join(self.args)
    def run(self):
        pass

class ChdirOp(Op):
    def __init__(self, args):
        super(ChdirOp, self).__init__('ChdirOp', args)
    def __str__(self):
        return self.name + ' ' + ' '.join(self.args)
    def run(self):
        if not self.args or not self.args[0]:
            self.args = ['.']
        os.chdir(_nicePath(self.args[0]))

class MkdirOp(Op):
    def __init__(self, args):
        super(MkdirOp, self).__init__('MkdirOp', args)
    def __str__(self):
        return self.name + ' ' + ' '.join(self.args)
    def run(self):
        if not self.args:
            raise Exception('MkdirOp requires 1 arguments')
        path = _nicePath(self.args[0])
        if not os.path.exists(path):
            os.makedirs(path)
        elif not os.path.isdir(path):
            raise Exception('Path {} exists, but it is not a directory'.format(path))

class ConfigOp(Op):
    def __init__(self, args):
        super(ConfigOp, self).__init__('ConfigOp', args)
    def __str__(self):
        return self.name + ' ' + ' '.join(self.args)
    def run(self):
        if len(self.args) < 3:
            raise Exception('ConfigOp requires at least 3 arguments')
        configPath = _nicePath(self.args[0])
        sectionName = self.args[1]
        configContent = self.args[2:]
        updateStartupScript(configPath, sectionName, configContent)

class GitcloneOp(Op):
    def __init__(self, args):
        super(GitcloneOp, self).__init__('GitcloneOp', args)
    def __str__(self):
        return self.name + ' ' + ' '.join(self.args)
    def run(self):
        if (len(self.args) < 2):
            raise Exception('Invalid argument(s): clone origin URL and destination path are required')
        # get url and repo path 
        repodir = _nicePath(self.args[0])
        giturl = self.args[1]
        MkdirOp(repodir).run()    # if repo dir does not exist, create it
        prevcwd = os.getcwd()
        ChdirOp(repodir).run()
        dirIsRepo = runCommand(['git', 'rev-parse'])['returncode'] == 0
        if not dirIsRepo:
            print(runCommand(['git', 'init']))
            print(runCommand(['git', 'remote', 'add', 'origin', giturl]))
            print(runCommand(['git', 'checkout', 'master']))
            print(runCommand(['git', 'fetch', 'origin']))
            print(runCommand(['git', 'rebase', 'origin/master']))
        else:
            print('Repo already exists in {}'.format(repodir))
        ChdirOp(prevcwd).run()

class GitupdateOp(Op):
    def __init__(self, args):
        super(GitupdateOp, self).__init__('GitupdateOp', args)
    def __str__(self):
        return self.name + ' ' + ' '.join(self.args)
    def run(self):
        # get repo dir and (optionally) git repo url
        giturl = None
        if not self.args:
            raise Exception('Invalid arguments')
        repodir = _nicePath(self.args[0])
        giturl = self.args[1] if len(self.args) > 1 else None
        # if repo dir exists, try update
        if os.path.exists(repodir):
            prevcwd = os.getcwd()
            ChdirOp(repodir).run()
            dirIsRepo = runCommand(['git', 'rev-parse'])['returncode'] == 0
            if (dirIsRepo):
                print(runCommand(['git', 'checkout', 'master']))
                print(runCommand(['git', 'fetch', 'origin']))
                print(runCommand(['git', 'rebase', 'origin/master']))
            ChdirOp(prevcwd).run()
        # if repo dir does not exist, try clone
        else: 
            GitcloneOp(self.args).run()

def parseLazyCommand(cmd):
    buildList = {
        '#shell' : lambda args: ShellOp(args),
        '#gitupdate' : lambda args: GitupdateOp(args),
        '#cd' : lambda args: ChdirOp(args),
        'cd' : lambda args: ChdirOp(args),
        '#mkdir' : lambda args : MkdirOp(args),
        '#config' : lambda args : ConfigOp(args),
        '#sleep' : lambda args : SleepOp(args)
    }
    args = shlex.split(cmd)
    if args[0] in buildList:
        op = buildList[args[0]](args[1:])
    else:
        op = ShellOp(args)
    return op

# TODO: command runner
def runCommand(args, verbose = False):
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

# run lazy command recursively
def runLazy(config):
    originalCwd = os.getcwd() # backup cwd
    if isinstance(config, dict):
        for key in config:
            print('Entering section "{}"'.format(key))
            runLazy(config[key])        # TODO: run parallel?
    elif isinstance(config, list):
        for command in config:
            runLazy(command)
    elif isinstance(config, str):
        print('RUN OPERATOR "{}"'.format(config))
        parseLazyCommand(config).run()
    os.chdir(originalCwd) # reset cwd

def readStartupScript(startupScriptPath):
    sectionMarker = '#>'
    globalSectionName = '__global__'
    startupScriptObj = {}
    startupScriptLines = [] 
    if os.path.exists(_nicePath(startupScriptPath)):
        startupScriptLines = open(_nicePath(startupScriptPath), 'r').readlines()
    startupScriptLines = [line.strip() for line in startupScriptLines if len(line.strip()) > 0]
    currentSection = globalSectionName
    startupScriptObj[currentSection] = []
    for l in startupScriptLines:
        if l.startswith(sectionMarker):
            currentSection = l[len(sectionMarker):].strip()
            startupScriptObj[currentSection] = []
        else:
            startupScriptObj[currentSection].append(l)
    return startupScriptObj

def writeStartupScript(startupScriptPath, startupScriptObj):
    sectionMarker = '#>'
    globalSectionName = '__global__'
    with open(_nicePath(startupScriptPath), 'w') as f:
        if globalSectionName in startupScriptObj:
            if (len(startupScriptObj[globalSectionName]) > 0):
                f.write('\n'.join(startupScriptObj[globalSectionName]) + '\n\n')
        for sectionName in startupScriptObj:
            if sectionName != globalSectionName:
                f.write('{} {}\n'.format(sectionMarker, sectionName))
                f.write('\n'.join(startupScriptObj[sectionName]) + '\n\n')

def updateStartupScript(startupScriptPath, section, content):
    startupScriptObj = readStartupScript(startupScriptPath)
    startupScriptObj[section] = content
    writeStartupScript(startupScriptPath, startupScriptObj)
    return startupScriptObj

def installBashPowerline():
    installation = [
        '#mkdir ~/.dotfiles/user_data/packages',
        '#sleep 2.0',
        'cd ~/.dotfiles/user_data/packages',
        '#gitupdate ~/.dotfiles/user_data/packages/bash-powerline https://github.com/riobard/bash-powerline',
        '#config ~/.dotfiles/user_data/.dotrc bash-powerline "source ~/user_data/packages/bash-powerline/bash-powerline.sh"'
    ]
    runLazy(installation)

"""
def main():
    test = {
        'commands' : [
            'cd ~/work',
            '#gitupdate https://github.com/thyu/.dotfiles .dotfiles_test'
        ]
    }
    runLazy(test)

if __name__ == '__main__':
    main()
"""
