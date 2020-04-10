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
from fuzzywuzzy import fuzz as fuzz_fuzz
from fuzzywuzzy import process as fuzz_proc
from fuzzy_types import config


def get_best_fuzzy(value, choices, min_score=None, scorer=fuzz_fuzz.WRatio, return_score=False):
    """ Returns the best match in a list of choices using fuzzywuzzy.
    
    Parameters:
        value (str):
            A string to match on
        choices (list):
            A list of string choices to match from
        min_score (int):
            The score cutoff threshold. The minimum score to consider when matching.
        scorer (fuzzywuzzy.Ratio):
            The fuzzywuzzy score ratio to use.  Default is WRatio.
        return_score (bool):
            If True, also returns the score value of the match
    """

    assert isinstance(value, six.string_types), 'Invalid value. Must be a string.'

    min_score = min_score or config.get('fuzzy_score_cutoff', 75)
    minfuzz = config.get('minimum_fuzzy_characters', 3)
    assert len(value) >= minfuzz, f'Your fuzzy search value must be at least {minfuzz} characters long.'

    bests = fuzz_proc.extractBests(value, choices, scorer=scorer, score_cutoff=min_score)

    if len(bests) == 0:
        best = None
    elif len(bests) == 1:
        best = bests[0]
    else:
        if bests[0][1] == bests[1][1]:
            best = None
        else:
            best = bests[0]

    if best is None:
        raise ValueError('Cannot find a good match for {0!r}. '
                         'Your input value is too ambiguous.'.format(value))

    return best if return_score else best[0]
