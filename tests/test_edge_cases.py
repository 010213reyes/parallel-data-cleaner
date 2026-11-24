
import tempfile
import unittest
from pathlib import Path

import pandas as pd

from src.sequential import run_sequential
from src.threaded import run_threaded
from src.parallel import run_parallel


class TestEdgeCases(unittest.TestCase):

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)

        self.input_dir = self.root / "input"
        self.input_dir.mkdir()

        self.methods = {
            "secuencial": run_sequential,
            "hilos": run_threaded,
            "procesos": run_parallel,
        }

    def tearDown(self):
        self.temporary.cleanup()

    def execute(self, method):
        output_dir = self.root / method
        output_dir.mkdir(exist_ok=True)

        results = self.methods[method](
            self.input_dir,
            output_dir,
        )

        return results, output_dir

    def test_empty_directory(self):
        for method in self.methods:
            with self.subTest(method=method):
                results, output = self.execute(method)

                self.assertEqual(len(results), 0)
                self.assertEqual(len(list(output.iterdir())), 0)

    def test_header_only_csv(self):
        pd.DataFrame(
            columns=["nombre", "venta"]
        ).to_csv(
            self.input_dir / "empty.csv",
            index=False,
        )

        for method in self.methods:
            with self.subTest(method=method):
                results, output = self.execute(method)

                self.assertEqual(results[0]["status"], "OK")

                cleaned = pd.read_csv(output / "empty.csv")

                self.assertTrue(cleaned.empty)
                self.assertEqual(
                    list(cleaned.columns),
                    ["nombre", "venta"],
                )

    def test_excel_processing(self):
        original = pd.DataFrame({
            "nombre": [" Ana ", " Ana ", "Luis"],
            "venta": [100, 100, 200],
        })

        original.to_excel(
            self.input_dir / "ventas.xlsx",
            index=False,
        )

        expected = pd.DataFrame({
            "nombre": ["Ana", "Luis"],
            "venta": [100, 200],
        })

        for method in self.methods:
            with self.subTest(method=method):
                results, output = self.execute(method)

                self.assertEqual(results[0]["status"], "OK")

                cleaned = pd.read_excel(
                    output / "ventas.xlsx"
                )

                pd.testing.assert_frame_equal(
                    cleaned,
                    expected,
                )

    def test_corrupted_file(self):
        (self.input_dir / "corrupto.xlsx").write_text(
            "Archivo Excel invalido",
            encoding="utf-8",
        )

        pd.DataFrame({
            "nombre": ["Ana"],
            "venta": [100],
        }).to_csv(
            self.input_dir / "valido.csv",
            index=False,
        )

        for method in self.methods:
            with self.subTest(method=method):
                results, output = self.execute(method)

                statuses = {
                    result["file"]: result["status"]
                    for result in results
                }

                self.assertEqual(
                    statuses["corrupto.xlsx"],
                    "ERROR",
                )

                self.assertEqual(
                    statuses["valido.csv"],
                    "OK",
                )

                self.assertTrue(
                    (output / "valido.csv").exists()
                )


if __name__ == "__main__":
    unittest.main()
