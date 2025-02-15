import pandas as pd
import numpy as np

def clean_data(df_bom: pd.DataFrame) -> pd.DataFrame:
    """Limpa e transforma os dados para adequação ao modelo.

    Args:
        engine: Conexão ao banco de dados.
        df_bom (pd.DataFrame): Dados a serem limpos.

    Returns:
        pd.DataFrame: Dados limpos e transformados.
    """
    # Transformar os nomes das colunas para minúsculas
    df_bom.columns = df_bom.columns.str.lower()
    
    # Converter todas as colunas para string, exceto colunas numéricas conhecidas
    # for col in df_bom.columns:
    #     if col in ['qpa']:  # Adicione aqui outras colunas numéricas se necessário
    #         df_bom[col] = pd.to_numeric(df_bom[col], errors='coerce')
    #     else:
    #         df_bom[col] = df_bom[col].astype(str)
    
    return df_bom
