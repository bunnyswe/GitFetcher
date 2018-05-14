#! /usr/bin/env python
# -*- coding: utf-8 *-*

'''
   Copyright 2015 Naitiz Zhang

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
'''
import argparse
import commands
import os.path

import pexpect

__author__ = 'naitiz'


def parseRepo(repo):
    repo = repo.replace("://", "\t")
    repo = repo.replace("@", "\t")
    repo = repo.replace(":", "\t")
    repo = repo.replace("/", "\t")
    repo = repo.replace(".git", "")
    result = repo.split("\t")
    return os.path.sep.join(result[1:-1]), result[-1]


def interact(cmd):
    a = commands.getoutput('echo $SHELL')
    shell = pexpect.spawn(a)
    shell.expect('$')
    shell.sendline(cmd)
    shell.interact()
    return shell


def cloneProject(repo, cdinto=True, workingpath=os.path.expanduser('~')):
    set_working_path(workingpath)
    dirname, projectname = parseRepo(repo)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    full_path = os.getcwd() + os.path.sep + dirname + os.path.sep + projectname
    if not os.path.exists(full_path):
        print("Cloning " + repo + " into " + full_path)
        os.system("cd " + dirname + ";git clone " + repo + " --recursive")
    else:
        print("Pulling " + full_path)
        os.system("cd " + full_path + ";git pull")
    if cdinto:
        interact('cd ' + full_path)


def set_working_path(workingpath):
    if not os.path.exists(workingpath):
        os.mkdir(workingpath)
    os.chdir(workingpath)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='faster clone from git, for lazy guys')
    parser.add_argument(
        '-d',
        dest='dir',
        action='store',
        default=os.path.expanduser('~'),
        help='target directory, "user home" for default')
    parser.add_argument('repo', nargs='?',
                        help='remote repo path to clone from, http(s) and git path both support, if local repo exists, git pull instead')
    parser.add_argument(
        '-n',
        dest='cdinto',
        action='store_false',
        help='cd into dir')
    args = parser.parse_args()
    workingpath = args.dir
    repo = args.repo
    cdinto = args.cdinto
    if (repo):
        cloneProject(repo, cdinto, workingpath)
    else:
        parser.print_help()
