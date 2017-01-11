#
# Simple tests to see that pytest works
#

import sys
sys.path.append('..')

def test_import_modules():
    import pydevtools.profiling
    import pydevtools.profiling_late
    import pydevtools.pydebug
