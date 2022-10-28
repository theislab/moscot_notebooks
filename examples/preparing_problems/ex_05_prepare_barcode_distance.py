#!/usr/bin/env python
"""
Passing barcodes as cost
------------------------
"""

###############################################################################
# This notebook demonstrates how cost matrices are computed from barcode data, 
# specifically useful for the :class:`moscot.problems.time.LineageProblem`.
#
# The :class:`moscot.problems.time.LineageProblem` requires lineage information.
# :mod:`moscot` allows this in three way: by passing precomputed cost matrices,
# by passing barcodes or by passing a lineage tree as a :class:`networkx.DiGraph`.
# In this notebook, we consider the barcode case. 

from moscot.datasets import simulate_data
from moscot.problems.time import LineageProblem

