#!/usr/bin/env python
"""
The goal filesystem tree printer in Python, made after
http://mama.indstate.edu/users/ice/tree/

Goals:

 - reusability
  - public domain license
  - simplicity
  - readability
   - deliver each feature with major version

Evolution:

 [ ] print tree from current directory
 [ ] process symlinks
   [ ] prevent recursive symlinks

Format specifics:

 - directory names end with /
 - drawing chars are in the ASCII range
 - no colors

Example:

    $ tree.py
    .
    |-- directory/
    |-- tree.py
    `-- README.md

Credits:

 anatoly techtonik <techtonik@gmail.com>

"""

__version__ = 'idea'
__license__ = 'Public Domain'
__author__  = 'anatoly techtonik <techtonik@gmail.com>'

import os

# [ ] move to function
# [ ] make a __main__

"""
os.walk can not be used, because it is hard to print
filenames that should go after dir is processed. The
easy solution is a recursion, but it will fail on
deep trees, so here is a custom algorithm that
transforms recursion into queue processing. Queue is
a list that is modied inplace inside of `for` cycle.

[ ] for every entry in sorted list of entries
  [x] print
  [ ] if directorylistdir it and add to queue at
      current position
  [ ] detect when a last element is processed
    [ ] last element
      [ ] depth decreases on next element
    [ ] change format of the entry

"""
# it is important to pass unicode string to list,
# otherwise international names will be mungled.

# but then there will be problem printing unicode
# to windows console =/

"""
Commenting and committing this as there is no time
for research - only for earning money. =/

Basically, there are four pathways to be explored:
1. os.walk   - seems to be dead end
2. recursive listdir()   - prone to stack overflow
3. non-recursive with state variables   - state
            tracking needs a food picture/overview
4. queues   - [data in, code, data out] - pipeline,
            command pattern, stackless, better name?

root = '.'
print(root)
depth = 1
stack = [root]
dlist = sorted(os.listdir(root))
for idx, entry in enumerate(dlist):
    isdir = os.path.isdir(entry)

    last = True
    # detect if dir is empty
    if isdir:
        path = os.path.join(stack)
        path = os.path.join(path, entry)
        contents = os.path.listdir(path)
        if contents:
            last = False
        


    line = '|   '*(depth-1) + '|-- '+ entry
    if 
    print()
        print(entry)
"""

"""
featurecreep

[ ] overridable print function
[ ] overridable sort order

canofworms

[ ] deal with windows encoding bugs
  [ ] filename encoding
  [ ] console printing

"""
