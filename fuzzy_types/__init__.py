# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Filename: __init__.py
# Project: fuzzy_types
# Author: Brian Cherinka
# Created: Tuesday, 7th April 2020 1:55:50 pm
# License: BSD 3-clause "New" or "Revised" License
# Copyright (c) 2020 Brian Cherinka
# Last Modified: Friday, 10th April 2020 4:46:59 pm
# Modified By: Brian Cherinka


from __future__ import print_function, division, absolute_import

from fuzzy_types.configuration import get_config

NAME = 'fuzzy_types'

config = get_config(NAME)

__version__ = '0.1.1'
