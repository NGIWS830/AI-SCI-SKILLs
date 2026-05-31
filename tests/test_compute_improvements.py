from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "experiment" / "scripts" / "compute_improvements.py"


class ComputeImprovementsTests(unittest.TestCase):
    def run_script(self, csv_text: str, *args: str) -> str:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            csv_path = tmp_path / "results.csv"
            output_path = tmp_path / "improvements.md"
            csv_path.write_text(csv_text, encoding="utf-8")

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    str(csv_path),
                    "--output",
                    str(output_path),
                    *args,
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertIn("wrote", result.stdout)
            return output_path.read_text(encoding="utf-8")

    def test_global_higher_better_metric(self):
        output = self.run_script(
            "Method,Acc,F1\nBaseA,90,88\nBaseB,91,89\nOurs,93,90\n",
            "--target",
            "Ours",
            "--metrics",
            "Acc",
            "F1",
            "--higher-better",
            "Acc",
            "F1",
        )

        self.assertIn("| all | Acc | higher | 93 | BaseB | 91 | 2 | 2.20% |", output)
        self.assertIn("| all | F1 | higher | 90 | BaseB | 89 | 1 | 1.12% |", output)

    def test_grouped_mixed_metric_directions(self):
        output = self.run_script(
            "\n".join(
                [
                    "Dataset,Method,Acc,Params",
                    "A,BaseA,90,12",
                    "A,BaseB,91,15",
                    "A,Ours,93,10",
                    "B,BaseA,80,8",
                    "B,Ours,82,7",
                ]
            ),
            "--target",
            "Ours",
            "--metrics",
            "Acc",
            "Params",
            "--higher-better",
            "Acc",
            "--lower-better",
            "Params",
            "--group-cols",
            "Dataset",
        )

        self.assertIn("| Dataset=A | Acc | higher | 93 | BaseB | 91 | 2 | 2.20% |", output)
        self.assertIn("| Dataset=A | Params | lower | 10 | BaseA | 12 | 2 | 16.67% |", output)
        self.assertIn("| Dataset=B | Acc | higher | 82 | BaseA | 80 | 2 | 2.50% |", output)
        self.assertIn("| Dataset=B | Params | lower | 7 | BaseA | 8 | 1 | 12.50% |", output)

    def test_baseline_method_filter(self):
        output = self.run_script(
            "Method,Acc\nBaseA,90\nBaseB,95\nOurs,96\n",
            "--target",
            "Ours",
            "--metrics",
            "Acc",
            "--higher-better",
            "Acc",
            "--baseline-methods",
            "BaseA",
        )

        self.assertIn("| all | Acc | higher | 96 | BaseA | 90 | 6 | 6.67% |", output)
        self.assertNotIn("BaseB | 95", output)


if __name__ == "__main__":
    unittest.main()
