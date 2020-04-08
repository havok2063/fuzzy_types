# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Filename: __init__.py
# Project: fuzzy_types
# Author: Brian Cherinka
# Created: Tuesday, 7th April 2020 1:55:50 pm
# License: BSD 3-clause "New" or "Revised" License
# Copyright (c) 2020 Brian Cherinka
# Last Modified: Wednesday, 8th April 2020 6:11:43 pm
# Modified By: Brian Cherinka


from __future__ import print_function, division, absolute_import

from fuzzy_types.configuration import get_config, get_package_version

NAME = 'fuzzy_types'

config = get_config(NAME)

__version__ = get_package_version(path=__file__, package_name=NAME)
