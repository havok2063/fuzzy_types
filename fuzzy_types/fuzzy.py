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
import inspect
import six
from fuzzy_types.utils import get_best_fuzzy
from typing import Callable, Union, TypeVar

__all__ = ['FuzzyBase', 'FuzzyBaseDict', 'FuzzyList', 'FuzzyDict', 'FuzzyOrderedDict', 'FuzzyStr']

# types
FL = TypeVar('FL', bound='FuzzyList')
FD = TypeVar('FD', bound='FuzzyDict')
FOD = TypeVar('FOD', bound='FuzzyOrderedDict')
FS = TypeVar('FS', bound='FuzzyStr')
AF = Union[FL, FD, FOD, FS]

class FuzzyBase(abc.ABC):
    """ Abstract Base Class for all Fuzzy objects """
    _base = None

    def __init__(self, the_items: Union[list, dict], use_fuzzy: Callable = None, 
                 dottable: bool = True):
        self.use_fuzzy = use_fuzzy or get_best_fuzzy
        self._dottable = dottable
        self._base.__init__(self, the_items)

    def __getattr__(self, value: Union[str, int, object]):
        if self._dottable is False:
            raise AttributeError(f"'{self._base.__name__}' object has no attribute '{value}'")

        if '__' in value:
            return super(FuzzyBase, self).__getattr__(value)
        return self.__getitem__(value)

    @abc.abstractmethod
    def __getitem__(self, value):
        pass

    @abc.abstractmethod
    def __dir__(self) -> list:
        return object.__dir__(self)

    @staticmethod
    def mapper(item: Union[str, object]) -> str:
        """ Mapper between list/dict item and rapidfuzz choices  

        Static method used to map a list's items or dict's keys to a
        string representation used by ``rapidfuzz`` for.  By default returns an
        explicit string case of the item.  To see the output, view the ``choices``
        property.  Can be overridden to customize what is input into ``rapidfuzz``. 

        Parameters
        ----------
        item : Union[str, object]
            Any iterable item, i.e. a list item or dictionary key

        Returns
        -------
        str
            The string representation to use in the choices supplied to ``rapidfuzz``
        """
        return str(item)

    @abc.abstractproperty
    def choices(self):
        pass

    def __contains__(self, value: Union[str, int, object]) -> bool:
        if not isinstance(value, six.string_types):
            return super(FuzzyBase, self).__contains__(value)

        try:
            best = self.use_fuzzy(value, self.choices)
        except ValueError:
            best = None

        return best in self.choices

    def copy(self) -> AF:
        """ Returns a copy of the fuzzy instance

        Returns
        -------
        Union[list, dict]
            A copy of the fuzzy instance
        """
        if self._base == OrderedDict:
            kopied = dict(self)
        else:
            kopied = self._base.copy(self)
        return self.__class__(kopied, use_fuzzy=self.use_fuzzy, dottable=self._dottable)

    def to_original(self) -> Union[list, dict]:
        """ Convert fuzzy object back to original Python datatype """
        return self._base(self)


class FuzzyBaseDict(FuzzyBase):

    def __init__(self, the_dict: dict, use_fuzzy: Callable = None, dottable: bool = True):
        super(FuzzyBaseDict, self).__init__(the_dict, use_fuzzy=use_fuzzy, dottable=dottable)
        # in case a value is another dictionary; also make it fuzzy
        for key, val in the_dict.items():
            if isinstance(val, dict):
                self[key] = self.__class__(val)

    def __getitem__(self, value: Union[int, str]):
        if not isinstance(value, six.string_types):
            return self.get(value)

        best = self.use_fuzzy(value, self.choices)
        return self._base.__getitem__(self, best)

    def __dir__(self) -> list:
        members = super(FuzzyBaseDict, self).__dir__()
        if self._dottable is True:
            members.extend(self.choices)
        return members

    @property
    def choices(self) -> list:
        """ A list of choices used during fuzzy matching

        The list of choices passes into ``rapidfuzz`` to use 
        for fuzzy-matching a string.  The list of choices is computed
        by iterating over the dictionary keys, passing each item through
        the `~FuzzyBase.mapper` method. 

        Returns
        -------
        list
            The list of options used by ``rapidfuzz`` when fuzzy matching
        """
        return [self.mapper(i) for i in self.keys()]


class FuzzyDict(FuzzyBaseDict, dict):
    """ A dotable dictionary that uses rapidfuzz to select the key.

    Parameters
    ----------
    the_items : dict
        A dictionary of items to make fuzzy
    use_fuzzy : Callable 
        The function used to perform the fuzzy-matching.
        Default is :func:`fuzzy_types.utils.get_best_fuzzy`.
    dottable : bool
        If False, turns off dottable attributes.  Default is True.

    Returns
    -------
        A python dictionary with fuzzy keys
    """
    _base = dict


class FuzzyOrderedDict(FuzzyBaseDict, OrderedDict):
    """ A dotable ordered dictionary that uses rapidfuzz to select the key.

    Parameters
    ----------
    the_items : dict
        A dictionary of items to make fuzzy
    use_fuzzy : Callable 
        The function used to perform the fuzzy-matching.
        Default is :func:`fuzzy_types.utils.get_best_fuzzy`.
    dottable : bool
        If False, turns off dottable attributes.  Default is True.

    Returns
    -------
        A python ordered dictionary with fuzzy keys

    """
    _base = OrderedDict


class FuzzyList(FuzzyBase, list):
    """ A dottable python list that uses rapidfuzz to select a string item

    Parameters
    ----------
    the_items : list
        A list of items to make fuzzy
    use_fuzzy : Callable 
        The function used to perform the fuzzy-matching.
        Default is :func:`fuzzy_types.utils.get_best_fuzzy`.
    dottable : bool
        If False, turns off dottable attributes.  Default is True.

    Returns
    -------
        A python list with fuzzy items

    """
    _base = list

    @property
    def choices(self) -> list:
        """ A list of choices used during fuzzy matching

        The list of choices passes into ``rapidfuzz`` to use 
        for fuzzy-matching a string.  The list of choices is computed
        by iterating over the list items, passing each item through
        the `~FuzzyBase.mapper` method. 

        Returns
        -------
        list
            The list of options used by ``rapidfuzz`` when fuzzy matching
        """
        return [self.mapper(item) for item in self]

    def __getitem__(self, value):
        if not isinstance(value, six.string_types):
            return list.__getitem__(self, value)

        best = self.use_fuzzy(value, self.choices)
        return self[self.choices.index(best)]

    def __dir__(self) -> list:
        members = super(FuzzyList, self).__dir__()
        if self._dottable is True:
            members.extend(self.choices)
        return members


class FuzzyStr(str):
    """ A fuzzy string that uses rapidfuzz for equality checks

    Parameters
    ----------
    the_string : str
        A string to make fuzzy
    use_fuzzy : Callable
        The function used to perform the fuzzy-matching.
        Default is :func:`fuzzy_types.utils.get_best_fuzzy`.
    """
    _base = str

    def __init__(self, the_string: str, use_fuzzy: Callable = None):
        self.use_fuzzy = use_fuzzy or get_best_fuzzy
        self._base.__init__(the_string)

    def __eq__(self, value: str) -> bool:
        try:
            self.use_fuzzy(value, [self])
        except ValueError:
            return False
        else:
            return True
