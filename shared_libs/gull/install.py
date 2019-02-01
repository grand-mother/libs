# -*- coding: utf-8 -*-
"""
Installer for the GULL library

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

import os
import shutil
import subprocess

from . import LIBHASH, LIBPATH
from .. import DATADIR, LIBDIR, SRCDIR
from ..tools import Meta, Temporary

__all__ = ["install"]


def install():
    """Install the GULL library to the top package location"""

    # Check for an existing install
    meta = Meta("gull")
    if meta["LIBHASH"] == LIBHASH:
        return

    def system(command):
        subprocess.run(command, check=True, shell=True)

    # Install the library with its vectorization binding
    with Temporary("https://github.com/niess/gull", LIBHASH) as _:
        # Extend the source with vectorization
        target = f"src/gull.c"
        system(f"cat {target} {SRCDIR}/gull.c > tmp.c")
        system(f"mv tmp.c {target}")

        # Build the library
        system("make")

        # Copy back the library
        if not os.path.exists(LIBDIR):
            os.makedirs(LIBDIR)
        src = os.path.join("lib", "libgull.so")
        shutil.copy(src, LIBPATH)

        # Copy the data files
        dstdir = os.path.join(DATADIR, "gull")
        if not os.path.exists(dstdir):
            os.makedirs(dstdir)
        for fname in ("IGRF12.COF", "WMM2015.COF"):
            dst = os.path.join(dstdir, fname)
            if not os.path.exists(dst):
                shutil.copy(os.path.join("share", "data", fname), dst)

    # Dump the meta data
    meta["LIBHASH"] = LIBHASH
    meta.update()
