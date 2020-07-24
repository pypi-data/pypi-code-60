# -*- coding: utf-8 -*-
"""
The REsource eXtraction tool (rex)
"""
from __future__ import print_function, division, absolute_import
import os

from rex.multi_year_resource import (MultiYearResource, MultiYearNSRDB,
                                     MultiYearWindResource)
from rex.rechunk_h5 import RechunkH5, to_records_array
from rex.renewable_resource import (NSRDB, MultiFileNSRDB, MultiFileWTK,
                                    SolarResource, WindResource)
from rex.resource import Resource
from rex.resource_extraction import (ResourceX, MultiYearResourceX,
                                     NSRDBX, MultiFileNSRDBX, MultiYearNSRDBX,
                                     WindX, MultiFileWindX, MultiYearWindX)
from rex.utilities import init_logger, init_mult, SpawnProcessPool, Retry

from rex.version import __version__

__author__ = """Michael Rossol"""
__email__ = "michael.rossol@nrel.gov"

REXDIR = os.path.dirname(os.path.realpath(__file__))
TESTDATADIR = os.path.join(os.path.dirname(REXDIR), 'tests', 'data')
TREEDIR = os.path.join(os.path.dirname(REXDIR), 'bin', 'trees')
