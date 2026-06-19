"""macOS notification via osascript (built in — no install needed).

If `terminal-notifier` is installed it's used instead (it can deep-link to open
the briefing file on click).
"""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


def _escape_applescript(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"')


def notify(title: str, message: str, open_path: Path | None = None) -> bool:
    """Show a macOS notification. Returns True if a notifier ran."""
    tn = shutil.which("terminal-notifier")
    if tn:
        cmd = [tn, "-title", "Training Tracker", "-subtitle", title, "-message", message, "-sound", "Glass"]
        if open_path:
            cmd += ["-execute", f'open "{open_path}"']
        try:
            subprocess.run(cmd, check=False, timeout=10)
            return True
        except (OSError, subprocess.SubprocessError):
            pass

    osa = shutil.which("osascript")
    if osa:
        script = (
            f'display notification "{_escape_applescript(message)}" '
            f'with title "Training Tracker" subtitle "{_escape_applescript(title)}" '
            f'sound name "Glass"'
        )
        try:
            subprocess.run([osa, "-e", script], check=False, timeout=10)
            return True
        except (OSError, subprocess.SubprocessError):
            pass
    return False
