# -*- coding: utf-8 -*-
"""
Unit tests for the shared_libs.version module
"""

import unittest
import sys

import shared_libs
from framework import git


class VersionTest(unittest.TestCase):
    """Unit tests for the version module"""

    def test_hash(self):
        githash = git("rev-parse", "HEAD")
        self.assertEqual(githash.strip(), shared_libs.version.__githash__)

    def test_version(self):
        self.assertIsNotNone(shared_libs.version.__version__)


if __name__ == "__main__":
    unittest.main()