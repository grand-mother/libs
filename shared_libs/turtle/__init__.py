# -*- coding: utf-8 -*-
"""
Encapsulation of the TURTLE C library

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
from .. import LIBDIR

__all__ = ["LIBNAME", "LIBPATH", "LIBHASH"]


"""The OS specific name of the TURTLE library object"""
LIBNAME = "libturtle.so"

"""The full path to the TURTLE library object"""
LIBPATH = os.path.join(LIBDIR, LIBNAME)

"""The git hash of the library"""
LIBHASH = "0e7da42989bddd56426280ed6c02cd256d0bec9b"
