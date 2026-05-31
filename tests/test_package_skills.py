from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "package_skills.py"


class PackageFullSuiteTests(unittest.TestCase):
    def test_packages_root_skill_with_all_modules(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "SKILL.md").write_text(
                "---\nname: test-skill\n---\n# Test\n",
                encoding="utf-8",
            )
            # Create a module directory
            digest = root / "digest"
            (digest / "references").mkdir(parents=True)
            (digest / "references" / "guide.md").write_text("# Guide\n", encoding="utf-8")
            (digest / "__pycache__").mkdir()
            (digest / "__pycache__" / "ignored.pyc").write_bytes(b"x")

            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--root", str(root), "--output-dir", "dist"],
                check=True,
                capture_output=True,
                text=True,
            )

            self.assertIn("ai-sci-skills.zip", result.stdout)
            archive = root / "dist" / "ai-sci-skills.zip"
            self.assertTrue(archive.is_file())
            with zipfile.ZipFile(archive) as zf:
                names = set(zf.namelist())
            self.assertIn("SKILL.md", names)
            self.assertIn("digest/references/guide.md", names)
            self.assertNotIn("__pycache__/ignored.pyc", names)
            # Relative paths, not absolute
            for name in names:
                self.assertFalse(name.startswith("/") or name.startswith("\\"))


class PackageModuleTests(unittest.TestCase):
    def test_packages_single_module(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            module = root / "experiment"
            (module / "references").mkdir(parents=True)
            (module / "references" / "guide.md").write_text("# Exp Guide\n", encoding="utf-8")
            (module / "__pycache__").mkdir()
            (module / "__pycache__" / "ignored.pyc").write_bytes(b"x")

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--root",
                    str(root),
                    "--module",
                    "experiment",
                    "--output-dir",
                    "dist",
                ],
                check=True,
                capture_output=True,
                text=True,
            )

            self.assertIn("ai-sci-experiment.zip", result.stdout)
            archive = root / "dist" / "ai-sci-experiment.zip"
            self.assertTrue(archive.is_file())
            with zipfile.ZipFile(archive) as zf:
                names = set(zf.namelist())
            self.assertIn("references/guide.md", names)
            self.assertNotIn("__pycache__/ignored.pyc", names)


class BadModuleTests(unittest.TestCase):
    def test_invalid_module_name_exits_with_error(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--module", "nonexistent"],
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
