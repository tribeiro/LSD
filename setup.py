#! /usr/bin/python
# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.

from setuptools import setup, find_packages

import os
import sys

# read version.py file to get version and metadata information
here = os.path.abspath(os.path.dirname(__file__))
version_py = os.path.join(here, "src/lsd/core/version.py")
execfile(version_py)

# lsd scripts
lsd_scripts = ['src/scripts/lsd_fitcontinum.py'
               ]

# platform specific requirements
platform_deps = []

# go!
setup(
    name='lsd-python',
    version=_lsd_version_,
    description=_lsd_description_,
    long_description=open("docs/site/index.rst").read(),
    url=_lsd_url_,

    author=_lsd_author_,
    author_email=_lsd_author_email_,

    license=_lsd_license_,

    package_dir={"": "src"},
    packages=find_packages("src", exclude=["*.tests"]),

    include_package_data=True,

    scripts=lsd_scripts,

    # installation happens in the specified order
    install_requires=[
                         "numpy",
                         "astropy",
                         "astropysics",
                         "pymc",
                     ] + platform_deps,

    # tests_require = ["nose", "coverage", "wheel"],
)
