#!/usr/bin/env python
"""
Linear solver
---
This example shows the advanced options for a linear problem solver
(the `SinkhornSolver`) exemplified using :class:`moscot.solvers.time.TemporalProblem`.


.. seealso::
    See :ref:`sphx_glr_auto_examples_example_different_policies.py` for policy alternatives
    and :ref:`sphx_glr_auto_tutorials_tutorial_temporal.py` for additional properties.
"""

from moscot.problems.time import TemporalProblem
from moscot.datasets import hspc

###############################################################################
# Let's load the data, this dataset contains single cell data across 4 time point,
# i.e. day 2.0, 3.0, 4.0 and 7.0.
adata = hspc()

###############################################################################
# We start by initializing a temporal problem and preparing it.

tp = TemporalProblem(adata)
tp = tp.prepare(time_key="day")

###############################################################################
# Below are some useful parameters of `moscot.problems.time.TemporalProblem.solve()`:
#
# - `epsilon` – entropic regularization term.
#
# - `scale_cost` – option to rescale the cost matrix. Implemented scalings are
#       "median", "mean", "max_cost", "max_norm" and "max_bound".
#       Alternatively, a float factor can be given to rescale the cost such
#       that ``cost_matrix /= scale_cost``. If `True`, use "mean".
#
# - `batch_size` – size of the batch for online computation avoiding matrix instantiation
#
# - `max_iterations` -  the maximum number of Sinkhorn iteration`
#
# - `stage` – stages of sub-problems which are to be solved. By default, prepared and solved problems are solved,
#     ("prepared", "solved").

tp = tp.solve(
    epsilon=1e-2,
    scale_cost="max_cost",
    max_iterations=1000,
    stage=("prepared", "solved"),
)
tp.solutions

