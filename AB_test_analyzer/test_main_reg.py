import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent


class TestMainOutput(unittest.TestCase):

    def test_output(self) -> None:
        result = subprocess.run(
            [sys.executable, str(ROOT / "main.py")],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True
        )

        expected = (
            ROOT / "expected_output.txt"
        ).read_text(encoding="utf-8")

        self.assertEqual(result.stdout, expected)


if __name__ == "__main__":
    unittest.main()
