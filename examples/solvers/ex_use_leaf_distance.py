#!/usr/bin/env python
"""
Solving linear problems
-----------------------
"""

###############################################################################
# This notebook elaborates on how to solve linear problems, e.g. the
# :class:`moscot.problems.time.TemporalProblem` and the
# :class:`moscot.problems.generic.SinkhornProblem`.

from moscot.datasets import simulate_data
from moscot.problems.time import TemporalProblem
from moscot.problems.generic import SinkhornProblem

adata = simulate_data(n_distributions=2, key="day", cells_per_distribution=5)
adata

###############################################################################
# The :meth:`moscot.problems.time.TemporalProblem.solve` has numerous arguments,
# a few of which will be discussed in the following.
# `epsilon` is the regularization parameter. The lower `epsilon`, the sparser the
# transport map. At the same time, the algorithm takes longer to converge. `tau_a`
# and `tau_b` denote the unbalancedness parameters in the source and the target
# distribution, respectively. `tau_a = 1` means the source marginals have to be fully
# satisfied while `0 < tau_a < 1` relaxes this condition. Analgously, `tau_b` affects
# the marginals of the target distribution. We demonstrate the effect of `tau_a` and `tau_b`
# with the :class:`moscot.problems.generic.SinkhornProblem`.
# Whenever the prior marginals `a` and `b` of the source and the target distribution, 
# respectively, are not passed (TODO link to marginals notebook), they are set to be uniform.

sp = SinkhornProblem(adata)
sp = sp.prepare(time_key="day")
print(sp[0,1].a, sp[0,1].b)

###############################################################################
# First, we solve the problem in a balanced manner, such that the posterior marginals of the
# solution (the sum over the rows and the columns for the source marginals and the
# target marginals, respectively) are equal to the prior marginals.
sp = sp.solve(epsilon=1e-2, tau_a=1, tau_b=1)
print(sp[0,1].solution.a, sp[0,1].solution.b)


###############################################################################
# If we solve an unbalanced problem, the posterior marginals will be different.
sp = sp.solve(epsilon=1e-2, tau_a=0.9, tau_b=0.99)
print(sp[0,1].solution.a, sp[0,1].solution.b)

###############################################################################
# Whenever the dataset is very large, the computational complexity can be 
# reduced by setting `rank` to a positive integer (:cite:`scetbon:21a`). In this 
# case, `epsilon` can also be set to 0, while only the balanced case 
# (`tau_a = tau_b = 1`) is supported.

###############################################################################
# Details
# Whenever the :meth:`moscot.problems.time.TemporalProblem.solve` is called,
# a backend-specific linear solver is instantiated. Currently, :mod:`ott` is
# supported, its corresponding linear solvers are :class:`ott.core.sinkhorn.Sinkhorn`,
# which is used whenever `rank = -1`, and :class:`ott.core.sinkhorn_lr.LRSinkhorn`,
# its counterpart whenever `rank` is a positive integer. :mod:`moscot` wraps these 
# classes in :class:`moscot.backends.ott.SinkhornSolver` which handles both full and
# low rank.
# 
# TODO See other examples for ...
