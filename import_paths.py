import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).parent
TOOL_MODULE_DIR = PROJECT_ROOT / "tools"


def ensure_project_paths():
    tool_path = str(TOOL_MODULE_DIR)

    if tool_path not in sys.path:
        sys.path.insert(0, tool_path)
