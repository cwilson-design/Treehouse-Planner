from pathlib import Path
import importlib

# Check that the test directories exist.
if not (Path(__file__).parent / 'layout_images').exists():
    raise OSError(
        'The image directory does not exist. '
        'This is most likely because the test data is not installed. '
        'You may need to install treehousing-planner from source to '
        'get the test data.')

def _check_required_packages():

    for modname in [
            ("matplotlib"),
            ("mathplotlib-inline"),
            ("pytest"),
            ("ipython"),
    ]:
        module = importlib.import_module(modname)

_check_required_packages()