# -*- coding: utf-8 -*-
"""
Python binding for the GULL library

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
from . import LIBPATH

__all__ = ["snapshot_create", "snapshot_destroy", "LibraryError"]


class LibraryError(Exception):
    """A GULL library error"""
    pass


"""Proxy for the GULL library"""
_lib = None
 

def _export():
    """Export the ctypes binding for the GULL library"""
    global _lib

    # Fetch the library handle
    _lib = ctypes.cdll.LoadLibrary(LIBPATH)

    # Export the library return codes
    r = ["RETURN_SUCCESS", "RETURN_DOMAIN_ERROR", "RETURN_FORMAT_ERROR",
         "RETURN_MEMORY_ERROR", "RETURN_MISSING_DATA", "RETURN_PATH_ERROR"]
    for i, attr in enumerate(r):
        globals()[attr] = i
    globals()["return_code"] = r

    # Prototype the library functions
    def Define(function, arguments=None, result=None, encapsulate=True):
        """Helper routine for configuring a library function"""
        f = getattr(_lib, "gull_" + function)
        if arguments:
            f.argtypes = arguments
        if result:
            f.restype = result
        if not encapsulate:
            globals()[function] = f
            return

        def encapsulated_library_function(*args):
            """Encapsulation of the library function with error check"""
            r = f(*args)
            if r != RETURN_SUCCESS:
                raise LibraryError(globals()["return_code"][r])
            else:
                return r

        globals()[function] = encapsulated_library_function

    # Export the snapshot functions
    Define("snapshot_create", arguments=(ctypes.POINTER(ctypes.c_void_p),
        ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int,
        ctypes.POINTER(ctypes.c_int)), result=ctypes.c_int)

    Define("snapshot_destroy", arguments=(
       ctypes.POINTER(ctypes.c_void_p),), encapsulate=False)


# Export the binding
_export()
