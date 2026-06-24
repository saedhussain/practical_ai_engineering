"""File I/O tools — read and write text files under the outputs/ directory.

Path traversal is rejected at the API boundary — filenames containing '/',
'\\', or '..' are refused. This isn't a hard security boundary, but it
stops the obvious failure mode where a prompt-injected agent tries to write
outside the project's outputs directory.

Tests can override the output directory by passing `output_dir=` to the
underlying underscore-prefixed functions.
"""

from pathlib import Path

from agents import function_tool

from agent_workshop.config import settings


def _is_safe_filename(filename: str) -> bool:
    """Reject filenames that contain path separators or parent traversal."""
    return not ("/" in filename or "\\" in filename or ".." in filename)


def _resolve_output_dir(output_dir: str | None) -> Path:
    """Return the directory to write to, creating it if necessary."""
    target = Path(output_dir) if output_dir is not None else settings.outputs_dir
    target.mkdir(parents=True, exist_ok=True)
    return target


def _write_text_file(
    filename: str,
    content: str,
    output_dir: str | None = None,
) -> str:
    """Save text content to a file under the outputs directory.

    Args:
        filename: file name. Must not contain path separators or '..'.
        content: text to write.
        output_dir: override the default output directory. Used by tests; agents
            should leave this as None.

    Returns:
        A confirmation message including the saved path, or an error message.
    """
    if not filename or not filename.strip():
        return "Error: filename cannot be empty."

    if not _is_safe_filename(filename):
        return (
            f"Error: filename must not contain path separators or '..'. "
            f"Got: {filename!r}."
        )

    target_dir = _resolve_output_dir(output_dir)
    path = target_dir / filename

    try:
        path.write_text(content, encoding="utf-8")
    except OSError as exc:
        return f"Error: could not write {filename}. Reason: {exc}"

    return f"Saved to {path}"


def _read_text_file(
    filename: str,
    output_dir: str | None = None,
) -> str:
    """Read a text file from the outputs directory.

    Args:
        filename: file name. Must not contain path separators or '..'.
        output_dir: override the default output directory. Used by tests.

    Returns:
        The file's contents, or an error message including what files do exist.
    """
    if not filename or not filename.strip():
        return "Error: filename cannot be empty."

    if not _is_safe_filename(filename):
        return (
            f"Error: filename must not contain path separators or '..'. "
            f"Got: {filename!r}."
        )

    target_dir = _resolve_output_dir(output_dir)
    path = target_dir / filename

    if not path.exists():
        available = sorted(p.name for p in target_dir.iterdir() if p.is_file())
        available_str = ", ".join(available) if available else "no files yet"
        return (
            f"Error: file {filename!r} not found in {target_dir}. "
            f"Available files: {available_str}."
        )

    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        return f"Error: could not read {filename}. Reason: {exc}"


# Agent-facing wrappers.
write_text_file = function_tool(_write_text_file)
read_text_file = function_tool(_read_text_file)
