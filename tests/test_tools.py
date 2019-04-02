# -*- coding: utf-8 -*-
"""
Unit tests for the grand_libs.tools module
"""

import os
import unittest

import grand_libs.tools
from grand_libs import LIBDIR


class ToolsTest(unittest.TestCase):
    """Unit tests for the tools module"""

    def test_meta(self):
        meta = grand_libs.tools.Meta("test-tools")
        meta["LIBHASH"] = "abcd"
        meta.update()
        del meta

        meta = grand_libs.tools.Meta("test-tools")
        self.assertEqual(meta["LIBHASH"], "abcd")
        os.remove(os.path.join(LIBDIR, ".test-tools.json"))


    def test_temporary(self):
        path = os.getcwd()
        with grand_libs.tools.Temporary(
            "https://github.com/grand-mother/libs") as _:
            self.assertNotEqual(path, os.getcwd())
        self.assertEqual(path, os.getcwd())


    def test_installer(self):
        def run():
            return True

        Install = grand_libs.tools.Installer([run])


if __name__ == "__main__":
    unittest.main()
