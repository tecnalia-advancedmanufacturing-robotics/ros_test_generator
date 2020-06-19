# ! DO NOT MANUALLY INVOKE THIS setup.py, USE CATKIN INSTEAD
"""
@package ros_test_generator
@file setup.py
@author Anthony Remazeilles
@brief Standard ROS python package setup file

Copyright (C) 2020 Tecnalia Research and Innovation
Distributed under the Apache 2.0 license.
"""

from distutils.core import setup
from catkin_pkg.python_setup import generate_distutils_setup

# fetch values from package.xml
SETUP_ARGS = generate_distutils_setup(
    packages=['ros_test_generator'],
    package_dir={'': 'src'})

setup(**SETUP_ARGS)
