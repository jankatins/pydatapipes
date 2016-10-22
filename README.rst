=====================
Python data pipelines
=====================


.. image:: https://img.shields.io/pypi/v/pydatapipes.svg
        :target: https://pypi.python.org/pypi/pydatapipes

.. image:: https://img.shields.io/travis/janschulz/pydatapipes.svg
        :target: https://travis-ci.org/janschulz/pydatapipes

.. image:: https://readthedocs.org/projects/pydatapipes/badge/?version=latest
        :target: https://pydatapipes.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/janschulz/pydatapipes/shield.svg
     :target: https://pyup.io/repos/github/janschulz/pydatapipes/
     :alt: Updates


Features
--------

This package implements the basics for building pipelines similar to magrittr in R. Pipelines are
created using ``>>``. Internally it uses singledispatch_ to provide a way for a unified API
for different kinds of inputs (SQL databases, HDF, simple dicts, ...).

Basic example what can be build with this package:

.. code-block:: python

    >>> from my_library import append_col
    >>> import pandas as pd

    >>> pd.DataFrame({"a" : [1,2,3]}) >> append_col(x=3)
       a  X
    0  1  3
    1  2  3
    2  3  3

In the future, this package might also implement the verbs from the R packages dplyr_ and
tidyr_ for ``pandas.DataFrame`` and  or I will fold this into one of the other available
implementation of dplyr_ style pipelines/verbs for pandas.


Documentation
-------------

The documentaiton can be found on ReadTheDocs_: https://pydatapipes.readthedocs.io

License
-------

Free software: MIT license

Credits
---------

* magrittr_ and it's usage in dplyr_ / tidyr_ for the idea of using pipelines in that ways
* lots of python implementations of dplyr style pipelines: dplython_, pandas_ply_, dfply_


This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _ReadTheDocs: https://readthedocs.org/
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _magrittr: https://cran.r-project.org/web/packages/magrittr/vignettes/magrittr.html
.. _dplyr: https://cran.rstudio.com/web/packages/dplyr/vignettes/introduction.html
.. _tidyr: https://cran.r-project.org/web/packages/tidyr/index.html
.. _singledispatch: https://docs.python.org/3/library/functools.html#functools.singledispatch
.. _dplython: https://github.com/dodger487/dplython
.. _pandas_ply: https://github.com/coursera/pandas-ply
.. _dfply: https://github.com/kieferk/dfply
