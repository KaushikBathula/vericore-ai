"""Utilities for locating external EDA executables."""

from __future__ import annotations

import shutil
from pathlib import Path


class ToolchainExecutableNotFoundError(RuntimeError):
    """Raised when a required external tool cannot be found."""

    def __init__(self, tool_name: str, stage: str) -> None:
        """Create a stage-specific missing-tool error."""
        super().__init__(
            f"{stage} failed because required executable '{tool_name}' "
            "was not found on PATH. Verify the tool is installed and "
            "available to the backend process."
        )
        self.tool_name = tool_name
        self.stage = stage


def resolve_executable(tool_name: str, stage: str) -> str:
    """Return the absolute executable path or raise a clear toolchain error."""

    # Verilator's OSS CAD Suite installation on Windows may expose
    # `verilator` as a Perl wrapper while the native executable is
    # `verilator_bin.exe`.
    candidates = [tool_name]

    if tool_name == "verilator":
        candidates.insert(0, "verilator_bin.exe")

    for candidate in candidates:
        executable = shutil.which(candidate)

        if executable is not None:
            return str(Path(executable).resolve())

    raise ToolchainExecutableNotFoundError(
        tool_name=tool_name,
        stage=stage,
    )