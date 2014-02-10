Version Contol Statistics
-------------------------
Gather data about source code evolution.

This was born from a need to locate large commits
in repository history when migrating SCons repository
from Subversion to Mercurial. Subversion uses central
server to store historical revisions, so it is not an
issue for it, but for systems where the full history
is on a local machine, committed binary files make
repository large and slow to clone.


Datasets
--------
[Set 1] Basic.

Includes information per `revision`:
 - size   - total size of all files in this revision
 - dirs   - how many dirs in revision
 - files  - how many files

See example in `dataset/SCons.SET1.csv`


[Set 2] Internals.

To optimize repostiory size, it is good to know how
well the revision is compressed. There can be a huge
increase in size of working copy, but small increase
in repository size. For what we need to measure the
repository size delta per revision.


Notes
-----
Why not SVNPlot?
- it is SVN only
- not a simple download and run script
- requires binary dependencies
- no docs about produced data format / DB structure
- two step process is not really needed
