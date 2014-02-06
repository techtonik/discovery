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
#   [ ] getting list of all revisions
#   [ ] processing one revision at a time
#     [ ] update copy to revision
#       [ ] stop on error
#       [ ] save progress
#       [ ] rollback bad revision data
#       [ ] ...
#
# [ ] mercurial traversing
#   [x] getting list of all revisions
#   [ ] processing one revision at a time
#     [ ] update copy to revision
#       [ ] stop on error
#       [ ] save progress
#       [ ] rollback bad revision data
#       [ ] ...

import copy
import os
import subprocess


SET1 = {
  'totalsize': 0,
  'dirsnum': 0, 
  'filesnum': 0,
}


class HG(object):

  def revlist(self):
    """get list of revisions from oldest to youngest"""
    cmd = 'hg log --template "{rev}\\n"'
    output = subprocess.check_output(cmd, shell=True)
    rev = []
    for line in output.splitlines():
      rev.append(line)
    return reversed(rev)


def process():
  """calculate directory stats and return tree for saving"""
  s = copy.copy(SET1)
  s['totalsize'] = 0
  for root, dirs, files in os.walk('.'):
    for f in files:
      s['totalsize'] += os.path.getsize(os.path.join(root, f))
    s['filesnum'] += len(files)
    s['dirsnum'] += len(dirs)

  return s



# get API to repository information
repapi = HG()

for rev in repapi.revlist():
  pass#print rev

print process()