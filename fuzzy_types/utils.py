# !/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Filename: utils.py
# Project: fuzzy_types
# Author: Brian Cherinka
# Created: Tuesday, 7th April 2020 3:34:46 pm
# License: BSD 3-clause "New" or "Revised" License
# Copyright (c) 2020 Brian Cherinka
# Last Modified: Friday, 10th April 2020 6:46:29 pm
# Modified By: Brian Cherinka


from __future__ import print_function, division, absolute_import
import six
from rapidfuzz import fuzz as fuzz_fuzz
from rapidfuzz import process as fuzz_proc
from fuzzy_types import config
from typing import Callable, Union


def get_best_fuzzy(value: str, choices: list, min_score: int = None, 
                   scorer: Callable = fuzz_fuzz.WRatio, return_score: bool = False) -> Union[None, str]:
    """ Returns the best match in a list of choices using rapidfuzz.

    Parameters
    ----------
    value : str
        A string to match on
    choices : list
        A list of string choices to match from
    min_score : int
        The score cutoff threshold. The minimum score to consider when matching. By default, None
    scorer : Callable
        The rapidfuzz score ratio to use.  By default, WRatio.
    return_score : bool
        If True, also returns the score value of the match.  By default, False.
        
    Returns
    -------
    Union[None, str]
        Either None if no matches found above score, or the best match from list of choices 
          
    Raises
    ------
    ValueError
        when rapidfuzz cannot find a single best match
    """

    assert isinstance(value, six.string_types), 'Invalid value. Must be a string.'

    min_score = min_score or config.get('fuzzy_score_cutoff', 75)
    minfuzz = config.get('minimum_fuzzy_characters', 3)
    assert len(value) >= minfuzz, f'Your fuzzy search value must be at least {minfuzz} characters long.'

    # returns a tuple of (best choice, score, index of choice in list or key of choice in dict)
    bests = fuzz_proc.extract(value, choices, scorer=scorer, score_cutoff=min_score)

    if len(bests) == 0:
        best = None
    elif len(bests) == 1:
        best = bests[0]
    else:
        # compare the two scores of top two choices
        # or take the top choice
        if bests[0][1] == bests[1][1]:
            best = None
        else:
            best = bests[0]

    if best is None:
        raise ValueError(f"Cannot find a good match for '{value}'. "
                         'Your input value is too ambiguous.')

    return best if return_score else best[0]
