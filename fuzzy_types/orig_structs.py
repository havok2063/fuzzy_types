# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Filename: structs.py
# Project: fuzzy_types
# Author: Brian Cherinka
# Created: Tuesday, 7th April 2020 2:15:25 pm
# License: BSD 3-clause "New" or "Revised" License
# Copyright (c) 2020 Brian Cherinka
# Last Modified: Wednesday, 8th April 2020 5:48:32 pm
# Modified By: Brian Cherinka


from __future__ import print_function, division, absolute_import
from collections import OrderedDict

import six
import inspect
from fuzzy_types.utils import get_best_fuzzy


class Dotable(dict):
    """A custom dict class that allows dot access to nested dictionaries.

    Copied from http://hayd.github.io/2013/dotable-dictionaries/. Note that
    this allows you to use dots to get dictionary values, but not to set them.

    """

    def __getattr__(self, value):
        if '__' in value:
            return dict.__getattr__(self, value)
        else:
            return self.__getitem__(value)

    # def __init__(self, d):
    #     dict.__init__(self, ((k, self.parse(v)) for k, v in d.iteritems()))

    @classmethod
    def parse(cls, v):
        if isinstance(v, dict):
            return cls(v)
        elif isinstance(v, list):
            return [cls.parse(i) for i in v]
        else:
            return v


class DotableCaseInsensitive(Dotable):
    """Like dotable but access to attributes and keys is case insensitive."""

    def _match(self, list_of_keys, value):

        lower_values = [str(xx).lower() for xx in list_of_keys]
        if value.lower() in lower_values:
            return list_of_keys[lower_values.index(value.lower())]
        else:
            return False

    def __getattr__(self, value):
        if '__' in value:
            return super(DotableCaseInsensitive, self).__getattr__(value)
        return self.__getitem__(value)

    def __getitem__(self, value):
        key = self._match(list(self.keys()), value)
        if key is False:
            raise KeyError('{0} key or attribute not found'.format(value))
        return dict.__getitem__(self, key)


class FuzzyDict(OrderedDict):
    """A dotable dictionary that uses fuzzywuzzy to select the key."""

    def __getattr__(self, value):
        if '__' in value:
            return super(FuzzyDict, self).__getattr__(value)
        return self.__getitem__(value)

    def __getitem__(self, value):

        if not isinstance(value, six.string_types):
            return self.values()[value]

        if value in self.keys():
            return dict.__getitem__(self, value)

        best = get_best_fuzzy(value, self.keys())

        return dict.__getitem__(self, best)

    def __dir__(self):

        return list(self.keys())


class FuzzyList(list):
    """A list that uses fuzzywuzzy to select the item.
    Parameters:
        the_list (list):
            The list on which we will do fuzzy searching.
        use_fuzzy (function):
            A function that will be used to perform the fuzzy selection
    """

    def __init__(self, the_list, use_fuzzy=None):

        self.use_fuzzy = use_fuzzy if use_fuzzy else get_best_fuzzy

        list.__init__(self, the_list)

    def mapper(self, item):
        """The function that maps each item to the querable string."""

        return str(item)

    def __eq__(self, value):

        self_values = [self.mapper(item) for item in self]

        try:
            best = self.use_fuzzy(value, self_values)
        except ValueError:
            # Second pass, using underscores.
            best = self.use_fuzzy(value.replace(' ', '_'), self_values)

        return self[self_values.index(best)]

    def __contains__(self, value):

        if not isinstance(value, six.string_types):
            return super(FuzzyList, self).__contains__(value)

        try:
            self.__eq__(value)
            return True
        except ValueError:
            return False

    def __getitem__(self, value):

        if isinstance(value, six.string_types):
            return self == value
        else:
            return list.__getitem__(self, value)

    def __getattr__(self, value):

        self_values = [super(FuzzyList, self).__getattribute__('mapper')(item)
                       for item in self]

        if value in self_values:
            return self[value]

        return super(FuzzyList, self).__getattribute__(value)

    def __dir__(self):
        ''' override the dir to only show new methods and items in the list '''
        # get all original members of the FuzzyList
        #class_members = set(list(zip(*inspect.getmembers(self.__class__)))[0])
        # subtract out members from original list object
        #members = list(set(class_members) - set(dir(list)))
        members = super(FuzzyList, self).__dir__()
        # get parameters in list
        params = [self.mapper(item) for item in self]
        return members + params


class OrderedDefaultDict(FuzzyDict):

    def __init__(self, default_factory=None, *args, **kwargs):
        OrderedDict.__init__(self, *args, **kwargs)
        self.default_factory = default_factory

    def __missing__(self, key):
        result = self[key] = self.default_factory()
        return result
