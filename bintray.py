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
import os
import urllib
import urllib2

__author__ = 'naitiz'

from HTMLParser import HTMLParser


class RecursiveParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.result = list()
        self.mark = False

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            self.mark = True

    def handle_data(self, data):
        if self.mark:
            self.result.insert(0, data)

    def handle_endtag(self, tag):
        if tag == 'a':
            self.mark = False


def fetch(target_path, url):
    req = urllib2.Request(url)
    resp = urllib2.urlopen(req)
    content_type = str(resp.headers['content-type'])
    if content_type.startswith("text/html"):
        html_parser = RecursiveParser()
        html_parser.feed(str((resp.read())))
        for p in html_parser.result:
            fetch(target_path, url + p)
    else:
        download(target_path, url)


def download(target_path, url):
    dirname = str(url).split("://")[1]
    filename = dirname[dirname.rindex('/') + 1:]
    dirname = dirname[dirname.index('/') + 1:dirname.rindex('/') + 1]
    dirname = target_path + os.path.sep + dirname
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    if not os.path.exists(dirname + filename):
        print "download >>>> ", dirname, filename
        urllib.urlretrieve(url, dirname + filename)
    else:
        print "skip >>>> ", dirname, filename


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Tool to fetch files from jcenter.bintray.com')
    parser.add_argument(
        '-d',
        dest='dir',
        action='store',
        default=os.path.curdir,
        help='target directory, current for default')
    parser.add_argument('src', nargs='?',
                        help='remote url path to fetch from, e.g. "http://jcenter.bintray.com/com/android/databinding/"')
    args = parser.parse_args()
    ourl = args.src
    if (ourl):
        fetch(args.dir, ourl)
    else:
        parser.print_help()
