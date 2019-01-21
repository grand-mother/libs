# -*- coding: utf-8 -*-
"""
Unit tests for the shared_libs.tools module
"""

import os
import unittest
import sys

import shared_libs.tools
from shared_libs import LIBDIR


class ToolsTest(unittest.TestCase):
    """Unit tests for the tools module"""

    def test_meta(self):
        meta = shared_libs.tools.Meta("test-tools")
        meta["LIBHASH"] = "abcd"
        meta.update()
        del meta

        meta = shared_libs.tools.Meta("test-tools")
        self.assertEqual(meta["LIBHASH"], "abcd")
        os.remove(os.path.join(LIBDIR, ".test-tools.json"))


    def test_temporary(self):
        path = os.getcwd()
        with shared_libs.tools.Temporary(
            "https://github.com/grand-mother/shared-libs") as _:
            self.assertNotEqual(path, os.getcwd())
        self.assertEqual(path, os.getcwd())


    def test_installer(self):
        def run():
            return True

        Install = shared_libs.tools.Installer([run])


if __name__ == "__main__":
    unittest.main()
