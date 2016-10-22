
Background
==========

Since a few years, pipelines (via ``%>%`` of the `magrittr
package <https://cran.r-project.org/web/packages/magrittr/vignettes/magrittr.html>`__)
are quite popular in R and the grown ecosystem of the
`"tidyverse" <https://blog.rstudio.org/2016/09/15/tidyverse-1-0-0/>`__
is built around pipelines. Having tried both the pandas syntax (e.g.
chaining like ``df.groupby().mean()`` or plain
``function2(function1(input))``) and the R's pipeline syntax, I have to
admit that I like the pipeline syntax a lot more.

In my opinion the strength of R's pipeline syntax is:

-  The **same verbs can be used for different inputs** (there are `SQL
   backends for
   dplyr <https://cran.r-project.org/web/packages/dplyr/vignettes/new-sql-backend.html>`__),
   thanks to R's single-dispatch mechanism (called `S3
   objects <http://adv-r.had.co.nz/S3.html>`__).
-  Thanks to **using function** instead of class methods, it's also more
   easily extendable (for a new method on ``pandas.DataFrame`` you have
   to add that to the pandas repository or you need to use monkey
   patching). Fortunatelly, both functions and singledispatch are also
   available in python :-)
-  It **uses normal functions** as pipline parts:
   ``input %>% function()`` is equivalent to ``function(input)``.
   Unfortunately, this isn't easily matched in python, as pythons
   evaluation rules would first evaluate ``function()`` (e.g. call
   functions without any input). So one has to make ``function()``
   return a helper object which can then be used as a pipeline part.
-  R's delayed evaluation rules make it easy to **evaluate arguments in
   the context of the pipeline**, e.g. ``df %>% select(x)`` would be
   converted to the equivalent of pandas ``df[["x"]]``, e.g. the name of
   the variable will be used in the selection. In python it would either
   error (if ``x`` is not defined) or (if ``x`` was defined, e.g.
   ``x = "column"``), would take the value of ``x``, e.g.
   ``df[["column"]]``. For this, some workarounds exist by using helper
   objects like ``select(X.x)``, e.g. `pandas-ply and its
   ``Symbolic expression`` <https://github.com/coursera/pandas-ply>`__.

There exist a few implementation of dplyr like pipeline verbs for python
(e.g. `pandas
itself <http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.pipe.html>`__,
`pandas-ply <https://github.com/coursera/pandas-ply>`__ (uses method
chaining instead of a pipe operator),
`dplython <https://github.com/dodger487/dplython>`__, and
`dfply <https://github.com/kieferk/dfply>`__), but they all focus on
implementing dplyr style pipelines for ``pandas.DataFrames`` and I
wanted to try out a simpler but more general approach to pipelines.
