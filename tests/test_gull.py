# -*- coding: utf-8 -*-
"""
Unit tests for the shared_libs.gull module
"""

import ctypes
import os
import unittest
import sys

from shared_libs import *
from shared_libs.gull import *
from shared_libs.gull.install import *

install()
import shared_libs.gull.binding as gull


class GullTest(unittest.TestCase):
    """Unit tests for the gull sub-package"""

    def test_init(self):
        self.assertEqual(LIBNAME, "libgull.so")
        self.assertNotEqual(LIBHASH, None)


    def test_install(self):
        self.assertTrue(os.path.exists(LIBPATH))


    def test_load(self):
        self.assertEqual(gull.RETURN_SUCCESS, 0)


    def test_snapshot(self):
        snapshot = ctypes.c_void_p(None)
        path = ctypes.c_char_p(os.path.join(DATADIR, "gull",
            "IGRF12.COF").encode("ascii"))
        line = ctypes.c_int(0)
        r = gull.snapshot_create(ctypes.byref(snapshot), path, 1, 1, 2019,
            ctypes.byref(line))
        self.assertEqual(r, 0)
        self.assertNotEqual(snapshot.value, None)

        gull.snapshot_destroy(ctypes.byref(snapshot))
        self.assertEqual(snapshot.value, None)


    def test_snapshot_error(self):
        snapshot = ctypes.c_void_p(None)
        path = ctypes.c_char_p("unknown.COF".encode("ascii"))
        line = ctypes.c_int(0)
        try:
            r = gull.snapshot_create(ctypes.byref(snapshot), path, 1, 1, 2019,
                ctypes.byref(line))
        except Exception as e:
            self.assertEqual(str(e), gull.return_code[5])


if __name__ == "__main__":
    unittest.main()
