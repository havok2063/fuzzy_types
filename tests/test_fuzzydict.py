# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Filename: test_fuzzydict.py
# Project: tests
# Author: Brian Cherinka
# Created: Wednesday, 8th April 2020 2:36:33 pm
# License: BSD 3-clause "New" or "Revised" License
# Copyright (c) 2020 Brian Cherinka
# Last Modified: Wednesday, 8th April 2020 3:39:41 pm
# Modified By: Brian Cherinka


from __future__ import print_function, division, absolute_import
import pytest
from fuzzy_utils.fuzzy import FuzzyDict, FuzzyOrderedDict


real = {'apple': 1, 'banana': 2, 'orange': 3, 'pear': 4}
fuzzy = FuzzyDict(real)
ordered = FuzzyOrderedDict(real)


def assert_exact(dd):
    assert 'apple' in dd
    assert dd['apple'] == 1
    assert dd['pear'] == 4


def assert_fuzzy(dd, dottable=True):
    assert 'appl' in dd
    assert dd['appl'] == 1
    assert dd['paer'] == 4
    assert dd['bannaa'] == 2
    assert hasattr(dd, 'orange')
    assert dd.orange == 3
    if dottable:
        assert 'orange' in dir(dd)
    else:
        assert 'orange' not in dir(dd)


class TestDict(object):
    
    def test_real_dict(self):
        assert_exact(real)
        assert not ('appl' in real)

    @pytest.mark.parametrize('dd', [(fuzzy), (ordered)], ids=['fuzzy', 'fuzzyord'])
    def test_fuzzy_dict(self, dd):
        assert_exact(dd)
        assert_fuzzy(dd)

    def test_fuzzy_nodots(self):
        fuzzy = FuzzyDict(real, dottable=False)
        assert_fuzzy(fuzzy, dottable=False)


class TestDictFails(object):
    
    @pytest.mark.parametrize('key', [('mandarin'), ('appl')], ids=['nokey', 'fuzzykey'])
    def test_real_nokey(self, key):
        with pytest.raises(KeyError) as cm:
            real[key]
        assert cm.type == KeyError
        
    def test_fuzzy_nokey(self):
        with pytest.raises(ValueError) as cm:
            fuzzy['mandarin']
        assert cm.type == ValueError
        assert "Cannot find a good match for 'mandarin'. Your input value is too ambiguous." in str(cm.value)
    
