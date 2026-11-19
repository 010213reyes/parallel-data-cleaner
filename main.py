from pathlib import Path
import time

import pandas as pd

from src.sequential import run_sequential


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

    print("\nModo de procesamiento: SECUENCIAL\n")

    start = time.perf_counter()

    results = run_sequential(INPUT_DIR, OUTPUT_DIR)

    elapsed = time.perf_counter() - start

    if not results:
        print("No se encontraron archivos CSV o XLSX.")
        return

    report = pd.DataFrame(results)

    report_path = REPORT_DIR / "reporte_secuencial.csv"
    report.to_csv(report_path, index=False)

    successful = sum(
        result["status"] == "OK"
        for result in results
    )

    print("\n" + "=" * 45)
    print("RESUMEN DEL PROCESAMIENTO")
    print("=" * 45)

    print(f"Archivos encontrados: {len(results)}")
    print(f"Archivos procesados: {successful}")
    print(f"Archivos con error: {len(results) - successful}")
    print(f"Tiempo total: {elapsed:.4f} segundos")

    print(f"\nReporte guardado en: {report_path}")
    print(f"Archivos limpios en: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()