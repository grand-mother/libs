# -*- coding: utf-8 -*-
"""
Encapsulation of the GULL C library

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


"""The OS specific name of the GULL library object"""
LIBNAME = "libgull.so"

"""The full path to the GULL library object"""
LIBPATH = os.path.join(LIBDIR, "libgull.so")

"""The git hash of the library"""
LIBHASH = "91ed20fc52c35a8ae9d32416dd7d0249100aad6f"
