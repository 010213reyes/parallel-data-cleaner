
import hashlib
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.sequential import run_sequential
from src.threaded import run_threaded
from src.parallel import run_parallel


SCENARIOS = {
    "pequeno": 5,
    "mediano": 20,
    "grande": 50,
}

WORKERS = [1, 2, 4]


def file_hash(path):
    digest = hashlib.sha256()

    with path.open("rb") as file:
        for block in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(block)

    return digest.hexdigest()


def execute(processor, input_dir, output_dir, workers=None):
    output_dir.mkdir(parents=True, exist_ok=True)

    if workers is None:
        results = processor(input_dir, output_dir)
    else:
        results = processor(
            input_dir,
            output_dir,
            workers=workers,
        )

    expected = {
        file.name for file in input_dir.glob("*.csv")
    }

    if len(results) != len(expected):
        raise AssertionError("Cantidad incorrecta de resultados")

    if any(result["status"] != "OK" for result in results):
        raise RuntimeError("Error durante el procesamiento")

    outputs = {
        file.name: file_hash(file)
        for file in output_dir.glob("*.csv")
    }

    if set(outputs) != expected:
        raise AssertionError("Archivos faltantes o adicionales")

    return outputs


def main():
    validations = 0

    for scenario, expected_count in SCENARIOS.items():
        input_dir = ROOT / "data" / "benchmarks" / scenario

        if len(list(input_dir.glob("*.csv"))) != expected_count:
            raise AssertionError(
                f"Dataset incompleto: {scenario}"
            )

        print(f"\nESCENARIO: {scenario.upper()}")

        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)

            reference = execute(
                run_sequential,
                input_dir,
                base / "secuencial",
            )

            methods = {
                "hilos": run_threaded,
                "procesos": run_parallel,
            }

            for name, processor in methods.items():
                for workers in WORKERS:
                    outputs = execute(
                        processor,
                        input_dir,
                        base / f"{name}_{workers}",
                        workers,
                    )

                    if outputs != reference:
                        raise AssertionError(
                            f"Resultados diferentes: "
                            f"{scenario}, {name}, {workers}"
                        )

                    validations += 1

                    print(
                        f"PASS: {name} ({workers} workers) - "
                        f"{len(outputs)} archivos equivalentes"
                    )

    print("\n" + "=" * 50)
    print("VALIDACION FINAL EXITOSA")
    print(f"Configuraciones verificadas: {validations}/18")
    print("=" * 50)


if __name__ == "__main__":
    main()
