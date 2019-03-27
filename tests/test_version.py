# -*- coding: utf-8 -*-
"""
Unit tests for the shared_libs.version module
"""

import unittest
import sys

import shared_libs
from framework import git


try:
    import shared_libs.version
except:
    # Skip version tests for non release builds
    pass
else:
    class VersionTest(unittest.TestCase):
        """Unit tests for the version module"""

        def test_hash(self):
            githash = git("rev-parse", "HEAD")
            self.assertEqual(githash.strip(), shared_libs.version.__git__["sha1"])

        def test_version(self):
            self.assertIsNotNone(shared_libs.version.__version__)


if __name__ == "__main__":
    unittest.main()
