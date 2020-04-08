# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Filename: structs.py
# Project: fuzzy_utils
# Author: Brian Cherinka
# Created: Tuesday, 7th April 2020 2:15:25 pm
# License: BSD 3-clause "New" or "Revised" License
# Copyright (c) 2020 Brian Cherinka
# Last Modified: Wednesday, 8th April 2020 3:40:14 pm
# Modified By: Brian Cherinka


from __future__ import print_function, division, absolute_import
from collections import OrderedDict

import abc
import six
from fuzzy_utils.utils import get_best_fuzzy


class FuzzyBase(abc.ABC):

    def __init__(self, the_dict, use_fuzzy=None, dottable=True, base=None):
        self.use_fuzzy = use_fuzzy or get_best_fuzzy
        self._dottable = dottable
        self._base = base
        self._base.__init__(self, the_dict)

    @abc.abstractmethod
    def __getattr__(self, value):
        pass
    
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


class FuzzyBaseDict(FuzzyBase):
    def __getattr__(self, value):
        if '__' in value:
            return super(FuzzyBaseDict, self).__getattr__(value)
        return self.__getitem__(value)

    def __getitem__(self, value):

        if not isinstance(value, six.string_types):
            return self.values()[value]

        # if value in self.keys():
        #     return self._base.__getitem__(self, value)

        best = self.use_fuzzy(value, self.choices)

        return self._base.__getitem__(self, best)

    def __dir__(self):
        members = super(FuzzyBaseDict, self).__dir__()
        if self._dottable is True:
            members.extend([self.mapper(i) for i in self.keys()])
        return members

    @property
    def choices(self):
        return [self.mapper(i) for i in self.keys()]

    
class FuzzyDict(FuzzyBaseDict, dict):
    ''' A dotable dictionary that uses fuzzywuzzy to select the key. '''

    def __init__(self, the_dict, use_fuzzy=None, dottable=True):
        super(FuzzyDict, self).__init__(the_dict, use_fuzzy=use_fuzzy, dottable=dottable, base=dict)


class FuzzyOrderedDict(FuzzyBaseDict, OrderedDict):
    ''' A dotable ordered dictionary that uses fuzzywuzzy to select the key. '''

    def __init__(self, the_dict, use_fuzzy=None, dottable=True):
        super(FuzzyOrderedDict, self).__init__(
            the_dict, use_fuzzy=use_fuzzy, dottable=dottable, base=OrderedDict)


class FuzzyList(FuzzyBase, list):
    ''' A dottable python list that uses fuzzywuzzy to select a string item '''
    
    def __init__(self, the_list, use_fuzzy=None, dottable=True):
        super(FuzzyList, self).__init__(
            the_list, use_fuzzy=use_fuzzy, dottable=dottable, base=list)

    @property
    def choices(self):
        return [self.mapper(item) for item in self]
        
    @staticmethod
    def mapper(item):
        ''' The function that maps each item to the querable string. '''
        return str(item)

    def __getitem__(self, value):
        if not isinstance(value, six.string_types):
            return list.__getitem__(self, value)

        best = self.use_fuzzy(value, self.choices)
        return self[self.choices.index(best)]
    
    def __getattr__(self, value):

        self_values = [super(FuzzyList, self).__getattribute__('mapper')(item)
                       for item in self]

        if value in self_values:
            return self[value]

        return super(FuzzyList, self).__getattribute__(value)

    # def __getattr__(self, value):
    #     if '__' in value:
    #         return super(FuzzyBaseDict, self).__getattr__(value)
    #     return self.__getitem__(value)

    def __dir__(self):
        members = super(FuzzyList, self).__dir__()
        if self._dottable is True:
            members.extend([self.mapper(item) for item in self])
        return members

# class FuzzyList(list):
#     """A list that uses fuzzywuzzy to select the item.
#     Parameters:
#         the_list (list):
#             The list on which we will do fuzzy searching.
#         use_fuzzy (function):
#             A function that will be used to perform the fuzzy selection
#     """

#     def __init__(self, the_list, use_fuzzy=None):
#         self.use_fuzzy = use_fuzzy if use_fuzzy else get_best_fuzzy
#         list.__init__(self, the_list)

#     def mapper(self, item):
#         """The function that maps each item to the querable string."""
#         return str(item)

#     def __eq__(self, value):
#         self_values = [self.mapper(item) for item in self]

#         try:
#             best = self.use_fuzzy(value, self_values)
#         except ValueError:
#             # Second pass, using underscores.
#             best = self.use_fuzzy(value.replace(' ', '_'), self_values)

#         return self[self_values.index(best)]

#     def __contains__(self, value):
#         if not isinstance(value, six.string_types):
#             return super(FuzzyList, self).__contains__(value)

#         try:
#             self.__eq__(value)
#             return True
#         except ValueError:
#             return False

#     def __getitem__(self, value):

#         if isinstance(value, six.string_types):
#             return self == value
#         else:
#             return list.__getitem__(self, value)

#     def __getattr__(self, value):

#         self_values = [super(FuzzyList, self).__getattribute__('mapper')(item)
#                        for item in self]

#         if value in self_values:
#             return self[value]

#         return super(FuzzyList, self).__getattribute__(value)

#     def __dir__(self):
#         ''' override the dir to only show new methods and items in the list '''
#         # get all original members of the FuzzyList
#         #class_members = set(list(zip(*inspect.getmembers(self.__class__)))[0])
#         # subtract out members from original list object
#         #members = list(set(class_members) - set(dir(list)))
#         members = super(FuzzyList, self).__dir__()
#         # get parameters in list
#         params = [self.mapper(item) for item in self]
#         return members + params
