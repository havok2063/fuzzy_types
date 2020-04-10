# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Filename: test_fuzzylist.py
# Project: tests
# Author: Brian Cherinka
# Created: Wednesday, 8th April 2020 4:24:11 pm
# License: BSD 3-clause "New" or "Revised" License
# Copyright (c) 2020 Brian Cherinka
# Last Modified: Friday, 10th April 2020 7:01:11 pm
# Modified By: Brian Cherinka


from __future__ import print_function, division, absolute_import
import pytest
from fuzzy_types.fuzzy import FuzzyList


real = ['apple', 'banana', 'orange', 'pear']
fuzzy = FuzzyList(real)


def assert_exact(dd):
    assert 'apple' in dd
    assert dd[0] == 'apple'
    assert dd[3] == 'pear'


def assert_fuzzy(dd, dottable=True):
    assert 'appl' in dd
    assert dd[0] == 'apple'
    assert dd['appl'] == 'apple'
    assert dd['paer'] == 'pear'
    assert dd['bannaa'] == 'banana'
    if dottable:
        assert hasattr(dd, 'orange')
        assert dd.orange == 'orange'
        assert 'orange' in dir(dd)
    else:
        assert 'orange' not in dir(dd)
        assert not hasattr(dd, 'orange')


class TestList(object):

    def test_real_list(self):
        assert_exact(real)
        assert not ('appl' in real)
        assert not hasattr(real, 'orange')

    def test_fuzzy_list(self):
        assert_exact(fuzzy)
        assert_fuzzy(fuzzy)

    def test_fuzzy_nodots(self):
        fuzzy = FuzzyList(real, dottable=False)
        assert_fuzzy(fuzzy, dottable=False)

    def test_copy(self):
        kopy = fuzzy.copy()
        assert isinstance(kopy, FuzzyList)

    def test_tooriginal(self):
        orig = fuzzy.to_original()
        assert isinstance(orig, list)


class TestListFails(object):

    @pytest.mark.parametrize('item', [('mandarin'), ('apple')], ids=['noitem', 'fuzzyitem'])
    def test_real_noitem(self, item):
        with pytest.raises(TypeError) as cm:
            real[item]
        assert cm.type == TypeError
        assert 'list indices must be integers or slices, not str' in str(cm.value)

    def test_fuzzy_noitem(self):
        with pytest.raises(ValueError) as cm:
            fuzzy['mandarin']
        assert cm.type == ValueError
        assert "Cannot find a good match for 'mandarin'. Your input value is too ambiguous." in str(
            cm.value)

    def test_tooshort(self):
        with pytest.raises(AssertionError) as cm:
            fuzzy['ba']
        assert cm.type == AssertionError
        assert 'Your fuzzy search value must be at least 3 characters long.' in str(cm.value)
