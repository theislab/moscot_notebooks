#!/usr/bin/env python
"""
Low-rank solver
---------------
"""

###############################################################################
# This example shows how to solve a problem with the `Low Rank` approach suggested by
# Meyer et al. :cite`scetbon:21a` :cite`scetbon:21b`.

# This is especially useful for large dataset which can not by handled with standard solvers.


from moscot.datasets import hspc
from moscot.problems.time import TemporalProblem

###############################################################################
# Let's load the data, this dataset contains single cell data across 4 time point,
# i.e. day 2.0, 3.0, 4.0 and 7.0.
adata = hspc()

###############################################################################
# We start by initializing a temporal problem and preparing it.

tp = TemporalProblem(adata)
tp = tp.prepare(time_key="day")

###############################################################################
# Below are some useful parameters of `moscot.problems.time.TemporalProblem.solve()` for the Low-rank solver:
#
# - `epsilon` – entropic regularization term.
#
# - `rank` – the rank constraint on the coupling to minimize the linear OT problem
#
# - `gamma` – the (inverse of) gradient stepsize used by mirror descent.
#
# - `initializer` - Initializer to use for the problem, for low-rank available options are
#         - `random`
#         - `rank2` (:cite:`scetbon:21a`)
#         - `k-means` (:cite:`scetbon:22b`)
#         - `generalized-k-means` (:cite:`scetbon:22b`)
#     If `None` the default is `random`.
#
# - `initializer_kwargs` - keyword arguments for the initializer, taken from
#       https://github.com/ott-jax/ott/blob/main/ott/core/initializers_lr.py.
#

tp = tp.solve(
    epsilon=1e-1,
    rank=10,
    gamma=100,
    max_iterations=1e2,
    initializer="k-means",
    initializer_kwargs={"min_iterations": 0, "max_iterations": 100},
)
tp.solutions
