#!/usr/bin/env python
# coding=utf-8
# Created by evertonstz
""" This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>. """

from setuptools import setup

with open("README.md", "r") as fh:
   long_description = fh.read()

setup(
    name='pynps',
    version='1.3.1',
    py_modules=['pynps'],
    license='GPL3',
    description = 'PyNPS is a Nopaystation client writen in python',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='evertonstz',
    url='https://github.com/evertonstz/pynps',
    keywords = ['nopaystation', 'pkg2zip', 'playstation', 'psv', 'psp', 'psx', 'psm'], 
    install_requires=[
        'prompt_toolkit',
        'sqlitedict',
    ],
    entry_points='''
        [console_scripts]
        pynps=pynps:main
    ''',
    classifiers=[
    'Development Status :: 5 - Production/Stable',      
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Programming Language :: Python :: 3.7',
  ],
)
