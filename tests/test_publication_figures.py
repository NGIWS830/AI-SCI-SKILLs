from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "experiment" / "scripts" / "publication_figures.py"


class PublicationFiguresTests(unittest.TestCase):
    def test_dry_run_writes_figure_plan_without_matplotlib(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            csv_path = tmp_path / "results.csv"
            out_dir = tmp_path / "figures"
            csv_path.write_text(
                "Dataset,Method,Acc,F1\nA,Base,90,88\nA,Ours,92,89\n",
                encoding="utf-8",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    str(csv_path),
                    "--target",
                    "Ours",
                    "--metrics",
                    "Acc",
                    "F1",
                    "--higher-better",
                    "Acc",
                    "F1",
                    "--output-dir",
                    str(out_dir),
                    "--dry-run",
                ],
                check=True,
                capture_output=True,
                text=True,
            )

            self.assertIn("figure_plan.md", result.stdout)
            plan = (out_dir / "figure_plan.md").read_text(encoding="utf-8")
            self.assertIn("Grouped bar chart", plan)
            self.assertIn("Improvement heatmap", plan)


if __name__ == "__main__":
    unittest.main()
