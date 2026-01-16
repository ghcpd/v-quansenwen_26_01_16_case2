import os
import sys

_ROOT = os.path.dirname(__file__)
_SRC = os.path.join(_ROOT, "src")

if os.path.isdir(_SRC) and _SRC not in sys.path:
    sys.path.insert(0, _SRC)
