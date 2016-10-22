#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, with_statement

"""
test_pydatapipes
----------------------------------

Tests for `pydatapipes` module.
"""

import pytest

from pydatapipes.pipes import singledispatch_pipeverb, pipeverb, make_pipesource, singledispatch, PipeVerb


def test_pipeverb():
    """Tests that pipeverv works
    """

    @singledispatch
    def append_(input, x=1):
        """Docstring"""
        raise NotImplementedError("append is not implemented for data of type %s" % type(input))

    append = pipeverb(append_)

    @append.register(list)
    def append_list(input, x=1):
        return input + [x]

    @append.register(str)
    def append_list(input, x=1):
        return input + str(x)

    assert isinstance(append(), PipeVerb)

    assert [] >> append() == [1]
    assert "" >> append() == "1"

    assert append_([]) == [1]
    assert append_("") == "1"

    with pytest.raises(NotImplementedError):
        1 >> append()

    with pytest.raises(NotImplementedError):
        object() >> append()

    with pytest.raises(NotImplementedError):
        append_(1)


def test_maintain_docstring():
    """Tests that a pipever has the docstrng from the generic method
    """

    @singledispatch
    def append_(input, x=1):
        """Docstring generic"""
        raise NotImplemented("append is not implemented for data of type %s" % type(input))

    append = pipeverb(append_)

    @append.register(list)
    def append_list(input, x=1):
        """Docstring list"""
        return input + [x]

    assert append_.__doc__ == "Docstring generic"
    assert append.__doc__ == "Docstring generic"


def test_singledispatch_pipeverb():
    """Tests that pipeverv works
    """

    @singledispatch_pipeverb
    def append(input, x=1, y=2):
        """Docstring"""
        raise NotImplemented("append is not implemented for data of type %s" % type(input))

    @append.register(list)
    def append_list(input, x=1, y=2):
        return input + [x, y]

    # list has no __rshift__, so no need for make_pipesource

    assert append.__doc__ == "Docstring"

    assert [] >> append() == [1, 2]
    assert [] >> append(2) == [2, 2]
    assert [] >> append(2, y=4) == [2, 4]
    assert [1] >> append(2) >> append(3, 3) == [1, 2, 2, 3, 3]


def test_make_pipesource():
    class Tester(object):
        def __rshift__(self, other):
            """ORIG RSHIFT"""
            return "TESTER"

    @singledispatch_pipeverb
    def test_verb(input):
        return "VERB"

    assert Tester() >> 1 == "TESTER"
    assert Tester() >> test_verb() == "TESTER"
    assert not hasattr(Tester.__rshift__, "pipeoperator")

    make_pipesource(Tester)

    assert "Pipeline" in Tester.__rshift__.__doc__
    assert Tester.__rshift__.pipeoperator
    assert hasattr(Tester.__rshift__, "pipeoperator")
    assert hasattr(Tester, "__orig_rshift__")
    assert Tester().__orig_rshift__(1) == "TESTER"
    assert Tester() >> test_verb() == "VERB"
    assert Tester() >> 1 == "TESTER"

    # assure that we don't replace twice!
    make_pipesource(Tester)
    assert Tester().__orig_rshift__(1) == "TESTER"
    assert "ORIG RSHIFT" in Tester().__orig_rshift__.__doc__


def test_PipeVerb():
    """Test PipeVerb internals"""

    do_nothing = lambda: PipeVerb(lambda x: x)
    assert 1 >> do_nothing()


    f = lambda x, a, y=1: x + a + y
    x = PipeVerb(f, 2, y=1)
    assert x.pipe_func == f
    assert x.args == (2,)
    assert x.kwargs == dict(y=1)

    assert x.__rrshift__(1) == f(1, 2, y=1)
