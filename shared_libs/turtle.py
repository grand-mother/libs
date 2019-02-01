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

import ctypes
import glob
import os
import shutil
import subprocess

import numpy

from . import LIBDIR, SRCDIR
from .tools import Meta, Temporary, define


__all__ = ["LIBNAME", "LIBPATH", "LIBHASH", "LibraryError",
           "ecef_from_geodetic", "ecef_from_horizontal", "ecef_to_geodetic",
           "ecef_to_horizontal"]


LIBNAME = "libturtle.so"
"""The OS specific name of the TURTLE library object"""


LIBPATH = os.path.join(LIBDIR, LIBNAME)
"""The full path to the TURTLE library object"""


LIBHASH = "0e7da42989bddd56426280ed6c02cd256d0bec9b"
"""The git hash of the library"""


def _install():
    """Install the TURTLE library to the top package location"""

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


# Install the library on import, if needed
_install()


class LibraryError(Exception):
    """A TURTLE library error"""

    def __init__(self, code):
        """Set a TURTLE library error

        Parameters
        ----------
        code : int
            The function return code
        """
        self.code = code
        message = f"A TURTLE library error occurred: {strerror(code)}"

        super().__init__(message)


_lib = ctypes.cdll.LoadLibrary(LIBPATH)
"""Proxy for the TURTLE library"""


_CST_DBL_P = numpy.ctypeslib.ndpointer(float, flags="aligned, contiguous")
_DBL_P = numpy.ctypeslib.ndpointer(float,
    flags="aligned, contiguous, writeable")

@define (_lib.turtle_ecef_from_geodetic_v,
         arguments = (_CST_DBL_P, _CST_DBL_P, _CST_DBL_P, _DBL_P,
                      numpy.ctypeslib.c_intp))
def _ecef_from_geodetic(latitude, longitude, altitude, ecef, size):
    """Convert geodetic coordinates to ECEF ones"""
    pass

@define (_lib.turtle_ecef_from_horizontal_v,
         arguments = (_CST_DBL_P, _CST_DBL_P, _CST_DBL_P, _CST_DBL_P, _DBL_P,
                      numpy.ctypeslib.c_intp))
def _ecef_from_horizontal(
    latitude, longitude, azimuth, elevation, direction, size):
    """Convert horizontal coordinates to an ECEF direction"""
    pass

@define (_lib.turtle_ecef_to_geodetic_v,
         arguments = (_CST_DBL_P, _DBL_P, _DBL_P, _DBL_P,
                      numpy.ctypeslib.c_intp))
def _ecef_to_geodetic(ecef, latitude, longitude, altitude, size):
    """Convert ECEF coordinates to geodetic ones"""
    pass

@define (_lib.turtle_ecef_to_horizontal_v,
         arguments = (_CST_DBL_P, _CST_DBL_P, _CST_DBL_P, _DBL_P, _DBL_P,
                      numpy.ctypeslib.c_intp))
def _ecef_to_horizontal(
    latitude, longitude, direction, azimuth, elevation, size):
    """Convert an ECEF direction to horizontal coordinates"""
    pass


def _regularize(a):
    """Regularize an array (or float) input"""
    a = numpy.asanyarray(a)
    return numpy.require(a, float, ["CONTIGUOUS", "ALIGNED"])


def ecef_from_geodetic(latitude, longitude, altitude):
    """Convert geodetic coordinates to ECEF ones"""

    latitude, longitude, altitude = map(_regularize, (latitude, longitude,
                                                      altitude))
    if latitude.size != longitude.size:
        raise ValueError("latitude and longitude must have the same size")
    if latitude.size != altitude.size:
        raise ValueError("latitude and altitude must have the same size")

    if latitude.size == 1:
        ecef = numpy.zeros(3)
    else:
        ecef = numpy.zeros((latitude.size, 3))

    _ecef_from_geodetic(latitude, longitude, altitude, ecef, latitude.size)
    return ecef


def ecef_from_horizontal(latitude, longitude, azimuth, elevation):
    """Convert horizontal coordinates to an ECEF direction"""

    latitude, longitude, azimuth, elevation = map(_regularize,
        (latitude, longitude, azimuth, elevation))
    if latitude.size != longitude.size:
        raise ValueError("latitude and longitude must have the same size")
    if latitude.size != azimuth.size:
        raise ValueError("latitude and azimuth must have the same size")
    if latitude.size != elevation.size:
        raise ValueError("latitude and elevation must have the same size")

    if latitude.size == 1:
        direction = numpy.zeros(3)
    else:
        direction = numpy.zeros((latitude.size, 3))

    _ecef_from_horizontal(
        latitude, longitude, azimuth, elevation, direction, latitude.size)
    return direction


def ecef_to_geodetic(ecef):
    """Convert ECEF coordinates to geodetic ones"""

    ecef = _regularize(ecef)
    if (ecef.size < 3) or ((ecef.size % 3) != 0):
        raise ValueError("ecef coordinates must be n x 3")

    n = int(ecef.size / 3)
    if n == 1:
        set0 = lambda x:numpy.zeros(1)
        latitude, longitude, altitude = map(set0, range(3)) 
    else:
        set0 = lambda x: numpy.zeros(n)
        latitude, longitude, altitude = map(set0, range(3))

    _ecef_to_geodetic(ecef, latitude, longitude, altitude, latitude.size)

    if n == 1:
        return latitude[0], longitude[0], altitude[0]
    else:
        return latitude, longitude, altitude


def ecef_to_horizontal(latitude, longitude, direction):
    """Convert an ECEF direction to horizontal coordinates"""

    latitude, longitude, direction = map(_regularize, (latitude, longitude,
                                                       direction))
    if latitude.size != longitude.size:
        raise ValueError("latitude and longitude must have the same size")
    if (direction.size < 3) or ((direction.size % 3) != 0):
        raise ValueError("direction must be n x 3")
    n = int(direction.size / 3)
    if latitude.size != n:
        raise ValueError("latitude and direction must have consistent shapes")

    if n == 1:
        set0 = lambda x:numpy.zeros(1)
        azimuth, elevation = map(set0, range(2))
    else:
        set0 = lambda x: numpy.zeros(n)
        azimuth, elevation = map(set0, range(2))

    _ecef_to_horizontal(
        latitude, longitude, direction, azimuth, elevation, latitude.size)

    if n == 1:
        return azimuth[0], elevation[0]
    else:
        return azimuth, elevation
