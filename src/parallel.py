from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed

from src.sequential import process_file, SUPPORTED_EXTENSIONS


def run_parallel(
    input_dir: Path,
    output_dir: Path,
    workers: int = 4
) -> list[dict]:

    """
    Procesa archivos utilizando múltiples procesos.
    """

    files = sorted(
        file
        for file in input_dir.iterdir()
        if file.is_file()
        and file.suffix.lower() in SUPPORTED_EXTENSIONS
        and not file.name.startswith("~$")
    )

    results = []

    with ProcessPoolExecutor(max_workers=workers) as executor:

        futures = {
            executor.submit(process_file, file, output_dir): file
            for file in files
        }

        for future in as_completed(futures):

            file = futures[future]

            try:
                result = future.result()
                results.append(result)

                print(f"Completado: {file.name}")

            except Exception as error:
                print(f"Error en {file.name}: {error}")

                results.append({
                    "file": file.name,
                    "status": "ERROR",
                    "error": str(error),
                })

    return sorted(results, key=lambda item: item["file"])