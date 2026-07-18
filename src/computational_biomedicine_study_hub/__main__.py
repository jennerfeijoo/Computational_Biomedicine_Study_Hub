"""Allow the package to run with ``python -m``."""

from __future__ import annotations

from .application import main

if __name__ == "__main__":
    raise SystemExit(main())
