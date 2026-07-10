from functools import lru_cache
from pathlib import Path

__all__ = ["get_prompt"]


def _get_templates_dir() -> Path:
    """Return the directory containing prompt templates."""
    return Path(__file__).resolve().parent / "templates"


@lru_cache(maxsize=None)
def _load_prompt(name: str) -> str:
    """Load a prompt template from disk."""
    prompt_path = _get_templates_dir() / f"{name}.txt"

    if not prompt_path.exists():
        raise FileNotFoundError(
            f"Prompt template '{name}.txt' was not found in "
            f"'{_get_templates_dir()}'."
        )

    prompt = prompt_path.read_text(encoding="utf-8")

    if not prompt.strip():
        raise ValueError(f"Prompt template '{name}.txt' is empty.")

    return prompt

def get_prompt(name: str) -> str:
    """Return the requested prompt template."""
    return _load_prompt(name)