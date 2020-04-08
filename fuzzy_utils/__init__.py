# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Filename: __init__.py
# Project: fuzzy_utils
# Author: Brian Cherinka
# Created: Tuesday, 7th April 2020 1:55:50 pm
# License: BSD 3-clause "New" or "Revised" License
# Copyright (c) 2020 Brian Cherinka
# Last Modified: Wednesday, 8th April 2020 5:02:13 pm
# Modified By: Brian Cherinka


from __future__ import print_function, division, absolute_import

from fuzzy_utils.configuration import get_config, get_package_version

NAME = 'fuzzy_utils'

config = get_config('fuzzy')

__version__ = get_package_version(path=__file__, package_name=NAME)
