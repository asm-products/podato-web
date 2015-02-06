import os
import sys

# This module adds 'lib' to the python path, so we can store 3rd party libraries there.
# You probably don't need to touch this.

sys.path.append(os.path.join(os.path.dirname(__file__), 'lib'))