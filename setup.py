# -*- coding: utf-8 -*-

from grand_pkg import setup_package


# The package version
MAJOR = 0
MINOR = 1
MICRO = 5


# Extra package meta data can be added here. For a full list of available
# classifiers, see:
#     https://pypi.org/pypi?%3Aaction=list_classifiers
EXTRA_CLASSIFIERS = (
    "Development Status :: 3 - Alpha",
)


if __name__ == "__main__":
    setup_package(
        # Framework arguments
        __file__, (MAJOR, MINOR, MICRO), EXTRA_CLASSIFIERS,

        # Vanilla setuptools.setup arguments can be added below,
        # e.g. `entry_points` for executables or `data_files`
        install_requires = ("numpy >= 1.16.0",),
        package_data = {"grand_libs": ["data/gull/*", "src/*",
                                       "src/turtle/*"]}
    )
