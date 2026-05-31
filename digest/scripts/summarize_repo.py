#!/usr/bin/env python3
"""Create a lightweight inventory of an AI project repository.

Usage:
    python summarize_repo.py /path/to/repo --output repo_inventory.md
"""
from __future__ import annotations
import argparse
from pathlib import Path

DEFAULT_IGNORE = {'.git', '__pycache__', '.ipynb_checkpoints', 'wandb', 'runs', 'checkpoints', 'outputs', 'dist', 'build'}
IMPORTANT_SUFFIXES = {'.py', '.ipynb', '.yaml', '.yml', '.json', '.toml', '.md', '.txt', '.csv', '.tsv'}
IMPORTANT_NAMES = {'README.md', 'requirements.txt', 'environment.yml', 'pyproject.toml'}

def iter_files(root: Path, max_files: int = 500):
    count = 0
    for p in sorted(root.rglob('*')):
        if count >= max_files:
            break
        if any(part in DEFAULT_IGNORE for part in p.parts):
            continue
        if p.is_file() and (p.suffix.lower() in IMPORTANT_SUFFIXES or p.name in IMPORTANT_NAMES):
            count += 1
            yield p

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('repo')
    parser.add_argument('--output', default='repo_inventory.md')
    args = parser.parse_args()
    root = Path(args.repo).resolve()
    if not root.exists() or not root.is_dir():
        raise SystemExit(f'not a directory: {root}')
    lines = ['# Repository Inventory', '', f'Root: `{root}`', '']
    groups = {}
    for p in iter_files(root):
        rel = p.relative_to(root)
        key = rel.parts[0] if len(rel.parts) > 1 else '.'
        groups.setdefault(key, []).append(rel)
    for key, files in sorted(groups.items()):
        lines.append(f'## {key}')
        for rel in files[:80]:
            lines.append(f'- `{rel}`')
        if len(files) > 80:
            lines.append(f'- ... {len(files)-80} more')
        lines.append('')
    Path(args.output).write_text('\n'.join(lines), encoding='utf-8')
    print(f'wrote {args.output}')

if __name__ == '__main__':
    main()
