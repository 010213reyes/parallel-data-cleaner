
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"

SCENARIOS = ["pequeno", "mediano", "grande"]

CONFIGURATIONS = [
    "Secuencial",
    "Hilos (1)",
    "Hilos (2)",
    "Hilos (4)",
    "Procesos (1)",
    "Procesos (2)",
    "Procesos (4)",
]


def create_plot(df, metric, title, ylabel, filename):
    table = df.pivot(
        index="escenario",
        columns="configuracion",
        values=metric,
    )

    table = table.reindex(
        index=SCENARIOS,
        columns=CONFIGURATIONS,
    )

    ax = table.plot(
        kind="bar",
        figsize=(12, 6),
        rot=0,
    )

    ax.set_title(title)
    ax.set_xlabel("Escenario")
    ax.set_ylabel(ylabel)
    ax.legend(title="Configuracion")
    ax.grid(axis="y", alpha=0.25)

    if metric == "speedup":
        ax.axhline(
            y=1,
            linestyle="--",
            color="black",
            linewidth=1,
        )

    plt.tight_layout()

    destination = REPORTS / filename

    plt.savefig(destination, dpi=150)
    plt.close()

    print(f"Grafica generada: {destination}")


def main():
    df = pd.read_csv(
        REPORTS / "benchmark_summary.csv"
    )

    df["configuracion"] = df.apply(
        lambda row: (
            "Secuencial"
            if row["metodo"] == "secuencial"
            else f"{row['metodo'].capitalize()} ({row['workers']})"
        ),
        axis=1,
    )

    create_plot(
        df,
        "mediana_segundos",
        "Parallel Data Cleaner - Tiempo de ejecucion",
        "Tiempo mediano (segundos)",
        "benchmark_comparison.png",
    )

    create_plot(
        df,
        "speedup",
        "Parallel Data Cleaner - Speedup",
        "Speedup",
        "benchmark_speedup.png",
    )

    create_plot(
        df,
        "eficiencia",
        "Parallel Data Cleaner - Eficiencia relativa",
        "Eficiencia",
        "benchmark_efficiency.png",
    )

    print("\nGRAFICAS GENERADAS CORRECTAMENTE")


if __name__ == "__main__":
    main()
