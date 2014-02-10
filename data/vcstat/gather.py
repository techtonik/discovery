#!/usr/bin/env python
#
# Gather revision statistics from version control system.
# The process is not optimized for speed or anything. It
# just uses command line tools and updates working copy
# from revision to revision..
# 
# 1. Get a fresh clone / checkout
# 2. Run gather.py inside of it
#
#
# --- dataset 1: size ---
#
# - size of all files in revision
# - number of files
# - number of dirs
#
#
# status
#
# [ ] subversion traversing
#   [x] getting list of all revisions
#   [ ] processing one revision at a time
#     [ ] update copy to revision
#     [x] stop on error
#     [ ] save progress
#     [ ] rollback bad revision data
#     [ ] ...
#
# [ ] mercurial traversing
#   [x] getting list of all revisions
#   [ ] processing one revision at a time
#     [x] update copy to revision
#     [x] stop on error
#     [ ] save progress
#     [ ] rollback bad revision data
#     [ ] ...

import copy
import os
import sys
import subprocess


SET1 = {
  'totalsize': 0,
  'dirsnum': 0, 
  'filesnum': 0,
}


def echo(msg):
  '''only for debug'''
  pass # print msg

def runout(cmd):
  return subprocess.check_output(cmd, shell=True)


class HG(object):

  def check_clean(self):
    """check that working copy is clean and can be
       successfully updated to any revision"""
    if len(runout('hg status')) != 0:
      return False
    else:
      return True

  def revlist(self):
    """get list of revisions from oldest to youngest"""
    output = runout('hg log --template "{rev}\\n"')
    rev = []
    for line in output.splitlines():
      rev.append(line)
    return reversed(rev)


class SVN(object):

  def check_clean(self):
    """check that working copy is clean and can be
       successfully updated to any revision"""
    if len(runout('svn status')) != 0:
      return False
    else:
      return True

  def revlist(self):
    """get list of revisions from oldest to youngest"""
    output = runout('svn info')
    lastrev = 0
    for line in output.splitlines():
      if line.startswith('Revision: '):
        lastrev = line.strip().split()[1]

    lastrev = int(lastrev)
    rev = range(lastrev + 1)
    return rev


def process(path, ignore=[]):
  """calculate SET1 directory stats for given path, skipping
     directories mentioned in ignore (e.g. '.hg', '.svn', ...)
  """

  # unicode is critical to for non-English local names on Windows
  path = unicode(path)

  s = copy.copy(SET1)
  s['totalsize'] = 0
  for root, dirs, files in os.walk(path):
    # filter directories
    for ig in ignore:
      if ig in dirs:
        dirs.remove(ig)

    for f in files:
      s['totalsize'] += os.path.getsize(os.path.join(root, f))
    s['filesnum'] += len(files)
    s['dirsnum'] += len(dirs)

  return s


if __name__ == '__main__':
  # detect version control type
  i = 0
  reptype = None
  for n in ['.svn', '.hg']:
    if os.path.isdir(n):
      i += 1
      reptype = n

  if i == 0:
    sys.exit('Error: Can\'t detect version control system')
  if i > 1:
    sys.exit('Error: Detected several version control systems')

  # get API to repository information
  if reptype == '.hg':
    repapi = HG()
    echo('HG selected')
  else:
    repapi = SVN()
    echo('SVN selected')


  # get clearance
  if not repapi.check_clean():
    sys.exit('Error: Working copy is not clean, can not continue')



  # CSV header 
  print "revision, size, dirs, files"
  for rev in repapi.revlist():
    runout('hg up -r %s' % rev)
    line = process('.', ignore=['.hg'])
    line['rev'] = rev
    #print line
    s = "{rev}, {totalsize}, {dirsnum}, {filesnum}\n".format(**line)
    sys.stdout.write(s)
    sys.stdout.flush()

