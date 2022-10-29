#!/usr/bin/env python
"""
Spatiotemporal mapping
----------------------
"""

###############################################################################
# In this notebook, we will showcase how to use the
# :class:`moscot.problems.spatio_temporal.SpatioTemporalProblem`.

from moscot.datasets import mosta
from moscot.problems.spatio_temporal import SpatioTemporalProblem

adata = mosta()

###############################################################################
# Let's prepare and solve the problem.

stp = SpatioTemporalProblem(adata)
