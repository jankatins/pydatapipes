# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, with_statement

try:
    # in py >=3.4
    from functools import singledispatch
except ImportError:
    # backport...
    from singledispatch import singledispatch

import functools

# reexport singledispatch so that library developers don't need to implement the same logic...
__all__ = ['singledispatch', 'PipeVerb', 'pipeverb', 'make_pipesource', 'singledispatch_pipeverb']

class PipeVerb(object):
    """Object which represents a part of a pipeline

    An object of this class can be used as part of a data pipeline: ``1 >> PipeVerb(lambda x: x)``

    :Example:

    >>> @singledispatch_pipeverb
    >>> def my_verb_impl(input, x=1, y=2):
    >>>     raise NotImplementedError("my_verb is not implemented for data of type %s" % type(input))
    >>> @my_verb_impl.register(pd.DataFrame)
    >>> def my_verb_impl_df(input, x=1, y=2):
    >>>     # do something with input being a Dataframe
    >>>     pass
    >>> # ensure that pd.DataFrame is useable as a pipe source
    >>> make_pipesource(pd.DataFrame)
    """

    def __init__(self, func, *args, **kwargs):
        self.pipe_func = func
        self.args = args
        self.kwargs = kwargs

    def __rrshift__(self, input):
        return self.pipe_func(input, *self.args, **self.kwargs)


def pipeverb(func):
    """
    Decorator to convert a function to a pipeline verb (without singledispatch)

    Use this version together with :func:'singledispatch` if you want to create `pipeline verbs`
    which should also be callable as a normal python function ``verb_(input, ...). If you don't
    care about having you verb callable as python function, simply use the convenience decorator
    :func:`singledispatch_pipeverb`.

    Compared to the :func:`singledispatch_pipeverb` decorator, ``func`` is **NOT** converted to a
    :func:`singledispatch` function, but if ``func`` is already a :func:`singledispatch` function,
    the ``register(...)`` method is also exposed on the decorated function.

    This is useful if you want to both expose a normal callable function and the pipeline verb
    version to the user, so that ``verb_(x,y)`` can be used as equivalent of ``x >> verb(y).

    The actual ``func`` must follow these rules to work as a pipeline verb:

    * Pipelines assume that the verbs itself are side-effect free, i.e. they do not change the
      inputs of the data pipeline. This means that actual implementations of a verb for a
      specific data source must ensure that the input is not changed in any way, e.g. if you want
      to pass on a changed value of a ``pd.DataFrame``, make a copy first.
    * The initial function (not the actual implementations for a specific data source) should
      usually do nothing but simply raise `NotImplementedError`, as it is called for all other
      types of data sources.

    To ensure a coherent API for pipeline verbs, the actual ``func`` should follow these
    conventions:

    * Pipeline verbs should actually be named as verbs, e.g. use ``input >> summarize()`` instead of
      ``input >> Summary()``
    * The actual implementation function of a ``verb()`` for a data source of class ``Type``
      should be called ``verb_Type(...)``,  e.g. ``select_DataFrame()``
    * If you want to expose both the pipeline verb and a normal function (which can be called
      directly), the pipeline verb should get the "normal" verb name and the function version
      should get an underscore ``_`` appended, e.g. ``x >> verb()`` -> ``verb_(x)``

    :param func: the function which should be converted
    :type func: function
    :return: PipeVerb instance which can be used in rshift `>>` operations
    :rtype: PipeVerb

    :Example:

    >>> @singledispatch
    >>> def my_verb_(input, x=1, y=2):
    >>>     raise NotImplementedError("my_verb is not implemented for data of type %s" % type(input))
    >>> my_verb = pipeverb(my_verb_)
    >>> @my_verb_.register(pd.DataFrame) # works both on ''my_verb_`` and ``my_verb``
    >>> def my_verb_impl_df(input, x=1, y=2):
    >>>     # do something with input being a Dataframe
    >>>     pass
    >>> # ensure that pd.DataFrame is useable as a pipe source
    >>> make_pipesource(pd.DataFrame)
    """

    @functools.wraps(func)
    def decorated(*args, **kwargs):
        return PipeVerb(func, *args, **kwargs)

    if hasattr(func, 'register'):
        decorated.register = func.register

    return decorated


def make_pipesource(cls):
    """Enables a class to function as a pipe source

    For every new data source used in ``verb.register(data_source)`` (and if that data source
    does not yet implement ``>>`` as the pipe operator), you should also call
    ``make_pipesource(data_source)`` once.

    If you want to make a data source pipeable by default, either do not implement a
    ``__rshift__()`` method or simply define you class and after the class definition call
    ``make_pipesource(YourClass)``.

    Internally, it replaces an implemented ``__rshift__()`` method with one which will check if the
    right side is a :class:`PipeVerb` and if so will call that sides ``__rrshift__()`` method
    instead. Otherwise the original ``__rshift__()`` method is called.

    :param cls: a class which should work as a pipe source
    :type cls: class
    """
    if hasattr(cls, '__rshift__') and (not getattr(cls.__rshift__, 'pipeoperator', False)):
        def __rshift__(self, other):
            """Pipeline operator if the right side is a PipeVerb"""
            if isinstance(other, PipeVerb):
                return other.__rrshift__(self)
            else:
                return self.__orig_rshift__(other)

        cls.__orig_rshift__ = cls.__rshift__
        cls.__rshift__ = __rshift__
        try:
            cls.__rshift__.pipeoperator = True
        except AttributeError:
            # py27
            cls.__rshift__.__func__.pipeoperator = True

def singledispatch_pipeverb(func):
    """
    Convenience decorator to convert a function to a singledispatch pipeline verb

    The function is converted to a :func:`singledispatch` function and then
    converted into an instance of class :class:`PipeVerb` via :func:`pipeverb`.

    This decorator is equivalent to ``verb = pipeverb(singledispatch(func))``

    Please see :func:`pipeverb` for rules which a pipeline verb has to follow!

    :param func: the function which should be converted
    :type func: function
    :return: PipeVerb instance which can be used in rshift `>>` operations
    :rtype: PipeVerb

    :Example:

    >>> @singledispatch_pipeverb
    >>> def my_verb_impl(input, x=1, y=2):
    >>>     raise NotImplementedError("my_verb is not implemented for data of type %s" % type(input))
    >>> @my_verb_impl.register(pd.DataFrame)
    >>> def my_verb_impl_df(input, x=1, y=2):
    >>>     # do something with input being a Dataframe
    >>>     pass
    >>> # ensure that pd.DataFrame is useable as a pipe source
    >>> make_pipesource(pd.DataFrame)


    .. seealso:: :func:`pipeverb`, :func:`singledispatch`
    """
    return pipeverb(singledispatch(func))
