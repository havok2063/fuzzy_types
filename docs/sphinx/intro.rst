
.. _intro:

Introduction to fuzzy_types
===============================

``fuzzy_types`` provides a set of core classes representing fuzzy Python datatypes and helper functions, using 
`fuzzywuzzy <https://github.com/seatgeek/fuzzywuzzy>`_, a package for fuzzy string matching.  ``fuzzy_types`` currently 
provides fuzzy versions of the following datatypes:

- Python lists (:class:`fuzzy_types.fuzzy.FuzzyList`)
- Python dicts (:class:`fuzzy_types.fuzzy.FuzzyDict`)
- Python OrderedDicts (:class:`fuzzy_types.fuzzy.FuzzyOrderedDict`)

Fuzzy Basics
------------

All fuzzy datatypes are subclassed from the same `FuzzyBase` class and have similar functionality.  Fuzzy datatypes use `fuzzywuzzy`
to provide fuzzy string matching on any string parameter, such as string list items, or dictionary keys.  The following 
example demonstrates fuzziness using ``FuzzyList`` but applies equally to other fuzzy classes.  Let's create a ``FuzzyList``
::

    >>> from fuzzy_types import FuzzyList
    >>> ll = FuzzyList(['apple', 'banana', 'orange', 'pear'])
    >>> ll
    ['apple', 'banana', 'orange', 'pear']

Fuzzy items are accessible by name and fuzzy-matching attempts to handle fuzzy typos.  
:: 

    >>> # access by name
    >>> ll['pear']
    pear

    >>> # access by mispelled name
    >>> ll['paer']
    pear

    >>> ll['appl']
    apple

If a fuzzy item cannot be matched, a `ValueError` is thrown.
::

    >>> ll['mandarin']
    ValueError: Cannot find a good match for 'mandarin'. Your input value is too ambiguous.

A fuzzy attempt must be at least 3 characters along or it throws an error.
::

    >>> ll['ba']
    AssertionError: Your fuzzy search value must be at least 3 characters long.

By default, fuzzy items are also accessible as dottable attributes.  This is enabled by default but can be 
disabled by passing ``dottable=False`` when initializing a fuzzy object.
::

    >>> ll.apple
    apple

    >>> ll = FuzzyList(['apple', 'banana', 'orange', 'pear'], dottable=False)
    >>> ll.apple
    AttributeError: 'list' object has no attribute 'apple'

``FuzzyDict`` and ``FuzzyOrderedDict`` behave almost the same way as ``FuzzyList``.  For dictionaries, the fuzzy matching occurs
**only** for dictionary keys, and not dictionary values.
::

    >>> from fuzzy_types import FuzzyDict
    >>> d = FuzzyDict({'apple':1,'banana':2,'orange':3,'pear':4})
    >>> d.apple
    apple

    >>> d['oang']
    >>> 3

Fuzzy Specifics
---------------

``fuzzywuzzy`` attempts fuzzy string-matching by computing string similarity scores and selecting out the best 
matched score above the cutoff threshold, which is set to a default of 75.  All ``Fuzzy`` classes use a provided convienence 
function, :func:`fuzzy_types.utils.get_best_fuzzy`, for all fuzzy matches. This function can be replaced with any custom 
function via the `use_fuzzy` keyword argument when initializing an object.

By default, ``get_best_fuzzy`` uses a default score threshold of 75/100 and a minimum character limit of 3 when fuzzy matching.
You can modify the default values ``get_best_fuzzy`` uses by setting the following configuration variables inside a custom
YAML config file, located at ``~/.fuzzy/fuzzy_types.yml``.  

:: 

    minimum_fuzzy_characters: 3
    fuzzy_score_cutoff: 75
