"""CLI entry point for the shared IDP image manifest validator."""

import sys
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from tooling.idp_images import main  # noqa: E402  (repo root is required for direct script execution)

if __name__ == "__main__":
    raise SystemExit(main())
