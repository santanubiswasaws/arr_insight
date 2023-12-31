import pandas as pd

def map_columns(df, column_mapping):
    """
    Map columns in the DataFrame according to the provided mapping.

    Parameters:
    - df (pd.DataFrame): Original DataFrame.
    - column_mapping (dict): Dictionary mapping predefined columns to user-selected columns.

    Returns:
    - pd.DataFrame: DataFrame with columns mapped according to the provided mapping.
    """
    new_df = pd.DataFrame({key: df[value].tolist() for key, value in column_mapping.items()})
    return new_df
