Installing module without distutils.

The most minimal interface that an archive with
Python module should support is unpacking and
running:

    python setup.py install

This should place Python module into
`site-packages` directory, so that it should
became importable.

To find `site-packages` (Python 2.6+):

    import site
    target = site.USER_SITE

or 

    python -c "import site; print(site.USER_SITE)"

This dir may not exist, so need to make sure it
is created:

    import os
    try:
      os.makedirs(target)
    except OSError:
      if not os.path.isdir(target):
        raise

The algorithm:

  [ ] check 'install' is supplied
  [ ] get site-packages
  [ ] create if not exists
  [ ] copy module

Bonus points:

  [ ] record all operations in sqlite db
    created dir /home/techtonik/.local/lib
    created dir /home/techtonik/.local/lib/python2.7
    created dir /home/techtonik/.local/lib/python2.7/site-packages
    copied patch.py to /home/techtonik/.local/lib/python2.7/site-packages
  [ ] provide uninstall command
    find db in target site-packages
    look at transaction number for patch.py installation
    rollback commands

