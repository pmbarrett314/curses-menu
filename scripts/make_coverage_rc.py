"""A script to make a coveragerc file for testing based on the platform."""

import os
from pathlib import Path


def main() -> None:
    """Make the file."""
    rcfile_path = os.environ["COVERAGE_RCFILE"]
    platform = os.environ["PLATFORM"]

    extra_omit = "test/test_graphics.py" if platform == "windows" else ""
    Path(rcfile_path).write_text(
        Path(".coveragerc.in")
        .read_text()
        .format(platform=platform, extra_omit=extra_omit),
    )


if __name__ == "__main__":
    main()
