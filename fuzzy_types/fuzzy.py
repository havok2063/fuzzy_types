# !/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Filename: structs.py
# Project: fuzzy_types
# Author: Brian Cherinka
# Created: Tuesday, 7th April 2020 2:15:25 pm
# License: BSD 3-clause "New" or "Revised" License
# Copyright (c) 2020 Brian Cherinka
# Last Modified: Friday, 10th April 2020 6:56:21 pm
# Modified By: Brian Cherinka


from __future__ import print_function, division, absolute_import
from collections import OrderedDict

import abc
import six
from fuzzy_types.utils import get_best_fuzzy

__all__ = ['FuzzyList', 'FuzzyDict', 'FuzzyOrderedDict', 'FuzzyStr']


class FuzzyBase(abc.ABC):
    _base = None

    def __init__(self, the_items, use_fuzzy=None, dottable=True):
        self.use_fuzzy = use_fuzzy or get_best_fuzzy
        self._dottable = dottable
        self._base.__init__(self, the_items)

    def __getattr__(self, value):
        if self._dottable is False:
            raise AttributeError(f"'{self._base.__name__}' object has no attribute '{value}'")

        if '__' in value:
            return super(FuzzyBase, self).__getattr__(value)
        return self.__getitem__(value)

    @abc.abstractmethod
    def __getitem__(self, value):
        pass

    @abc.abstractmethod
    def __dir__(self):
        members = object.__dir__(self)
        return members

    @staticmethod
    def mapper(item):
        return str(item)

    @abc.abstractproperty
    def choices(self):
        pass

    def __contains__(self, value):
        if not isinstance(value, six.string_types):
            return super(FuzzyBase, self).__contains__(value)

        try:
            best = self.use_fuzzy(value, self.choices)
        except ValueError:
            best = None

        return best in self.choices

    def copy(self):
        if self._base == OrderedDict:
            kopied = dict(self)
        else:
            kopied = self._base.copy(self)
        return self.__class__(kopied, use_fuzzy=self.use_fuzzy, dottable=self._dottable)

    def to_original(self):
        ''' Convert fuzzy object back to original Python datatype '''
        return self._base(self)


class FuzzyBaseDict(FuzzyBase):

    def __init__(self, the_dict, use_fuzzy=None, dottable=True):
        super(FuzzyBaseDict, self).__init__(the_dict, use_fuzzy=use_fuzzy, dottable=dottable)
        # in case a value is another dictionary; also make it fuzzy
        for key, val in the_dict.items():
            if isinstance(val, dict):
                self[key] = self.__class__(val)

    def __getitem__(self, value):
        if not isinstance(value, six.string_types):
            return self.get(value)

        best = self.use_fuzzy(value, self.choices)
        return self._base.__getitem__(self, best)

    def __dir__(self):
        members = super(FuzzyBaseDict, self).__dir__()
        if self._dottable is True:
            members.extend(self.choices)
        return members

    @property
    def choices(self):
        return [self.mapper(i) for i in self.keys() if isinstance(i, six.string_types)]


class FuzzyDict(FuzzyBaseDict, dict):
    ''' A dotable dictionary that uses fuzzywuzzy to select the key.

    Parameters:
        the_items (dict):
            A dictionary of items to make fuzzy
        use_fuzzy (func):
            The function used to perform the fuzzy-matching.
            Default is :func:`fuzzy_types.utils.get_best_fuzzy`.
        dottable (bool):
            If False, turns off dottable attributes.  Default is True.

    Returns:
        A python dictionary with fuzzy keys
    '''
    _base = dict


class FuzzyOrderedDict(FuzzyBaseDict, OrderedDict):
    ''' A dotable ordered dictionary that uses fuzzywuzzy to select the key.

    Parameters:
        the_items (dict):
            A dictionary of items to make fuzzy
        use_fuzzy (func):
            The function used to perform the fuzzy-matching.
            Default is :func:`fuzzy_types.utils.get_best_fuzzy`.
        dottable (bool):
            If False, turns off dottable attributes.  Default is True.

    Returns:
        A python ordered dictionary with fuzzy keys

    '''
    _base = OrderedDict


class FuzzyList(FuzzyBase, list):
    ''' A dottable python list that uses fuzzywuzzy to select a string item

    Parameters:
        the_items (list):
            A list of items to make fuzzy
        use_fuzzy (func):
            The function used to perform the fuzzy-matching.
            Default is :func:`fuzzy_types.utils.get_best_fuzzy`.
        dottable (bool):
            If False, turns off dottable attributes.  Default is True.

    Returns:
        A python list with fuzzy items

    '''
    _base = list

    @property
    def choices(self):
        return [self.mapper(item) for item in self if isinstance(item, six.string_types)]

    def __getitem__(self, value):
        if not isinstance(value, six.string_types):
            return list.__getitem__(self, value)

        best = self.use_fuzzy(value, self.choices)
        return self[self.choices.index(best)]

    def __dir__(self):
        members = super(FuzzyList, self).__dir__()
        if self._dottable is True:
            members.extend(self.choices)
        return members


class FuzzyStr(str):
    ''' A fuzzy string that uses fuzzywuzzy for equality checks

    Parameters:
        the_string (str):
            A string to make fuzzy
        use_fuzzy (func):
            The function used to perform the fuzzy-matching.
            Default is :func:`fuzzy_types.utils.get_best_fuzzy`.
    '''
    _base = str

    def __init__(self, the_string, use_fuzzy=None):
        self.use_fuzzy = use_fuzzy or get_best_fuzzy
        self._base.__init__(the_string)

    def __eq__(self, value):
        try:
            self.use_fuzzy(value, [self])
        except ValueError:
            return False
        else:
            return True
