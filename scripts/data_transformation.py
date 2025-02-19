import pandas as pd
import numpy as np

def clean_data(df_bom: pd.DataFrame) -> pd.DataFrame:
    """Transforms column names to lowercase.

    Args:
        df_bom (pd.DataFrame): Data to be transformed.

    Returns:
        pd.DataFrame: Data with column names in lowercase.
    """
    # Transform column names to lowercase
    df_bom.columns = df_bom.columns.str.lower()
    
    return df_bom