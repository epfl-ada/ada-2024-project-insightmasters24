import pandas as pd


def reorder_column(df: pd.DataFrame, col_name: str, index: int) -> pd.DataFrame:
    """Move a column to the specified position in a dataframe"""
    cols = df.columns.tolist()
    cols.remove(col_name)
    cols.insert(index, col_name)
    return df[cols]
