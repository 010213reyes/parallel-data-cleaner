
from pathlib import Path
import random

import pandas as pd


SCENARIOS = {
    "pequeno": (5, 1000),
    "mediano": (20, 5000),
    "grande": (50, 10000),
}


def generate_dataset(destination, file_count, row_count):
    destination.mkdir(parents=True, exist_ok=True)

    for old_file in destination.glob("*.csv"):
        old_file.unlink()

    for number in range(file_count):
        rng = random.Random(42 + number)

        records = []

        for index in range(row_count):
            records.append({
                "id": index,
                "nombre": rng.choice(
                    [" Ana ", "Luis", " Maria  ", "Pedro", None]
                ),
                "edad": rng.randint(18, 70),
                "ciudad": rng.choice(
                    [" Guadalajara ", "Monterrey", "CDMX", None]
                ),
                "venta": round(rng.uniform(100, 5000), 2),
            })

        # Agregar duplicados exactos.
        records.extend(records[:100])

        dataframe = pd.DataFrame(records)

        dataframe.to_csv(
            destination / f"datos_{number:03d}.csv",
            index=False,
        )


def main():
    base = Path("data/benchmarks")

    for name, (file_count, row_count) in SCENARIOS.items():
        generate_dataset(
            base / name,
            file_count,
            row_count,
        )

        print(
            f"{name}: {file_count} archivos, "
            f"{row_count} filas base por archivo"
        )


if __name__ == "__main__":
    main()
