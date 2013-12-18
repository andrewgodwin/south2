__version__ = "2.0.0a1"

# We need to ensure that monkeypatches are installed before anything else
# loads, so they're triggered here.
import os
if not os.environ.get("SOUTH_NO_MONKEY_PATCH", None):
    import south.patches
