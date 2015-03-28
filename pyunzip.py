#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Last modified: 2015 Mar 29 12:48:52 AM CST
#
# LICENSE:
#   Copyright (c) 2010 Tzeng, Yi-Feng
#
#   Permission is hereby granted, free of charge, to any person obtaining
#   a copy of this software and associated documentation files (the
#   "Software"), to deal in the Software without restriction, including
#   without limitation the rights to use, copy, modify, merge, publish,
#   distribute, sublicense, and/or sell copies of the Software, and to
#   permit persons to whom the Software is furnished to do so, subject to
#   the following conditions:
#
#   The above copyright notice and this permission notice shall be
#   included in all copies or substantial portions of the Software.
#
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#   EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#   MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
#   NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
#   LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
#   OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
#   WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""
   Extract zip tool.

   Due to default unzip in linux platfrom can not extract cp950, cp936 encoding etc.
"""

__version__ = "1.3"
__revision__ = '1.3.1'
__author__ = "Tzeng, Yi-Feng"
__authorcontact__ = "yftzeng@gmail.com"
__website__ = "http://antbsd.twbbs.org/"

import sys
import zipfile
import os
import getopt
import shutil

def usage():
    print """usage: unzip.py <zipfile> [[-e <encoding>] -p <password>]
    <zipfile> is the source zipfile to extract
    <encoding> is the encoding of zipfile
    <password> is the password of zipfile

    -h: help

    long options also work:
    --verbose
    --encoding
    --password

    :: encoding tips ::
    cp950 (Traditional Chinese)
    cp936 (Simplified Chinese)

    """

def main():
    shortargs = 'he:p:'
    longargs = ['help', 'encoding=', 'password=']

    if len(sys.argv) < 2:
        usage()
        sys.exit()

    try:
        if sys.argv[1].startswith('-'):
            opts, args = getopt.getopt(sys.argv[1:], shortargs, longargs)
            zipsource = ''.join(sys.argv[-1:])
        else:
            opts, args = getopt.getopt(sys.argv[2:], shortargs, longargs)
            zipsource = sys.argv[1]
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    encoding = 'cp950'
    password = None

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        if o in ("-e", "--encoding"):
            encoding = a
        if o in ("-p", "--password"):
            password = a

    if not os.path.isfile(zipsource):
        print "ERROR: (" + zipsource + ") file is not exist"
        sys.exit(2)

    try:
        f = zipfile.ZipFile(zipsource, 'r')
    except zipfile.BadZipfile:
        print "ERROR: File is broken zip or not a zip file"
        sys.exit(2)

    if password != None:
        f.setpassword(password)

    for fileinfo in f.infolist():
        try:
            filename = unicode(fileinfo.filename, encoding)
        except TypeError:
            filename = fileinfo.filename
        except:
            print "ERROR: unknown encoding (" + encoding + ")"
            sys.exit(2)

        if filename.endswith('/'):
            if not os.path.isdir(filename):
                os.makedirs(filename)
                print "Create : " + filename
        else:
            if os.path.dirname(filename) != '' and not os.path.exists(os.path.dirname(filename)):
                os.makedirs(os.path.dirname(filename))
            outputfile = open(filename, "wb")
            try:
                shutil.copyfileobj(f.open(fileinfo.filename), outputfile)
            except (zipfile.BadZipfile), e:
                # XXX: python extract zipfile encoding with cp936, will always raise BadZipfile except
                if encoding != 'cp936':
                    print e
            except:
                print "ERROR: File is encrypted, password required for extraction (-p, --password)"
                sys.exit(2)

            print "Extract: " + filename

if __name__ == '__main__': main()

