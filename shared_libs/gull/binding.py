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
import datetime

from . import LIBPATH
from .. import DATADIR
from ..tools import define


__all__ = ["LibraryError", "Snapshot", "strerror"]


def strerror(code):
    """Convert a GULL library return code to a string
    
    Parameters
    ----------
    code : int
        The function return code

    Returns
    -------
    str
        A string describing the error type
    """

    r = ["RETURN_SUCCESS", "RETURN_DOMAIN_ERROR", "RETURN_FORMAT_ERROR",
         "RETURN_MEMORY_ERROR", "RETURN_MISSING_DATA", "RETURN_PATH_ERROR"]
    return r[code]


class LibraryError(Exception):
    """A GULL library error"""

    def __init__(self, code):
        """Set a GULL library error

        Parameters
        ----------
        code : int
            The function return code
        """
        self.code = code
        message = f"A GULL library error occurred: {strerror(code)}"

        super().__init__(message)


_lib = ctypes.cdll.LoadLibrary(LIBPATH)
"""Proxy for the GULL library"""


@define (_lib.gull_snapshot_create,
         arguments = (ctypes.POINTER(ctypes.c_void_p), ctypes.c_char_p,
                      ctypes.c_int, ctypes.c_int, ctypes.c_int,
                      ctypes.POINTER(ctypes.c_int)),
         result = ctypes.c_int,
         exception = LibraryError)
def _snapshot_create(snapshot, path, day, month, year, line):
    """Create a new snapshot object"""
    pass


@define (_lib.gull_snapshot_destroy,
         arguments=(ctypes.POINTER(ctypes.c_void_p),))
def _snapshot_destroy(snapshot):
    """Destroy a snapshot object"""
    pass


@define (_lib.gull_snapshot_field,
         arguments = (ctypes.c_void_p, ctypes.c_double, ctypes.c_double,
                      ctypes.c_double, 3 * ctypes.c_double,
                      ctypes.POINTER(ctypes.c_void_p)),
         result = ctypes.c_int,
         exception = LibraryError)
def _snapshot_field(snapshot, latitude, longitude, altitude, field):
    """Get a magnetic field value from a snapshot"""
    pass


@define (_lib.gull_snapshot_info,
         arguments=(ctypes.c_void_p, ctypes.POINTER(ctypes.c_int),
                    ctypes.POINTER(ctypes.c_double),
                    ctypes.POINTER(ctypes.c_double)))
def _snapshot_info(snapshot):
    """Get some extra info about the snapshot data"""
    pass


class Snapshot:
    """Proxy for a GULL snapshot object"""

    def __init__(self, model="IGRF12", date="2019-01-01"):
        """Create a snapshot of the geo-magnetic field

        Parameters
        ----------
        model : str
            The geo-magnetic model to use (IGRF12, or WMM2015)
        date : str or datetime.date
            The day at which the snapshot is taken

        Raises
        ------
        LibraryError
            A GULL library error occured, e.g. if the model parameters are not
            valid
        """
        self._snapshot, self._model, self._date = None, None, None
        self._workspace = ctypes.c_void_p(0)

        # Create the snapshot object
        snapshot = ctypes.c_void_p(None)
        if isinstance(date, str):
            d = datetime.date.fromisoformat(date)
        else:
            d = date
        day, month, year = map(ctypes.c_int, (d.day, d.month, d.year))

        path = f"{DATADIR}/gull/{model}.COF".encode("ascii")
        line = ctypes.c_int()

        if (_snapshot_create(ctypes.byref(snapshot), path, day, month, year,
                             ctypes.byref(line)) != 0):
            return
        self._snapshot = snapshot
        self._model, self._date = model, d

        # Get the meta-data
        order = ctypes.c_int()
        altitude_min = ctypes.c_double()
        altitude_max = ctypes.c_double()
        _snapshot_info(self._snapshot, ctypes.byref(order),
                       ctypes.byref(altitude_min), ctypes.byref(altitude_max))
        self._order = order.value
        self._altitude = (altitude_min.value, altitude_max.value)


    def __del__(self):
        try:
            if self._snapshot is None:
                return
        except AttributeError:
            return

        _snapshot_destroy(ctypes.byref(self._snapshot))
        _snapshot_destroy(ctypes.byref(self._workspace))
        self._snapshot = None


    def __call__(self, latitude, longitude, altitude=0):
        """Get the magnetic field at a given Earth location"""
        field = (3 * ctypes.c_double)()
        if _snapshot_field(self._snapshot, latitude, longitude, altitude,
                           field, ctypes.byref(self._workspace)):
            return
        else:
            return [float(v) for v in field]


    @property
    def altitude(self):
        """The altitude range of the snapshot"""
        return self._altitude


    @property
    def date(self):
        """The date of the snapshot"""
        return self._date


    @property
    def model(self):
        """The world magnetic model"""
        return self._model


    @property
    def order(self):
        """The approximation order of the model"""
        return self._order
