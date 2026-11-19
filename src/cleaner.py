import pandas as pd


def clean_dataframe(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Limpia un DataFrame y devuelve estadísticas del proceso."""

    cleaned = df.copy()
    original_rows = len(cleaned)
    original_nulls = int(cleaned.isna().sum().sum())

    # Normalizar columnas de texto
    for column in cleaned.select_dtypes(include=["object", "string"]).columns:

        cleaned[column] = cleaned[column].map(
            lambda value: " ".join(value.split())
            if isinstance(value, str)
            else value
        )

        # Reconocer valores nulos escritos como texto
        cleaned[column] = cleaned[column].replace(
            ["", "N/A", "n/a", "NULL", "null", "None"],
            pd.NA
        )

    # Eliminar duplicados exactos después de normalizar
    cleaned = cleaned.drop_duplicates().reset_index(drop=True)

    stats = {
        "original_rows": original_rows,
        "cleaned_rows": len(cleaned),
        "duplicates_removed": original_rows - len(cleaned),
        "original_nulls": original_nulls,
        "final_nulls": int(cleaned.isna().sum().sum()),
    }

    return cleaned, stats