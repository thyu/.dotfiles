from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import sys
import time

from . import util
from . import constants
from . import disp

class Op(object):
    def __init__(self, typeName, args):
        self.type = typeName
        self.id = util.OperatorId.getNextId()
        if not isinstance(args, list):
            args = [args]
        self.args = args
    def __str__(self):
        return '{} (id = {}, args = [{}])'.format(self.type, self.id, ','.join(self.args))
    def run(self, env):
        raise Exception('Operator not implemented (base class Op)')

class SleepOp(Op):
    def __init__(self, args):
        super(SleepOp, self).__init__('Sleep', args)
    def run(self, env):
        if not self.args:
            raise Exception('SleepOp requires 1 arguments')
        try:
            time.sleep(float(self.args[0]))
        except:
            raise Exception('Invalid sleep duration')

class ShellOp(Op):
    def __init__(self, args):
        super(ShellOp, self).__init__('Shell', args)
    def run(self, env):
        util.runCommand(args)

class SetOp(Op):
    def __init__(self, args):
        super(SetOp, self).__init__('Set', args)
    def run(self, env):
        if len(self.args) < 2:
            raise Exception('SetOp requires 2 arguments')
        env[self.args[0]] = self.args[1]

class ChdirOp(Op):
    def __init__(self, args):
        super(ChdirOp, self).__init__('Chdir', args)
    def run(self, env):
        if not self.args or not self.args[0]:
            raise Exception('ChdirOp requires 1 arguments')
        newCwd = util.tidyPath(self.args[0], env[constants.CWD])
        env[constants.CWD] = newCwd

class MkdirOp(Op):
    def __init__(self, args):
        super(MkdirOp, self).__init__('Mkdir', args)
    def run(self, env):
        if not self.args:
            raise Exception('MkdirOp requires 1 arguments')
        path = util.tidyPath(self.args[0], env[constants.CWD])
        if not os.path.exists(path):
            os.makedirs(path)
        elif not os.path.isdir(path):
            raise Exception('Path {} exists, but it is not a directory'.format(path))

class ConfigOp(Op):
    def __init__(self, args):
        super(ConfigOp, self).__init__('Config', args)
    def run(self, env):
        if len(self.args) < 3:
            raise Exception('ConfigOp requires at least 3 arguments')
        configPath = util.tidyPath(self.args[0], env[constants.CWD])
        sectionName = self.args[1]
        configContent = self.args[2:]
        util.updateStartupScript(configPath, sectionName, configContent)

class GitcloneOp(Op):
    def __init__(self, args):
        super(GitcloneOp, self).__init__('Gitclone', args)
    def run(self, env):
        if (len(self.args) < 2):
            raise Exception('Invalid argument(s): clone origin URL and destination path are required')
        # get url and repo path 
        repoDir = util.tidyPath(self.args[0], env[constants.CWD])
        gitURL = self.args[1]
        MkdirOp(repoDir).run(env)    # if repo dir does not exist, create it
        dirIsRepo = util.runCommand(['git', '-C', repoDir, 'rev-parse'])['returncode'] == 0
        if not dirIsRepo:
            print(util.runCommand(['git', '-C', repoDir, 'init']))
            print(util.runCommand(['git', '-C', repoDir, 'remote', 'add', 'origin', gitURL]))
            print(util.runCommand(['git', '-C', repoDir, 'fetch', 'origin']))
            print(util.runCommand(['git', '-C', repoDir, 'checkout', 'master']))
            print(util.runCommand(['git', '-C', repoDir, 'rebase', 'origin/master']))
        else:
            print('Repo already exists in {}'.format(repoDir))

class GitupdateOp(Op):
    def __init__(self, args):
        super(GitupdateOp, self).__init__('Gitupdate', args)
    def run(self, env):
        # get repo dir and (optionally) git repo url
        gitURL = None
        if not self.args:
            raise Exception('Invalid arguments')
        repoDir = util.tidyPath(self.args[0], env[constants.CWD])
        gitURL = self.args[1] if len(self.args) > 1 else None
        # if repo dir exists, try update
        if os.path.exists(repoDir):
            dirIsRepo = util.runCommand(['git', '-C', repoDir, 'rev-parse'])['returncode'] == 0
            if (dirIsRepo):
                print(util.runCommand(['git', '-C', repoDir, 'checkout', 'master']))
                print(util.runCommand(['git', '-C', repoDir, 'fetch', 'origin']))
                print(util.runCommand(['git', '-C', repoDir, 'rebase', 'origin/master']))
        # if repo dir does not exist, try clone
        else: 
            GitcloneOp(self.args).run(env)

class DirSyncOp(Op):
    def __init__(self, args):
        super(DirSyncOp, self).__init__('DirSync', args)
    def _recursiveListDir(self, dirPath, ignore):
        filteredPaths = [p for p in os.listdir(dirPath) if not any(word in p for word in ignore)]
        fullFilteredPaths = [os.path.join(dirPath, p) for p in filteredPaths]
        dirPaths = [p for p in fullFilteredPaths if os.path.isdir(p)]
        filePaths = [p for p in fullFilteredPaths if not os.path.isdir(p)]
        for dirPath in dirPaths:
            filePaths = filePaths + self._recursiveListDir(dirPath, ignore)
        return filePaths
    def _relativeDstPaths(self, paths, srcRoot, dstRoot):
        rSrcPaths = [os.path.relpath(p, srcRoot) for p in paths]
        dstPaths = [os.path.join(dstRoot, p) for p in rSrcPaths]
        return dstPaths
    def _copyPaths(self, srcFilePaths, dstFilePaths):
        import shutil
        assert(len(srcFilePaths) == len(dstFilePaths))
        for i in range(0, len(srcFilePaths)):
            dstDir = os.path.dirname(dstFilePaths[i])
            if not os.path.exists(dstDir) or not os.path.isdir(dstDir):
                os.makedirs(dstDir, 0o711)
            disp.log(self.type, 'Sync file {:4d}/{:4d} {}'.format(i + 1, len(dstFilePaths), os.path.basename(dstFilePaths[i])), lineEnd = '\r')
            shutil.copy2(srcFilePaths[i], dstFilePaths[i])
        print('')
        disp.log(self.type, 'Finished copying {} files'.format(len(dstFilePaths)))
    def syncFolder(self, srcDir, dstDir, ignore):
        srcFilePaths =  self._recursiveListDir(srcDir, ignore)
        dstFilePaths = self._relativeDstPaths(srcFilePaths, srcDir, dstDir)
        self._copyPaths(srcFilePaths, dstFilePaths)
    def run(self, env):
        if len(self.args) < 2:
            raise Exception('DirSyncOp requires at least 2 arguments')
        fromDir = util.tidyPath(self.args[0], env[constants.CWD])
        toDir = util.tidyPath(self.args[1], env[constants.CWD])
        ignoreList = []
        if len(self.args) > 2:
            ignoreList = self.args[2:]
        self.syncFolder(fromDir, toDir, ignoreList)
