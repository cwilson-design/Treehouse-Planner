
from pathlib import Path

# Check that the test directories exist.
if not (Path(__file__).parent / 'test_files').exists():
    raise OSError(
        'The test files directory does not exist. '
        'This is most likely because the test data is not installed. '
        'You may need to install treehouse_draft_program from source to get the '
        'test data.')