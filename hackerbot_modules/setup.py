################################################################################
# Copyright (c) 2025 Hackerbot Industries LLC
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
#
# Created By: Allen Chien
# Created:    April 2025
# Updated:    2025.04.01
#
# This module contains the setup for the hackerbot_helper package.
#
# Special thanks to the following for their code contributions to this codebase:
# Allen Chien - https://github.com/AllenChienXXX
################################################################################


from setuptools import setup, find_packages

setup(
    name="hackerbot_helper",
    version="0.1",
    license="MIT",
    license_files=["LICENSE"],
    packages=find_packages(),
    install_requires=[
        "pyserial",
        "os",
        "json",
        "collections",
        "threading",
        "serial.tools.list_ports",
        "time",
        "logging",        
    ],

)
