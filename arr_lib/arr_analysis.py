import pandas as pd
from datetime import datetime

def create_monthly_buckets(df):
    """
    Process uploaded contract data 
        1. Validates all the columns 
        2. Breaks the uploaded records into monthly value - based on the contract lenght - create one row per month 
        3. Assigns the monthly monthlyRevenue amount for each month 

    Parameters:
    - df (pd.DataFrame): Original contract data DataFrame.

    Returns:
    - pd.DataFrame: Processed DataFrame one row for each month - for the customer and contract 
    """
    # Check if the required columns are present
    required_columns = ['customerId', 'contractId', 'contractStartDate', 'contractEndDate', 'totalContractValue']
    if not all(col in df.columns for col in required_columns):
        raise ValueError("Columns 'customerId', 'contractId', 'contractStartDate', 'contractEndDate', and 'totalContractValue' are required in the DataFrame.")

    # Validate date formats in 'contractStartDate' and 'contractEndDate'
    try:
        df['contractStartDate'] = pd.to_datetime(df['contractStartDate'], format='%m/%d/%y')
        df['contractEndDate'] = pd.to_datetime(df['contractEndDate'], format='%m/%d/%y')
    except ValueError:
        raise ValueError("Invalid date format in 'contractStartDate' or 'contractEndDate'. Use 'mm/dd/yy' format.")

    # Calculate the contract duration in months
    df['contractDuration'] = (df['contractEndDate'] - df['contractStartDate']).dt.days 

    # Validate contract duration
    valid_contract_duration = df['contractDuration'] > 0
    if not valid_contract_duration.all():
        raise ValueError("Invalid contract duration. 'contractEndDate' should be later than 'contractStartDate'.")
    
    # Validate contract value column
    if not pd.to_numeric(df['totalContractValue'], errors='coerce').notna().all():
        raise ValueError("Invalid 'totalContractValue'. It must contain numeric values.")
    
    # Drop a specific column contractDuration - it will be recalculated
    df = df.drop('contractDuration', axis=1)

    # In line function - Function to calculate total months and monthly contract value
    def calculate_months_and_value(row):
        months_range = pd.date_range(start=row['contractStartDate'], end=row['contractEndDate'], freq='M')
        total_months = len(months_range)
        monthly_contract_value = row['totalContractValue'] / total_months
        
        # Create a DataFrame for each contract
        df_temp = pd.DataFrame({
            'customerId': [row['customerId']] * total_months,
            'contractId': [row['contractId']] * total_months,
            'month': months_range,
            'monthlyRevenue': [monthly_contract_value] * total_months
        })
        # Apply the function to each row of the original DataFrame and concatenate the results
        return df_temp
    
    df_temp = pd.concat(df.apply(calculate_months_and_value, axis=1).tolist(), ignore_index=True)
    df2 = df_temp.groupby(['customerId', 'month']).agg({'monthlyRevenue': 'sum'}).reset_index()

    # Format 'month' column to YYYY-MM
    df2['month'] = df2['month'].dt.strftime('%Y-%m')  


    # Fill NaN values with 0 for 'monthlyRevenue'
    df2['monthlyRevenue'] = df2['monthlyRevenue'].fillna(0)


    return df2


def create_arr_metrics(df):
    """
    Process df containing monthly rr values for each customer and generates aggregated value.
    Also create the wwaterfall or flow of ARR 

    Parameters:
    - df (pd.DataFrame): Dataframe with each row containing customer and month level contract value - monthlyRevenue

    Returns: 2 data frames
    - pd.DataFrame: Dataframe with transposed data for each customer - for each month becoming a column, also gives customer level aggregated revenue
    - pd.DataFrame: Gives the over all metrics for each month, agrregatd for all customers - MRR, ARR, newBusiness, upSell, downSell, churn 
    """

    transposed_df = create_transposed_monthly_revenue_matrix(df)
    customer_arr_df, metrics_df = create_customer_and_aggregated_metrics(transposed_df)
    return customer_arr_df, metrics_df


def create_transposed_monthly_revenue_matrix (df): 
    """
    Process df containing monthly rr values for each customer and creates a transposed dataframe

    Parameters:
    - df (pd.DataFrame): Dataframe with each row containing customer and month level contract value

    Returns:
    - pd.DataFrame: Dataframe with transposed data - for each month becoming a column, also gives customer level aggregated revenue
    """


    # Print the original dataframe
    print("Original DataFrame:")

    # select only the required columns 
    df = df.loc[:, ['customerId', 'month','monthlyRevenue']]

    # Melt the original dataframe
    melted_df = pd.melt(df, id_vars=['customerId', 'month'],
                        var_name='measureType', value_name='value')

    print("melted df")
    #print(melted_df)
    # Get unique months dynamically
    # Transpose the melted dataframe
    transposed_df = melted_df.pivot_table(index=['customerId', 'measureType'],
                                        columns='month', values='value', fill_value=0, aggfunc='sum').reset_index()

    #print(transposed_df)
    # Rename the columns for better clarity
    transposed_df.columns.name = None  # Remove the 'month' label

    # Display the transposed dataframe
    print("\nTransposed DataFrame:")
    print(transposed_df)

    return transposed_df

def create_aggregated_arr_metrics(df):
    """
    Process df containing transposed monthly metrics for each customer, aggregates the values for all customers and returns the aggregated df

    Parameters:
    - df (pd.DataFrame): transposed monthly metrics for each customerlevel with revenue, new buessiness, upsell, downsell and churn

    Returns:
    - pd.DataFrame: Gives the over all metrics for each month - MRR, ARR, newBusiness, upSell, downSell, churn 
    """


    # Group by 'customerId' and aggregate the sum across all measureTypes for each month

    aggregated_df = df.groupby(['measureType'], observed=True).agg({col: 'sum' for col in df.columns[2:]}).reset_index()

    aggregated_df.insert(0, 'customerId', 'Aggregated')


    # # Add a new row for 'ARR' which is 12 * monthlyRevenue
    arr_row = pd.DataFrame({
        'customerId': ['Aggregated'],
        'measureType': ['ARR']})
    
    # Calculate values for each month
    values_dict = {
        month: 12 * aggregated_df.loc[aggregated_df['measureType'] == 'monthlyRevenue', month].iloc[0]
        for month in df.columns[2:]
    }

    # Create a Series with the calculated values and set the index to match df.columns
    arr_series = pd.Series(values_dict, index=df.columns[2:])

    # # Append the new row to the DataFrame
    # arr_series = pd.Series(values_dict, index=df.columns[2:])

    # Create a DataFrame from the Series
    arr_row = pd.DataFrame([arr_series], columns=arr_series.index)

    # Add 'customerId' and 'measureType'
    arr_row['customerId'] = 'Aggregated'
    arr_row['measureType'] = 'ARR'

    # add the ARR row to the original df 
    aggregated_df = pd.concat([aggregated_df, arr_row], ignore_index=True)

    # Display the aggregated DataFrame
    print("\nAggregated DataFrame:")
    print(aggregated_df)

    return aggregated_df


def create_customer_and_aggregated_metrics(df):
    """
    Process df containing transposed monthly metrics for each customer with aggregated monthly revenue, and calculates the following metrics
        newBusiness 
        upSell
        downSell
        churn 

    Parameters:
    - df (pd.DataFrame): transposed monthly metrics for each customer with aggregated monthly revenue

    Returns:
    - pd.DataFrame: Gives the over all metrics for each month for each customer - MRR, ARR, newBusiness, upSell, downSell, churn 
    - pd.DataFrame: Gives aggregated metrics  - MRR, ARR, newBusiness, upSell, downSell, churn 
    """


    # Identify 'newBusiness' rows based on the condition
    mask = (df.shift(axis=1, fill_value=0) == 0) & (df != 0)

    # Create a new DataFrame with 'newBusiness' rows
    new_business_df = df[mask].copy()
    new_business_df['measureType'] = 'newBusiness'

    # Fill NaN values with 0
    new_business_df = new_business_df.fillna(0)

    # Identify 'upSell' rows based on the condition for all month columns
    df_numeric = df.iloc[:, 2:].apply(pd.to_numeric, errors='coerce')  # Convert columns to numeric
    up_sell_mask = (df_numeric.diff(axis=1) > 0) & (df_numeric.shift(axis=1) != 0)
    up_sell_df = (df_numeric[up_sell_mask] - df_numeric.shift(axis=1))[up_sell_mask].copy()
    up_sell_df['measureType'] = 'upSell'

    # Mask to make 'upSell' rows zero when the previous month's 'monthlyRevenue' is 0 for all month columns
    zero_month_mask = (df_numeric.iloc[:, :-1] == 0)
    up_sell_df[zero_month_mask] = 0

    # Retrieve the 'customerId' values for 'upSell' rows
    up_sell_df['customerId'] = df.loc[up_sell_mask.index, 'customerId'].values

    # Identify 'downSell' rows based on the condition for all month columns
    down_sell_mask = (df_numeric.diff(axis=1) < 0) & (df_numeric.shift(axis=1) != 0) & (df_numeric !=0 )
    down_sell_df = (df_numeric[down_sell_mask] - df_numeric.shift(axis=1))[down_sell_mask].copy()
    down_sell_df['measureType'] = 'downSell'

    # Retrieve the 'customerId' values for 'downSell' rows
    down_sell_df['customerId'] = df.loc[down_sell_mask.index, 'customerId'].values

    # Calculate 'churn' rows based on the specified condition
    churn_mask = (df_numeric.diff(axis=1) < 0) & (df_numeric == 0)
    churn_df = (df_numeric[churn_mask] - df_numeric.shift(axis=1))[churn_mask].copy()
    churn_df['measureType'] = 'churn'


    # Retrieve the 'customerId' values for 'churn' rows
    churn_df['customerId'] = df.loc[churn_mask.index, 'customerId'].values

    # Append 'upSell', 'downSell', and 'churn' rows to the original DataFrame
    df = pd.concat([df, up_sell_df, down_sell_df, churn_df], ignore_index=True)

    # Append 'newBusiness' rows to the original DataFrame
    df = pd.concat([df, new_business_df], ignore_index=True)

    # Fill NaN values with 0
    df = df.fillna(0)

    # Define the sorting order for 'measureType'
    sorting_order = ['monthlyRevenue', 'newBusiness', 'upSell', 'downSell', 'churn']

    # Sort the DataFrame based on 'measureType' using the defined order and 'customerId'
    df['measureType'] = pd.Categorical(df['measureType'], categories=sorting_order, ordered=True)
    df = df.sort_values(['customerId', 'measureType'])


    df_agg = create_aggregated_arr_metrics(df)
    print(df)
    return df, df_agg