from pathlib import Path
import time

import pandas as pd

from src.cleaner import clean_dataframe


SUPPORTED_EXTENSIONS = {".csv", ".xlsx"}


def process_file(file_path: Path, output_dir: Path) -> dict:
    """
    Lee, limpia y guarda un archivo CSV o XLSX.
    """

    start = time.perf_counter()

    output_dir.mkdir(parents=True, exist_ok=True)

    if file_path.suffix.lower() == ".csv":
        df = pd.read_csv(file_path)

    elif file_path.suffix.lower() == ".xlsx":
        df = pd.read_excel(file_path)

    else:
        raise ValueError(f"Formato no compatible: {file_path.suffix}")

    cleaned, stats = clean_dataframe(df)

    output_path = output_dir / file_path.name

    if file_path.suffix.lower() == ".csv":
        cleaned.to_csv(output_path, index=False)

    else:
        cleaned.to_excel(output_path, index=False)

    elapsed = time.perf_counter() - start

    return {
        "file": file_path.name,
        **stats,
        "time_seconds": round(elapsed, 4),
        "status": "OK",
    }


def run_sequential(input_dir: Path, output_dir: Path) -> list[dict]:
    """
    Procesa secuencialmente todos los CSV y XLSX.
    """

    files = sorted(
        file
        for file in input_dir.iterdir()
        if file.is_file()
        and file.suffix.lower() in SUPPORTED_EXTENSIONS
        and not file.name.startswith("~$")
    )

    results = []

    for file in files:
        print(f"Procesando: {file.name}")

        try:
            result = process_file(file, output_dir)
            results.append(result)

        except Exception as error:
            print(f"Error en {file.name}: {error}")

            results.append({
                "file": file.name,
                "status": "ERROR",
                "error": str(error),
            })

    return results