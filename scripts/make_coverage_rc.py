"""A script to make a coveragerc file for testing based on the platform."""

import os
import sys
from pathlib import Path

scripts_path = Path(__file__).parent
rc_in_path = scripts_path / ".coveragerc.in"


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
    extra_exclude = (
        'if sys.platform.startswith\\("win"\\):' if platform != "windows" else ""
    )
    Path(rcfile_path).write_text(
        rc_in_path.read_text().format(
            platform=platform,
            extra_omit=extra_omit,
            extra_exclude=extra_exclude,
        ),
    )


if __name__ == "__main__":
    main()
