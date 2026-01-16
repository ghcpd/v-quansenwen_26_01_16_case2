import os
import sys

_TESTS = os.path.dirname(__file__)
_ROOT = os.path.abspath(os.path.join(_TESTS, os.pardir))
_SRC = os.path.join(_ROOT, "src")

if os.path.isdir(_SRC) and _SRC not in sys.path:
    sys.path.insert(0, _SRC)
