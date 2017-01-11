#
# Simple tests to see that pytest works
#

def test_import_modules():
    import sys
    sys.path.append('.')

    import pydevtools.profiling
    import pydevtools.profiling_late
    import pydevtools.pydebug
