# -*- coding: utf-8 -*-
"""
Unit tests for the shared_libs.turtle module
"""

import os
import unittest

import numpy

from shared_libs import *
from shared_libs.turtle import *
from shared_libs.turtle.install import *

install()
import shared_libs.turtle.binding as turtle


class TurtleTest(unittest.TestCase):
    """Unit tests for the turtle module"""

    def test_init(self):
        self.assertEqual(LIBNAME, "libturtle.so")
        self.assertNotEqual(LIBHASH, None)

    def test_install(self):
        self.assertTrue(os.path.exists(LIBPATH))


    def test_load(self):
        self.assertNotEqual(turtle._lib, None)

    def test_ecef(self):
        # Reference values
        ref = {
            "geodetic" : (45, 3, 1E+03),
            "ecef" : (4512105.81527233, 236469.44566852, 4488055.51564711),
            "horizontal" : (0, 90)}
        u = numpy.array(ref["ecef"])
        ref["direction"] = u / numpy.linalg.norm(u) # Assuming a spherical Earth

        # Check the ECEF to geodetic conversion
        ecef = turtle.ecef_from_geodetic(*ref["geodetic"])
        for i in range(3):
            self.assertAlmostEqual(ecef[i], ref["ecef"][i], 4)

        n = 10
        ecef = turtle.ecef_from_geodetic(n * (ref["geodetic"][0],),
            n * (ref["geodetic"][1],), n * (ref["geodetic"][2],))
        self.assertEqual(ecef.shape[0], n)
        self.assertEqual(ecef.shape[1], 3)
        for i in range(n):
            for j in range(3):
                self.assertAlmostEqual(ecef[i,j], ref["ecef"][j], 4)

        # Check the geodetic to ECEF conversion
        geodetic = turtle.ecef_to_geodetic(ref["ecef"])
        for i in range(3):
            self.assertAlmostEqual(geodetic[i], ref["geodetic"][i], 4)

        geodetic = turtle.ecef_to_geodetic(n * (ref["ecef"],))
        for i in range(3):
            self.assertEqual(geodetic[i].size, n) 
        for i in range(3):
            for j in range(10):
                self.assertAlmostEqual(geodetic[i][j], ref["geodetic"][i], 4)

        # Check the horizontal to ECEF conversion
        direction = turtle.ecef_from_horizontal(ref["geodetic"][0],
            ref["geodetic"][1], ref["horizontal"][0], ref["horizontal"][1])
        for i in range(3):
            self.assertAlmostEqual(direction[i], ref["direction"][i], 2)

        direction = turtle.ecef_from_horizontal(n * (ref["geodetic"][0],),
            n * (ref["geodetic"][1],), n * (ref["horizontal"][0],),
            n * (ref["horizontal"][1],))
        self.assertEqual(direction.shape[0], n)
        self.assertEqual(direction.shape[1], 3)
        for i in range(n):
            for j in range(3):
                self.assertAlmostEqual(direction[i,j], ref["direction"][j], 2)

        # Check the ECEF direction to horizontal conversion
        horizontal = turtle.ecef_to_horizontal(ref["geodetic"][0],
            ref["geodetic"][1], ref["direction"])
        self.assertAlmostEqual(horizontal[1], ref["horizontal"][1], 0)

        horizontal = turtle.ecef_to_horizontal(n * (ref["geodetic"][0],),
            n * (ref["geodetic"][1],), n * (ref["direction"],))
        for i in range(n):
            self.assertAlmostEqual(horizontal[1][i], ref["horizontal"][1], 0)


if __name__ == "__main__":
    unittest.main()
