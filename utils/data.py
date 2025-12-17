import duckdb
import pandas as pd
from pathlib import Path


def load_data(filepath: str | Path) -> pd.DataFrame:
    """
    Charge les données depuis un fichier Parquet.
    
    Utilise DuckDB pour des performances optimales.
    """
    con = duckdb.connect()
    df = con.execute(f"SELECT * FROM read_parquet('{filepath}')").df()
    con.close()
    return df


def get_data_summary(df: pd.DataFrame) -> dict:
    """Retourne un résumé des données pour le contexte."""
    return {
        "rows": len(df),
        "columns": list(df.columns),
        "dtypes": df.dtypes.to_dict(),
        "sample": df.head(5).to_dict()
    }


def filter_data(df: pd.DataFrame, filters: dict) -> pd.DataFrame:
    """
    Applique des filtres au DataFrame.
    
    Args:
        df: DataFrame source
        filters: Dict de {colonne: valeur ou liste de valeurs}
    
    Returns:
        DataFrame filtré
    """
    df_filtered = df.copy()
    
    for col, value in filters.items():
        if col not in df_filtered.columns:
            continue
        if isinstance(value, list):
            df_filtered = df_filtered[df_filtered[col].isin(value)]
        else:
            df_filtered = df_filtered[df_filtered[col] == value]
    
    return df_filtered