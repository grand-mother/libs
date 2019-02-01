# -*- coding: utf-8 -*-
"""
Unit tests for the shared_libs.turtle module
"""

import os
import unittest

import shared_libs.turtle


class TurtleTest(unittest.TestCase):
    """Unit tests for the turtle module"""

    def test_init(self):
        self.assertEqual(shared_libs.turtle.LIBNAME, "libturtle.so")
        self.assertNotEqual(shared_libs.turtle.LIBHASH, None)

    def test_install(self):
        shared_libs.turtle.install()
        self.assertTrue(os.path.exists(shared_libs.turtle.LIBPATH))

    def test_load(self):
        lib = shared_libs.turtle.get()
        self.assertEqual(shared_libs.turtle.get(), lib)


if __name__ == "__main__":
    unittest.main()
