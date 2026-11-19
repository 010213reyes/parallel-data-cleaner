from pathlib import Path
import time

import pandas as pd

from src.sequential import run_sequential
from src.threaded import run_threaded
from src.parallel import run_parallel


INPUT_DIR = Path("data/raw")
OUTPUT_DIR = Path("data/cleaned")
REPORT_DIR = Path("reports")


def main():

    print("=" * 45)
    print("       PARALLEL DATA CLEANER")
    print("=" * 45)

    INPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    print("\nSelecciona el modo de procesamiento:\n")
    print("1. Secuencial")
    print("2. Hilos")
    print("3. Procesos")

    option = input("\nOpción: ").strip()

    modes = {
        "1": ("secuencial", run_sequential),
        "2": ("hilos", run_threaded),
        "3": ("procesos", run_parallel),
    }

    if option not in modes:
        print("Opción no válida.")
        return

    mode_name, processor = modes[option]

    print(f"\nModo seleccionado: {mode_name.upper()}\n")

    start = time.perf_counter()

    results = processor(INPUT_DIR, OUTPUT_DIR)

    elapsed = time.perf_counter() - start

    if not results:
        print("No se encontraron archivos CSV o XLSX.")
        return

    report = pd.DataFrame(results)

    report_path = REPORT_DIR / f"reporte_{mode_name}.csv"
    report.to_csv(report_path, index=False)

    successful = sum(
        result["status"] == "OK"
        for result in results
    )

    print("\n" + "=" * 45)
    print("RESUMEN DEL PROCESAMIENTO")
    print("=" * 45)

    print(f"Modo: {mode_name}")
    print(f"Archivos encontrados: {len(results)}")
    print(f"Archivos procesados: {successful}")
    print(f"Archivos con error: {len(results) - successful}")
    print(f"Tiempo total: {elapsed:.4f} segundos")

    print(f"\nReporte guardado en: {report_path}")
    print(f"Archivos limpios en: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()