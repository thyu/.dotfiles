import os
import sys
import subprocess
import shlex

def _nicePath(path):
    return os.path.normpath(os.path.expanduser(path))

class Op(object):
    def __init__(self, name):
        self.name = name
        pass
    def run(self):
        pass

class ShellOp(Op):
    def __init__(self, args):
        super(ShellOp, self).__init__('ShellOp')
        self.args = args
    def __str__(self):
        return self.name + ' ' + ' '.join(self.args)
    def run(self):
        pass

class ChdirOp(Op):
    def __init__(self, args):
        super(ChdirOp, self).__init__('ChdirOp')
        self.args = args
    def __str__(self):
        return self.name + ' ' + ' '.join(self.args)
    def run(self):
        if not self.args or not self.args[0]:
            self.args = ['.']
        os.chdir(_nicePath(self.args[0]))

class MkdirOp(Op):
    def __init__(self, args):
        super(MkdirOp, self).__init__('MkdirOp')
        self.args = args
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

class GitcloneOp(Op):
    def __init__(self, args):
        super(GitcloneOp, self).__init__('GitcloneOp')
        self.args = args
    def __str__(self):
        return self.name + ' ' + ' '.join(self.args)
    def run(self):
        if (len(self.args) < 2):
            raise Exception('Invalid argument(s): clone origin URL and destination path are required')
        # get url and repo path 
        repodir = _nicePath(self.args[0])
        giturl = self.args[1]
        MkdirOp([repodir]).run()    # if repo dir does not exist, create it
        prevcwd = os.getcwd()
        ChdirOp([repodir]).run()
        dirIsRepo = runCommand(['git', 'rev-parse'])['returncode'] == 0
        if not dirIsRepo:
            print(runCommand(['git', 'init']))
            print(runCommand(['git', 'remote', 'add', 'origin', giturl]))
            print(runCommand(['git', 'fetch', 'origin']))
            print(runCommand(['git', 'checkout', '-t', 'origin/master']))
        else:
            print('Repo already exists in {}'.format(repodir))
        ChdirOp([prevcwd]).run()

class GitupdateOp(Op):
    def __init__(self, args):
        super(GitupdateOp, self).__init__('GitupdateOp')
        self.args = args
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
            ChdirOp([repodir]).run()
            dirIsRepo = runCommand(['git', 'rev-parse'])['returncode'] == 0
            if (dirIsRepo):
                print(runCommand(['git', 'checkout', 'master']))
                print(runCommand(['git', 'fetch', 'origin']))
                print(runCommand(['git', 'checkout', '-t', 'origin/master']))
            ChdirOp([prevcwd]).run()
        # if repo dir does not exist, try clone
        else: 
            GitcloneOp(self.args).run()

def parseLazyCommand(cmd):
    buildList = {
        '#shell' : lambda args: ShellOp(args),
        '#gitupdate' : lambda args: GitupdateOp(args),
        '#cd' : lambda args: ChdirOp(args),
        'cd' : lambda args: ChdirOp(args),
        '#mkdir' : lambda args : MkdirOp(args)
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

def runLazy(config):
    originalCwd = os.getcwd() # backup cwd
    # startup
    if 'startup' in config:
        assert('path' in config['startup'])
        assert('section' in config['startup'])
        assert('config' in config['startup'])
        updateStartupScript(config['startup']['path'], config['startup']['section'], config['startup']['config'])
    # TODO: run parallel?
    for cmd in config['commands']:
        print('RUN OPERATOR "{}"'.format(cmd))
        parseLazyCommand(cmd).run()
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

def updateStartupScript(startupScriptPath, section, content):
    startupScriptObj = readStartupScript(startupScriptPath)
    startupScriptObj[section] = content
    writeStartupScript(startupScriptPath, startupScriptObj)
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

def installBashPowerline():
    installation = {
        'commands' : [
            '#mkdir ~/.dotfiles/user_data/packages',
            'cd ~/.dotfiles/user_data/packages',
            '#gitupdate ~/.dotfiles/user_data/packages/bash-powerline https://github.com/riobard/bash-powerline'
        ],
        'startup' : {
            'path' : '~/.dotfiles/user_data/.dotrc',
            'section' : 'bash-powerline',
            'config' : [ 
                'source ~/user_data/packages/bash-powerline/bash-powerline.sh'
            ]
        }
    }
    runLazy(installation)

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
