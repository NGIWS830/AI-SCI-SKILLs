#!/usr/bin/env python3
"""Package the unified skill as an upload-ready zip archive.

With the v0.2 architecture, there is one root SKILL.md plus four module
directories (digest, literature, experiment, writer). This script packages
the entire suite into a single zip, or optionally packages just a specific
module as a standalone skill.
"""
from __future__ import annotations

import argparse
import zipfile
from pathlib import Path


EXCLUDED_DIRS = {".git", "__pycache__", ".pytest_cache"}
EXCLUDED_SUFFIXES = {".pyc", ".pyo"}


def is_skill_dir(path: Path) -> bool:
    """A skill dir is any directory containing SKILL.md."""
    return path.is_dir() and (path / "SKILL.md").is_file()


def is_module_dir(path: Path) -> bool:
    """A module dir is digest/, literature/, experiment/, or writer/."""
    return path.is_dir() and (path / "references").is_dir()


def iter_files(base: Path):
    """Yield all files under base, excluding build artifacts."""
    for p in sorted(base.rglob("*")):
        if any(part in EXCLUDED_DIRS for part in p.parts):
            continue
        if p.is_file() and p.suffix not in EXCLUDED_SUFFIXES:
            yield p


def package_root_skill(root: Path, output_dir: Path) -> Path:
    """Package the root SKILL.md plus all modules as one skill zip."""
    output_dir.mkdir(parents=True, exist_ok=True)
    archive_path = output_dir / "ai-sci-skills.zip"

    with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for file_path in iter_files(root):
            arcname = file_path.relative_to(root)
            zf.write(file_path, arcname)

    return archive_path


def package_module(root: Path, module_name: str, output_dir: Path) -> Path:
    """Package a single module (digest/literature/experiment/writer) as a standalone zip."""
    module_dir = root / module_name
    if not is_module_dir(module_dir):
        raise SystemExit(f"not a module directory: {module_dir}")

    output_dir.mkdir(parents=True, exist_ok=True)
    archive_path = output_dir / f"ai-sci-{module_name}.zip"

    with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for file_path in iter_files(module_dir):
            zf.write(file_path, file_path.relative_to(module_dir))

    return archive_path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Package the AI-SCI-SKILLs unified skill or individual modules."
    )
    parser.add_argument(
        "--root",
        default=".",
        help="Repository root.",
    )
    parser.add_argument(
        "--output-dir",
        default="dist",
        help="Directory for generated zip files.",
    )
    parser.add_argument(
        "--module",
        choices=["digest", "literature", "experiment", "writer"],
        help="Package only this module instead of the full suite.",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    output_dir = Path(args.output_dir)
    if not output_dir.is_absolute():
        output_dir = root / output_dir

    if args.module:
        archive_path = package_module(root, args.module, output_dir)
    else:
        archive_path = package_root_skill(root, output_dir)

    print(f"wrote {archive_path}")


if __name__ == "__main__":
    main()
