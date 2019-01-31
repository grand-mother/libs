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
        self.assertNotEqual(gull._lib, None)


    def test_snapshot(self):
        snapshot = gull.Snapshot()
        self.assertNotEqual(snapshot._snapshot, None)
        self.assertEqual(snapshot.model, "IGRF12")
        d = snapshot.date
        self.assertEqual(d.year, 2019)
        self.assertEqual(d.month, 1)
        self.assertEqual(d.day, 1)
        self.assertEqual(snapshot.order, 13)
        self.assertEqual(snapshot.altitude[0], -1E+03)
        self.assertEqual(snapshot.altitude[1], 600E+03)
        del snapshot

        snapshot = gull.Snapshot("WMM2015", "2018-06-04")
        self.assertNotEqual(snapshot._snapshot, None)
        self.assertEqual(snapshot.model, "WMM2015")
        d = snapshot.date
        self.assertEqual(d.year, 2018)
        self.assertEqual(d.month, 6)
        self.assertEqual(d.day, 4)

        m = snapshot(45., 3.)
        # Magnetic field according to
        # http://geomag.nrcan.gc.ca/calc/mfcal-en.php
        self.assertAlmostEqual(m[0], 0, 6)
        self.assertAlmostEqual(m[1], 2.2983E-05, 6)
        self.assertAlmostEqual(m[2], -4.0852E-05, 6)


    def test_snapshot_error(self):
        with self.assertRaises(gull.LibraryError) as context:
            snapshot = gull.Snapshot("Unknown")

if __name__ == "__main__":
    unittest.main()
