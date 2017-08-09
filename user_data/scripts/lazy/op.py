import os
import sys

import util

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
        os.chdir(util.tidyPath(self.args[0]))
        print('after chdir' , os.getcwd())

class MkdirOp(Op):
    def __init__(self, args):
        super(MkdirOp, self).__init__('MkdirOp', args)
    def __str__(self):
        return self.name + ' ' + ' '.join(self.args)
    def run(self):
        if not self.args:
            raise Exception('MkdirOp requires 1 arguments')
        path = util.tidyPath(self.args[0])
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
        configPath = util.tidyPath(self.args[0])
        sectionName = self.args[1]
        configContent = self.args[2:]
        util.updateStartupScript(configPath, sectionName, configContent)

class GitcloneOp(Op):
    def __init__(self, args):
        super(GitcloneOp, self).__init__('GitcloneOp', args)
    def __str__(self):
        return self.name + ' ' + ' '.join(self.args)
    def run(self):
        if (len(self.args) < 2):
            raise Exception('Invalid argument(s): clone origin URL and destination path are required')
        # get url and repo path 
        repodir = util.tidyPath(self.args[0])
        giturl = self.args[1]
        MkdirOp(repodir).run()    # if repo dir does not exist, create it
        prevcwd = os.getcwd()
        ChdirOp(repodir).run()
        dirIsRepo = util.runCommand(['git', 'rev-parse'])['returncode'] == 0
        if not dirIsRepo:
            print(util.runCommand(['git', 'init']))
            print(util.runCommand(['git', 'remote', 'add', 'origin', giturl]))
            print(util.runCommand(['git', 'checkout', 'master']))
            print(util.runCommand(['git', 'fetch', 'origin']))
            print(util.runCommand(['git', 'rebase', 'origin/master']))
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
        repodir = util.tidyPath(self.args[0])
        giturl = self.args[1] if len(self.args) > 1 else None
        # if repo dir exists, try update
        if os.path.exists(repodir):
            prevcwd = os.getcwd()
            ChdirOp(repodir).run()
            dirIsRepo = util.runCommand(['git', 'rev-parse'])['returncode'] == 0
            if (dirIsRepo):
                print(util.runCommand(['git', 'checkout', 'master']))
                print(util.runCommand(['git', 'fetch', 'origin']))
                print(util.runCommand(['git', 'rebase', 'origin/master']))
            ChdirOp(prevcwd).run()
        # if repo dir does not exist, try clone
        else: 
            GitcloneOp(self.args).run()
