#!/usr/bin/env python
"""
Quadratic solver
----------------
"""
###############################################################################
# This example shows how to solve a Fused Qaudratic problem.

###############################################################################
# Let's load the data, this dataset contains spatiotemporal transcriptomics

from moscot.datasets import mosta
from moscot.problems.spatio_temporal import SpatioTemporalProblem

###############################################################################
# Let's load the data, this dataset contains spatiotemporal transcriptomics
# atlas of mouse organogenesis in two time points, E9.5, E10.5
adata = mosta()

###############################################################################
# We start by initializing a spatio-temporal problem and preparing it.

stp = SpatioTemporalProblem(adata=adata).prepare(
    time_key="time",
    spatial_key="spatial",
    joint_attr=None,
    callback="local-pca",
)
