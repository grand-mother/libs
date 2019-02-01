# -*- coding: utf-8 -*-
"""
Encapsulation of the TURTLE library

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

import ctypes
import glob
import os
import shutil
import subprocess

from . import LIBDIR, SRCDIR
from .tools import Meta, Temporary

__all__ = ["LIBNAME", "LIBPATH", "LIBHASH", "install", "get"]


"""The OS specific name of the TURTLE library object"""
LIBNAME = "libturtle.so"

"""The full path to the TURTLE library object"""
LIBPATH = os.path.join(LIBDIR, "libturtle.so")

"""The git hash of the library"""
LIBHASH = "0e7da42989bddd56426280ed6c02cd256d0bec9b"


_lib = None


def get():
    """Get the ctypes handle for the TURTLE library"""
    global _lib

    if _lib is None:
        # Fetch the library handle
        _lib = ctypes.cdll.LoadLibrary(LIBPATH)
    return _lib


def install():
    """Install the TURTLE library to the GRAND software"""

    # Check for an existing install
    meta = Meta("turtle")
    if meta["LIBHASH"] == LIBHASH:
        return

    def system(command):
        subprocess.run(command, check=True, shell=True)

    # Install the library with its vectorization binding
    with Temporary("https://github.com/niess/turtle", LIBHASH) as _:
        # Extend the source with vectorization
        for path in glob.glob(f"{SRCDIR}/turtle/*.c"):
            target = f"src/turtle/{os.path.basename(path)}"
            system(f"cat {target} {path} > tmp.c")
            system(f"mv tmp.c {target}")

        # Build the library
        system("make")

        # Copy back the library
        if not os.path.exists(LIBDIR):
            os.makedirs(LIBDIR)
        src = os.path.join("lib", "libturtle.so")
        shutil.copy(src, LIBPATH)

    # Dump the meta data
    meta["LIBHASH"] = LIBHASH
    meta.update()
