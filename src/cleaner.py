import pandas as pd


def clean_dataframe(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """
    Aplica limpieza básica a un DataFrame.

    - Elimina filas duplicadas.
    - Elimina espacios al inicio y final de textos.
    - Conserva los valores nulos.
    - Genera estadísticas de limpieza.
    """

    original_rows = len(df)
    null_values = int(df.isna().sum().sum())

    cleaned = df.copy()

    # Normalizar espacios en columnas de texto.
    for column in cleaned.select_dtypes(include=["object", "string"]).columns:
        cleaned[column] = cleaned[column].map(
            lambda value: value.strip()
            if isinstance(value, str)
            else value
        )

    # Eliminar filas completamente duplicadas.
    cleaned = cleaned.drop_duplicates().reset_index(drop=True)

    stats = {
        "original_rows": original_rows,
        "cleaned_rows": len(cleaned),
        "duplicates_removed": original_rows - len(cleaned),
        "null_values": null_values,
    }

    return cleaned, stats