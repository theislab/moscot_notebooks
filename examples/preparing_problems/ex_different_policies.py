#!/usr/bin/env python
"""
Using different policies
------------------------
"""

###############################################################################
# This example shows how to use different policies.
#
# A policy is the rule which sets of transport maps are computed given different distributions of cells.
#
# Some problem classes require a certain policy, e.g. the :class:`moscot.solvers.space.MappingProblem`
# only works with the :class:`moscot.solvers._subset_policy.ExternalStarPolicy` meaning that all spatial
# batches from the :class:`anndata.AnnData` object are mapped to the same single cell reference cell distribution.
#
# Each problem class has a set of valid policies. For the :class:`moscot.solvers.time.LineageProblem` and the
# :class:`moscot.solvers.time.TemporalProblem` we can choose among different policies which we demonstrate below.


from moscot.datasets import simulate_data
from moscot.problems.time import TemporalProblem

adata = simulate_data(n_distributions=8, key="day")
adata

###############################################################################
# This simulated dataset contains single cell data across 8 time points, i.e. day 0-8.
#
# The policy allows us to determine which transport maps we want to compute.

###############################################################################
#  Different policies
#  ******************

# In the following, we consider a few policies which can be used for the
# :class:`moscot.solvers.time.TemporalProblem`.

###############################################################################
#  Sequential policy
#  ~~~~~~~~~~~~~~~~~

###############################################################################
# We start with the default policy, which is the sequential policy.
# The following code shows which OT problems are prepared to be solved.

tp_sequential = TemporalProblem(adata)
tp_sequential = tp_sequential.prepare(time_key="day", policy="sequential")
tp_sequential.problems

###############################################################################
# We see that all consecutive pairs of values in the `time_key` column are used to create an OT problem

###############################################################################
# Upper triangular policy
# ~~~~~~~~~~~~~~~~~~~~~~~

tp_triu = TemporalProblem(adata)
tp_triu = tp_triu.prepare(time_key="day", policy="triu")
tp_triu.problems

###############################################################################
# Explicit policy
# ~~~~~~~~~~~~~~~

tp_expl = TemporalProblem(adata)
tp_expl = tp_expl.prepare(time_key="day", policy="explicit", subset=[(0, 1), (1, 3), (4, 9)])
tp_expl.problems

###############################################################################
# In TODO link other notebooks
