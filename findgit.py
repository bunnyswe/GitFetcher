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
import commands
import os
import os.path

import gitc

def process(query_str):
    """ Entry point """
    rootdir = '/Users/naitiz/ScriptWorkspace'
    for parent, dirnames, filenames in os.walk(rootdir):  # 三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
        for filename in filenames:  # 输出文件夹信息
            if parent.endswith("/.git") and filename == "config":
                path_join = os.path.join(parent, filename)
                # print "the full name of the file is:" + path_join
                stat, value = commands.getstatusoutput(
                    'grep "%s" %s' % (query_str, path_join))
                if stat == 0 and value is not None:
                    value_split = value.split("\n")
                    for value in value_split:
                        repo = value.replace("url = ","").replace("\t","").strip()
                        workingpath = os.path.expanduser('~')
                        os.chdir(workingpath)
                        gitc.cloneProject(repo)



if __name__ == "__main__":
    # query_str = sys.argv[1]
    query_str = "url = "
    process(query_str)
