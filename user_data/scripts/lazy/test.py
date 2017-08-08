import os
import sys
import subprocess
import shlex

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
        print(self)
    def __str__(self):
        return self.name + ' ' + ' '.join(self.args)
    def run(self):
        pass

class GitupdateOp(Op):
    def __init__(self, args):
        super(GitupdateOp, self).__init__('GitupdateOp')
        self.args = args
        print(self)
    def __str__(self):
        return self.name + ' ' + ' '.join(self.args)
    def run(self):
        print(runCommand(['git','rev-parse']))

test = {
    'commands' : [
        'cd pkgdir',
        'x sadf asdf',
        '#gitupdate https://github.com/thyu/.dotfiles .'
    ]
}

InstallBashPowerline = {
    'variables' : {
        'pkgdir' : '~/.dotfiles/packages/',
        'giturl' : 'https://github.com/riobard/bash-powerline/'
    },
    'commands' : [
        'cd ${pkgdir}',
        'rm -rf ${powerlinedir}]',
        'git clone ${giturl}'
    ]
}

def parseCommand(cmd):
    buildList = {
        '#shell' : lambda args: ShellOp(args),
        '#gitupdate' : lambda args: GitupdateOp(args)
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
        'stderr' : stderrRedirection    # stderr redirection
    }
    process = subprocess.Popen( args, **kwargs )
    return process.returncode + process.communicate()

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
 
    pkgDir = os.path.join(root, 'user_data/packages/')
    oldDir = os.getcwd()
    if (not os.path.exists(pkgDir)):
        os.makedirs(pkgDir)
    os.chdir(pkgDir)
    commands = [
        'rm -rf ' + os.path.join(pkgDir, 'bash-powerline/'),
        'git clone https://github.com/riobard/bash-powerline'
    ]

    for command in commands:
        runCommand(shlex.split(command))

    os.chdir(oldDir)

    # setup .dotfilesrc file
    rc = readShellRC()
    rc = sourceConfigInProfile(rc, 'source ~/user_data/.dotrc')
    saveToRC(rc)

    # write .dotfilesrc
    configLines = ['source ~/user_data/packages/bash-powerline/bash-powerline.sh']
    writeConfigFile(configLines)

def main():
    ops = []
    for cmd in test['commands']:
        ops.append(parseCommand(cmd))
    for op in ops:
        op.run()

if __name__ == '__main__':
    main()
