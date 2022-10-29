#!/usr/bin/env python
"""
Spatial alignment
-----------------
"""

###############################################################################
# In this notebook, we will showcase how to use the
# :class:`moscot.problems.space.AlignmentProblem`.

from moscot.datasets import sim_align
from moscot.problems.time import AlignmentProblem

adata = sim_align()

###############################################################################
# Let's prepare and solve the problem.

ap = AlignmentProblem(adata)
