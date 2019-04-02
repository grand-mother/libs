# -*- coding: utf-8 -*-
"""
Utilities for encapsulating shared libraries

Copyright (C) 2018 The GRAND collaboration

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>
"""

import contextlib
import json
import os
import sys
import tempfile
from distutils.command.install import install
from grand_pkg import git
from . import LIBDIR

__all__ = ["Installer", "Meta", "Temporary"]


@contextlib.contextmanager
def Temporary(url, tag=None):
    """Temporary context for building a shared library"""
    path = os.getcwd()
    with tempfile.TemporaryDirectory(prefix="grand-") as tmpdir:
        try:
            # Clone the repo
            os.chdir(tmpdir)
            git(f"clone {url}")
            if tag is not None:
                git(f"checkout {tag}")
            os.chdir(os.path.basename(url))

            # Get the hash
            githash = git("rev-parse", "HEAD")

            # Yield back the context
            yield githash

        finally:
            os.chdir(path)


class Meta:
    """Encapsulation of library meta data"""

    def __init__(self, name):
        path = os.path.join(LIBDIR, f".{name}.json")
        self._path = path

        if os.path.exists(path):
            with open(path) as f:
                self._meta = json.load(f)
        else:
            self._meta = {}

    def __getitem__(self, k):
        try:
            return self._meta[k]
        except KeyError:
            return None

    def __setitem__(self, k, v):
        self._meta[k] = v

    def update(self):
        if not os.path.exists(LIBDIR):
            os.makedirs(LIBDIR)

        with open(self._path, "w") as f:
            json.dump(self._meta, f)


def Installer(installs):
    """Create an extended installer class"""

    class InstallWithLibs(install):
        # Extend the setuptools install command
        def run(self):
            super().run()
            for i in installs:
                i()

    return InstallWithLibs


def define(source, arguments=None, result=None, exception=None):
    """Decorator for defining wrapped library functions"""

    # Set the C prototype
    if arguments:
        source.argtypes = arguments
    if result:
        source.restype = result

    def decorator(function):
        # Return the (wrapped) function
        if exception is not None:
            def wrapped(*args):
                """Wrapper for library functions with error check"""
                r = source(*args)
                if r != 0:
                    raise exception(r)
                else:
                    return r

            return wrapped
        else:
            def wrapped(*args):
                """Wrapper for library functions without error check"""
                source(*args)

            return wrapped

    return decorator
