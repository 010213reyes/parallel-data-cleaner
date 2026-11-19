
import csv
import os
import platform
import statistics
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.sequential import run_sequential
from src.threaded import run_threaded
from src.parallel import run_parallel


SCENARIOS = ["pequeno", "mediano", "grande"]
WORKERS = [1, 2, 4]
REPETITIONS = 5

METHODS = {
    "secuencial": run_sequential,
    "hilos": run_threaded,
    "procesos": run_parallel,
}


def execute(processor, input_dir, workers=None):
    with tempfile.TemporaryDirectory() as temporary:
        output_dir = Path(temporary) / "cleaned"
        output_dir.mkdir()

        start = time.perf_counter()

        if workers is None:
            results = processor(input_dir, output_dir)
        else:
            results = processor(
                input_dir,
                output_dir,
                workers=workers,
            )

        elapsed = time.perf_counter() - start

        expected_files = len(list(input_dir.glob("*.csv")))

        if len(results) != expected_files:
            raise RuntimeError(
                "La cantidad de archivos procesados no coincide."
            )

        if any(result["status"] != "OK" for result in results):
            raise RuntimeError(
                "Se detectaron errores durante el procesamiento."
            )

        output_files = list(output_dir.glob("*.csv"))

        if len(output_files) != expected_files:
            raise RuntimeError(
                "La cantidad de archivos de salida no coincide."
            )

        return elapsed


def main():
    reports_dir = ROOT / "reports"
    reports_dir.mkdir(exist_ok=True)

    raw_records = []
    summary_records = []

    print("=" * 55)
    print("PARALLEL DATA CLEANER - BENCHMARKS")
    print("=" * 55)

    print(f"Sistema operativo: {platform.platform()}")
    print(f"Python: {platform.python_version()}")
    print(f"Procesadores logicos: {os.cpu_count()}")
    print(f"Repeticiones: {REPETITIONS}")

    for scenario in SCENARIOS:
        input_dir = ROOT / "data" / "benchmarks" / scenario

        if not input_dir.exists():
            raise FileNotFoundError(
                f"No existe el escenario: {input_dir}"
            )

        file_count = len(list(input_dir.glob("*.csv")))

        print(f"\nESCENARIO: {scenario.upper()}")
        print(f"Archivos: {file_count}")

        configurations = [("secuencial", None)]

        for method in ["hilos", "procesos"]:
            for workers in WORKERS:
                configurations.append((method, workers))

        measurements = {}

        for method, workers in configurations:
            processor = METHODS[method]
            label = (
                method if workers is None
                else f"{method} ({workers} workers)"
            )

            # Calentamiento: no se registra.
            execute(processor, input_dir, workers)

            times = []

            for repetition in range(1, REPETITIONS + 1):
                elapsed = execute(
                    processor,
                    input_dir,
                    workers,
                )

                times.append(elapsed)

                raw_records.append({
                    "escenario": scenario,
                    "metodo": method,
                    "workers": workers or 1,
                    "repeticion": repetition,
                    "tiempo_segundos": elapsed,
                })

            measurements[(method, workers)] = times

            print(
                f"{label}: "
                f"mediana={statistics.median(times):.4f}s"
            )

        baseline = statistics.median(
            measurements[("secuencial", None)]
        )

        for (method, workers), times in measurements.items():
            median_time = statistics.median(times)

            speedup = baseline / median_time

            efficiency = (
                1.0 if method == "secuencial"
                else speedup / workers
            )

            summary_records.append({
                "escenario": scenario,
                "metodo": method,
                "workers": workers or 1,
                "mediana_segundos": median_time,
                "promedio_segundos": statistics.mean(times),
                "desviacion_segundos": statistics.stdev(times),
                "speedup": speedup,
                "eficiencia": efficiency,
                "archivos_por_segundo": file_count / median_time,
            })

    raw_path = reports_dir / "benchmark_raw.csv"
    summary_path = reports_dir / "benchmark_summary.csv"

    pd_fields = [
        "escenario", "metodo", "workers",
        "repeticion", "tiempo_segundos",
    ]

    summary_fields = [
        "escenario", "metodo", "workers",
        "mediana_segundos", "promedio_segundos",
        "desviacion_segundos", "speedup",
        "eficiencia", "archivos_por_segundo",
    ]

    with raw_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=pd_fields)
        writer.writeheader()
        writer.writerows(raw_records)

    with summary_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=summary_fields)
        writer.writeheader()
        writer.writerows(summary_records)

    print("\nBENCHMARKS FINALIZADOS")
    print(f"Mediciones: {len(raw_records)}")
    print(f"Datos crudos: {raw_path}")
    print(f"Resumen: {summary_path}")


if __name__ == "__main__":
    main()
