# !/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Filename: test_fuzzy.py
# Project: tests
# Author: Brian Cherinka
# Created: Friday, 17th April 2020 10:27:44 am
# License: BSD 3-clause "New" or "Revised" License
# Copyright (c) 2020 Brian Cherinka
# Last Modified: Friday, 17th April 2020 10:27:44 am
# Modified By: Brian Cherinka


from __future__ import print_function, division, absolute_import
from fuzzy_types.fuzzy import FuzzyStr

real = 'apple'
fuzzy = FuzzyStr(real)


def test_fuzzy_str_eq():
    assert 'appl' != real
    assert 'appl' == fuzzy
    assert 'chocolate' != fuzzy
