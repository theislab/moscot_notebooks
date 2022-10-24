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
<<<<<<< HEAD:examples/problems/ex_03_different_policies.py
# Some problem classes require a certain policy, e.g. the :class:`moscot.problems.space.MappingProblem`
# only works with the :class:`moscot.problems._subset_policy.ExternalStarPolicy` meaning that all spatial
# batches from the :class:`anndata.AnnData` object are mapped to the same single cell reference cell distribution.
#
# Each problem class has a set of valid policies. For the :class:`moscot.problems.time.LineageProblem` and the
# :class:`moscot.problems.time.TemporalProblem` we can choose among different policies which we demonstrate below.
=======
# Some problem classes require a certain policy, e.g. the :class:`moscot.solvers.space.MappingProblem`
# only works with the :class:`moscot.problems._subset_policy.ExternalStarPolicy` meaning that all spatial
# batches from the :class:`anndata.AnnData` object are mapped to the same single cell reference cell distribution. 
#
# Each problem class has a set of valid policies. For the :class:`moscot.solvers.time.LineageProblem` and the
<<<<<<< HEAD
# :class:`moscot.solvers.time.TemporalProblem` we can choose among different policies which we demonstrate below.
>>>>>>> add examples and draft for st tutorial:examples/example_different_policies.py
=======
# :class:`moscot.problems.time.TemporalProblem` we can choose among different policies which we demonstrate below.
>>>>>>> Update example_different_policies.py

from moscot.datasets import simulation
from moscot.problems.time import TemporalProblem

adata = simulation(size=15360)

###############################################################################
# This simulated dataset contains single cell data across 4 time point, i.e. day 11.0, 12.0, 13.0 and 14.0.
#
# The policy allows us to determine which transport maps we want to compute.

###############################################################################
#  Different policies
#  ******************

<<<<<<< HEAD:examples/problems/ex_03_different_policies.py
# In the following, we consider a few policies which can be used for the
# :class:`moscot.problems.time.TemporalProblem`.
=======
# In the following, we consider a few policies which can be used for the 
# :class:`moscot.solvers.time.TemporalProblem`.
>>>>>>> add examples and draft for st tutorial:examples/example_different_policies.py

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
tp_expl = tp_expl.prepare(time_key="day", policy="explicit", subset=[(10, 11), (12, 13), (10, 13)])
tp_expl.problems

###############################################################################
#  Using the `filter` argument
#  ***************************

###############################################################################
# If we want to use the sequential policy but restrict it to a
# certain subset of distributions we can use the `filter` argument.

tp_filtered = TemporalProblem(adata)
tp_filtered = tp_filtered.prepare(time_key="day", policy="sequential", filter=[10, 12, 13])
tp_filtered.problems

###############################################################################
# Analogously, the `filter` argument can also be applied to other policies, e.g. the upper triangular policy.
