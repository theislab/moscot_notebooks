#!/usr/bin/env python
"""
Solving linear problems
-----------------------
"""

###############################################################################
# This examples is a continuation of TODO reference and shows advanced examples
# for how to solve linear problems like the 
# :class:`moscot.problems.time.TemporalProblem` and the
# :class:`moscot.problems.generic.SinkhornProblem`.

import numpy as np
from moscot.datasets import simulate_data
from moscot.problems.generic import SinkhornProblem

adata = simulate_data(n_distributions=2, key="day")
adata

###############################################################################
# The `threshold` parameter defines the convergence criterion. In the balanced
# setting the `threshold` denotes the deviation between prior and posterior
# marginals, while in the unbalanced setting the `threshold` corresponds to 
# a Cauchy sequence stopping criterion. 
# 
# Different Initializers can help to improve convergence. For the full-rank
# case we can set the initializer to the trivial initializing method denoted
# by `default`. The `gaussian` (:cite:`thornton2022`) initializer computes
# Gaussian approximations of two point clouds and leverages the closed-form 
# solution of Optimal Transport problems between Gaussians, while the `sorting`
# initializer (:cite:`thornton2022`) solves a simplified (sorting) Optimal Transport 
# problem and uses its solution as initializer.


# Implementation details
# ~~~~~~~~~~~~~~~~~~~~~~
# Whenever the :meth:`moscot.problems.time.TemporalProblem.solve` is called,
# a backend-specific linear solver is instantiated. Currently, :mod:`ott` is
# supported, its corresponding linear solvers are :class:`ott.core.sinkhorn.Sinkhorn`,
# which is used whenever `rank = -1`, and :class:`ott.core.sinkhorn_lr.LRSinkhorn`,
# its counterpart whenever `rank` is a positive integer. :mod:`moscot` wraps these 
# classes in :class:`moscot.backends.ott.SinkhornSolver` which handles both full and
# low rank.
# 
# TODO See other examples for ...
