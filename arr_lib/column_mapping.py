import pandas as pd


PREDEFINED_COLUMN_HEADERS = ['customerId', 'contractId', 'contractStartDate', 'contractEndDate', 'totalContractValue']
PREDEFINED_DATE_FORMATS = ['mm/dd/yy', 'dd/mm/yy', 'yyyy/mm/dd']
PREDEFINED_DATE_FORMAT_MAP = {
    'mm/dd/yy': '%m/%d/%y',
    'dd/mm/yy': '%d/%m/%y',
    'yyyy/mm/dd': '%Y/%m/%d'
}


# this version also include the dateformat - and returns dataframe
def map_columns(df, column_mapping_df):
    """
    Map columns in the DataFrame according to the provided mapping.

    Parameters:
    - df (pd.DataFrame): Original DataFrame.
    - column_mapping (dict): Dictionary mapping predefined columns to user-selected columns.

    Returns:
    - pd.DataFrame: DataFrame with columns mapped according to the provided mapping.
    """

    column_mapping = column_mapping_df.set_index('columnHeaders')['columnNames'].to_dict()

    new_df = pd.DataFrame({key: df[value].tolist() for key, value in column_mapping.items()})

    st_format = column_mapping_df.loc[column_mapping_df['columnHeaders']=='contractStartDate', 'dateFormat'].iloc[0]
    end_format =  column_mapping_df.loc[column_mapping_df['columnHeaders'] == 'contractEndDate', 'dateFormat'].iloc[0]

    new_df['startDateFormat'] = st_format
    new_df['endDateFormat'] = end_format

    print(new_df)
    return new_df


# this returns a dictionary and does not include date format
def map_columns_2(df, column_mapping):
    """
    Map columns in the DataFrame according to the provided mapping.

    Parameters:
    - df (pd.DataFrame): Original DataFrame.
    - column_mapping (dict): Dictionary mapping predefined columns to user-selected columns.

    Returns:
    - pd.DataFrame: DataFrame with columns mapped according to the provided mapping.
    """
    print(column_mapping)
    new_df = pd.DataFrame({key: df[value].tolist() for key, value in column_mapping.items()})
    return new_df

