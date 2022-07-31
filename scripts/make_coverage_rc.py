"""A script to make a coveragerc file for testing based on the platform."""

import os
import sys
from pathlib import Path


def main() -> None:
    """Make the file."""
    rcfile_path = os.environ["COVERAGE_RCFILE"]

    if sys.platform.startswith("win"):
        platform = "windows"
    elif sys.platform.startswith("darwin"):
        platform = "macos"
    elif sys.platform.startswith("linux"):
        platform = "linux"
    else:
        raise Exception("Unidentified platform")

    extra_omit = "test/test_graphics.py" if platform == "windows" else ""
    Path(rcfile_path).write_text(
        Path(".coveragerc.in")
        .read_text()
        .format(platform=platform, extra_omit=extra_omit),
    )


if __name__ == "__main__":
    main()
