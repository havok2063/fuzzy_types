
.. _intro:

Introduction to fuzzy_types
===============================

``fuzzy_types`` provides a set of core classes representing fuzzy Python datatypes and helper
functions, using `rapidfuzz <https://github.com/maxbachmann/rapidfuzz>`_, a package for fuzzy
string matching package based on `fuzzywuzzy <https://github.com/seatgeek/fuzzywuzzy>`_.
``fuzzy_types`` currently provides fuzzy versions of the following datatypes:

- Python lists (:class:`fuzzy_types.fuzzy.FuzzyList`)
- Python dicts (:class:`fuzzy_types.fuzzy.FuzzyDict`)
- Python OrderedDicts (:class:`fuzzy_types.fuzzy.FuzzyOrderedDict`)
- Python str (:class:`fuzzy_types.fuzzy.FuzzyStr`)

Fuzzy Basics
------------

All fuzzy datatypes are subclassed from the same `FuzzyBase` class and have similar functionality.  Fuzzy datatypes use `fuzzywuzzy`
to provide fuzzy string matching on any string parameter, such as string list items, or dictionary keys.  The following
example demonstrates fuzziness using ``FuzzyList`` but applies equally to other fuzzy classes.  Let's create a ``FuzzyList``
::

    >>> from fuzzy_types.fuzzy import FuzzyList
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

    >>> from fuzzy_types.fuzzy import FuzzyDict
    >>> d = FuzzyDict({'apple':1,'banana':2,'orange':3,'pear':4})
    >>> d.apple
    apple

    >>> d['oang']
    >>> 3

``FuzzyStr`` objects behave exactly like regular strings, except their equality operator has been overridden to be fuzzy.
::

    >>> from fuzzy_types.fuzzy import FuzzyStr
    >>> s = FuzzyStr('apple')
    >>> 'appl' == s
    True

    >>> 'chocolate' == s
    False


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

Copying a ``Fuzzy`` object produces a new ``Fuzzy`` object.
::

    >>> # copy a FuzzyList
    >>> tt = ll.copy()
    >>> type(tt)
    fuzzy_types.fuzzy.FuzzyList

You can convert a ``Fuzzy`` object back to its original type with `to_original` method.
::

    >>> # convert a FuzzyList back to a regular python list
    >>> old = tt.to_original()
    >>> old
    ['apple', 'banana', 'orange', 'pear']

    >>> type(old)
    list

Fuzzy Customizations
--------------------

All ``fuzzy_types`` use `~fuzzy_types.utils.get_best_fuzzy` to perform fuzzy matching, which 
itself wraps the `.rapidfuzz.process.extract` function.  The default fuzzy-matching function can be 
overridden in any ``fuzzy_types`` object, by passing a new callable function into the ``use_fuzzy`` 
keyword argument.  

The `.rapidfuzz.process.extract` function used by the default `~fuzzy_types.utils.get_best_fuzzy` 
accepts as input a list of "choices", any iterable list of string used for comparison during fuzzy
matching.  To see the list of choices used by any ``fuzzy_types``, access the ``choices`` property, 
e.g. `.fuzzy_types.fuzzy.FuzzyList.choices` or `.fuzzy_types.fuzzy.FuzzyBaseDict.choices`.
::

    >>> from fuzzy_types import FuzzyList
    >>> ll = FuzzyList(['apple', 'banana', 'orange', 'pear'])
    >>>
    >>> # look at the list of choices passed to rapidfuzz
    >>> ll.choices
    ['apple', 'banana', 'orange', 'pear']

The mapping between the items in a ``FuzzyList`` or ``FuzzyDict``, and the list of ``choices`` passed 
to ``rapidfuzz``, is controlled by the base `.fuzzy_types.fuzzy.FuzzyBase.mapper` method.  By default, 
the ``mapper`` returns an explicit string of a list's items or dict's keys, i.e. ``str(item)``.  This
means that by default, ``FuzzyList`` operates as a list of strings. 
  
The ``mapper`` method can be overridden to customize how the items in your input list or dict 
get converted into a list of fuzzy options, e.g. creating a fuzzy list of objects where you want to
perform fuzzy matching using an attribute of the instance.  Suppose we have a class representing a
type of toy
::

    class Toy(object):
        """ class representing toy objects """
        def __init__(self, name='toy'):
            self.name = name
            
        def __repr__(self):
            return f'<Toy(name="{self.name}")>'

And we have a list of toys that we want to convert to a fuzzy list. 
::
    
    >>> # create a list of toy objects
    >>> toys = [Toy(n) for n in ['car', 'truck', 'top', 'ball', 'rag', 'doll']]
    >>> toys
    [<Toy(name="car")>, <Toy(name="truck")>, <Toy(name="top")>, <Toy(name="ball")>, <Toy(name="rag")>, <Toy(name="doll")>]

    >>> create a fuzzy list of toys
    >>> tt = FuzzyList(toys)

By default ``fuzzy_types`` will map each instance's string ``repr`` to the list of choices.  This may 
not be ideal, or even desired, for complex reprs and could confuse the fuzzy matching.
::

    >>> # view the default choices passed to rapidfuzz
    >>> tt.choices
    ['<Toy(name="car")>', '<Toy(name="truck")>', '<Toy(name="top")>', '<Toy(name="ball")>', '<Toy(name="rag")>', '<Toy(name="doll")>']

To instead customize the ``FuzzyList`` of ``Toys`` to use the ``name`` attribute for all fuzzy matching, 
we can create a new custom ``FuzzyList`` class overriding the default ``mapper`` method.
::

    class FuzzyToy(FuzzyList):
        """ custom fuzzy list for toys """

        @staticmethod
        def mapper(item):
            """ overridden mapper to return the toy's name """
            return str(item.name)

Now we create a new list of ``FuzzyToy`` where the ``choices`` are mapped to the correct attribute 
::

    >>> # create a new fuzzy list of toys
    >>> tt = FuzzyToy(toys)
    >>> tt
    [<Toy(name="car")>, <Toy(name="truck")>, <Toy(name="top")>, <Toy(name="ball")>, <Toy(name="rag")>, <Toy(name="doll")>]

    >>> # view the fuzzy choices passed to rapidfuzz
    >>> tt.choices
    ['car', 'truck', 'top', 'ball', 'rag', 'doll']

Overriding the ``mapper`` also controls what is shown as a dottable attribute.
::

    >>> # each Toy.name is added as a dottable attribute
    >>> tt.doll
    <Toy(name="doll")>