"""Tests for the file I/O tools.

Uses pytest's tmp_path fixture so each test gets a clean directory
and tests don't interfere with each other or with the project's
outputs/ folder.
"""

from agent_workshop.tools.files import _read_text_file, _write_text_file


def test_writes_and_reads_file(tmp_path):
    write_result = _write_text_file(
        "note.md",
        "hello, workshop",
        output_dir=str(tmp_path),
    )
    assert write_result.startswith("Saved to")

    read_result = _read_text_file("note.md", output_dir=str(tmp_path))
    assert read_result == "hello, workshop"


def test_creates_output_dir_if_missing(tmp_path):
    target = tmp_path / "nested" / "outputs"
    assert not target.exists()

    _write_text_file("file.md", "content", output_dir=str(target))
    assert target.exists()


def test_rejects_path_separators(tmp_path):
    result = _write_text_file(
        "sub/note.md", "x", output_dir=str(tmp_path)
    )
    assert result.startswith("Error:")
    assert "path separator" in result.lower() or "'..'" in result


def test_rejects_parent_traversal(tmp_path):
    result = _write_text_file(
        "../secret.md", "x", output_dir=str(tmp_path)
    )
    assert result.startswith("Error:")


def test_missing_file_lists_what_is_available(tmp_path):
    _write_text_file("real.md", "content", output_dir=str(tmp_path))

    result = _read_text_file("missing.md", output_dir=str(tmp_path))
    assert result.startswith("Error:")
    assert "real.md" in result    # error mentions what IS available


def test_overwrites_existing_file(tmp_path):
    _write_text_file("note.md", "first", output_dir=str(tmp_path))
    _write_text_file("note.md", "second", output_dir=str(tmp_path))

    assert _read_text_file("note.md", output_dir=str(tmp_path)) == "second"


def test_empty_filename_rejected(tmp_path):
    result = _write_text_file("", "content", output_dir=str(tmp_path))
    assert result.startswith("Error:")
    assert "empty" in result.lower()
