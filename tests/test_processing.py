import tempfile
import unittest
from pathlib import Path

import pandas as pd

from src.sequential import run_sequential
from src.threaded import run_threaded
from src.parallel import run_parallel


class TestProcessing(unittest.TestCase):

    def test_processing_equivalence(self):

        with tempfile.TemporaryDirectory() as temp:

            base = Path(temp)
            input_dir = base / "raw"
            input_dir.mkdir()

            # Crear archivos de prueba.
            for number in range(3):

                df = pd.DataFrame({
                    "nombre": [" Ana ", "Ana", "Luis"],
                    "venta": [100, 100, 200],
                })

                df.to_csv(
                    input_dir / f"ventas_{number}.csv",
                    index=False
                )

            outputs = {}

            processors = {
                "secuencial": run_sequential,
                "hilos": run_threaded,
                "procesos": run_parallel,
            }

            for name, processor in processors.items():

                output_dir = base / name

                results = processor(input_dir, output_dir)

                self.assertEqual(len(results), 3)
                self.assertTrue(
                    all(result["status"] == "OK" for result in results)
                )

                outputs[name] = {
                    file.name: pd.read_csv(file)
                    for file in output_dir.glob("*.csv")
                }

            # Comparar los resultados de las tres versiones.
            reference = outputs["secuencial"]

            for mode in ["hilos", "procesos"]:

                self.assertEqual(
                    set(reference),
                    set(outputs[mode])
                )

                for filename in reference:

                    pd.testing.assert_frame_equal(
                        reference[filename],
                        outputs[mode][filename]
                    )


if __name__ == "__main__":
    unittest.main()