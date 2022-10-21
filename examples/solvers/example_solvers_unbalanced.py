#!/usr/bin/env python
"""
Unbalanced solver
---
This example shows how to solve a problem with the unbalanced approach allowing for deviation from initial marginals.
We showcase over a quadratic problem where unbalanced correction as introduced by :cite:`sejourne:21` is used.

"""

from moscot.problems.space import TemporalProblem
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
# Below are some useful parameters for `moscot.problems. .. .solve()` for the unbalanced case:
#
# - `tau_a` – unbalancedness parameter for left marginal between 0 and 1.
#       tau_a equalling 1 means no unbalancedness in the source distribution.
#       The limit of tau_a going to 0 ignores the left marginals.
#
# - `tau_a` – unbalancedness parameter for right marginal between 0 and 1.
#       tau_b equalling 1 means no unbalancedness in the target distribution.
#       The limit of tau_b going to 0 ignores the right marginals.
#
tp = tp.solve(
        epsilon = 1e-3,
        tau_a = 0.9,
        tau_b = 0.9
)
tp.solutions