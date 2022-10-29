#!/usr/bin/env python
"""
Temporal mapping
----------------
"""

###############################################################################
# In this notebook, we will showcase how to use the
# :class:`moscot.problems.time.TemporalProblem`.

from moscot.datasets import hspc
from moscot.problems.time import TemporalProblem

adata = hspc()

###############################################################################
# Let's prepare and solve the problem.

tp = TemporalProblem(adata)
