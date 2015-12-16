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

import os.path
import sys

__author__ = 'naitiz'


def parseRepo(repo):
    repo = repo.replace("://", "\t")
    repo = repo.replace("@", "\t")
    repo = repo.replace(":", "\t")
    repo = repo.replace("/", "\t")
    repo = repo.replace(".git", "")
    result = repo.split("\t")
    return os.path.sep.join(result[1:3]), result[3]


def cloneProject(repo):
    dirname, projectname = parseRepo(repo)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    full_path = dirname + os.path.sep + projectname
    if not os.path.exists(full_path):
        print("Cloning " + repo + " into " + os.getcwd() + os.path.sep + dirname)
        os.system("cd " + dirname + ";git clone " + repo + " --recursive")
    else:
        print("Pulling " + dirname + os.path.sep + projectname)
        os.system("cd " + dirname + os.path.sep + projectname + ";git pull")


def main(args=()):
    if len(args) == 2:
        workingpath = args[0]
    elif len(args) == 1:
        workingpath = "."
    else:
        print('args error \n\nusages: python gitc.py working_path path_to_repo')
        return
    repo = args[1]

    if not os.path.exists(workingpath):
        os.mkdir(workingpath)
    os.chdir(workingpath)
    cloneProject(repo)


if __name__ == '__main__':
    main(sys.argv[1:])
