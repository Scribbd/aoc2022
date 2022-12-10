import sys
from pathlib import Path

base = f"day_{sys.argv[1]}"
_input = f"{base}/input"

Path(_input).mkdir(parents=True)
Path(f"{_input}/day_10").touch()
Path(f"{base}/{base}.py").touch()