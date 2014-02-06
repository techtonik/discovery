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
# [ ] subversion traversing for single repository
#   [ ] getting list of all revisions
#   [ ] processing one revision at a time
#     [ ] update copy to revision
#       [ ] stop on error
#       [ ] save progress
#       [ ] rollback bad revision data
#       [ ] ...
#
