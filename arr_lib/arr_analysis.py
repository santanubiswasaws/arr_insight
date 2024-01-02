import pandas as pd
from datetime import datetime

def create_monthly_rr_analysis_2(df):
    """
    Process contract data and return a new DataFrame with aggregated values.

    Parameters:
    - df (pd.DataFrame): Original contract data DataFrame.

    Returns:
    - pd.DataFrame: Processed DataFrame with aggregated values.
    """
    # Check if the required columns are present
    required_columns = ['customerId', 'contractStartDate', 'contractEndDate', 'totalContractValue']
    if not all(col in df.columns for col in required_columns):
        raise ValueError("Columns 'customerId', 'contractStartDate', 'contractEndDate', and 'totalContractValue' are required in the DataFrame.")

    df2_rows = []

    # Create an empty DataFrame to store results
    df2 = pd.DataFrame(columns=['customerId', 'month', 'currentMonthContractValue', 'previousMonthAmount', 'nextMonthAmount', 'newBusiness'])

    # Iterate over each row in the original dataframe
    for _, row in df.iterrows():
        # Use pd.to_datetime to convert 'contractStartDate' and 'contractEndDate' to datetime format
        try:
            row['contractStartDate'] = pd.to_datetime(row['contractStartDate'], format='%m/%d/%y')
            row['contractEndDate'] = pd.to_datetime(row['contractEndDate'], format='%m/%d/%y')
        except ValueError:
            raise ValueError("Invalid date format in 'contractStartDate' or 'contractEndDate'. Use 'mm/dd/yy' format.")

        
        # Validate contract value
        if pd.notna(row['totalContractValue']):
            # Check if the value is a positive numeric value
            if isinstance(row['totalContractValue'], (int, float)) and row['totalContractValue'] > 0:
                pass  # Valid value, do nothing
            else:
                raise ValueError("Invalid 'totalContractValue'. It must be a positive numeric value.")
        else:
            raise ValueError("Invalid 'totalContractValue'. It must be a positive numeric value.")

        
        # Calculate the contract duration in months
        contract_duration = ((row['contractEndDate'] - row['contractStartDate']).days // 30) + 1

        # Validate contract duration
        if contract_duration <= 0:
            raise ValueError("Invalid contract duration. 'contractEndDate' should be later than 'contractStartDate'.")

        # Calculate the monthly contract value
        monthly_contract_value = row['totalContractValue'] / contract_duration

        # Generate monthly records for the new dataframe
        for i in range(contract_duration):
            current_month = row['contractStartDate'] + pd.DateOffset(months=i)

            # Check if a record already exists for the customer and month
            existing_record = df2[(df2['customerId'] == row['customerId']) & (df2['month'] == current_month.strftime('%Y-%m'))]

            # Skip creating a new row if currentMonthContractValue is already present for the customer and month
            if existing_record.empty or existing_record['monthlyRevenue'].sum() == 0:
                df2_rows.append({
                    'customerId': row['customerId'],
                    'month': current_month.strftime('%Y-%m'),
                    'monthlyRevenue': monthly_contract_value,
                    'previousMonthAmount': 0,  # Placeholder for now
                    'nextMonthAmount': 0,  # Placeholder for now
                    'newBusiness': 0  # Placeholder for now
                })

    # Create the DataFrame after the loop
    df2 = pd.DataFrame(df2_rows)

    # Group by customerId and month, sum the currentMonthContractValue
    df2 = df2.groupby(['customerId', 'month'], as_index=False).agg({'monthlyRevenue': 'sum'})

    # Update the 'previousMonthAmount' and 'nextMonthAmount' columns
    for idx, row in df2.iterrows():
        previous_month_row = df2[(df2['customerId'] == row['customerId']) & (df2['month'] == (datetime.strptime(row['month'], '%Y-%m') - pd.DateOffset(months=1)).strftime('%Y-%m'))]
        next_month_row = df2[(df2['customerId'] == row['customerId']) & (df2['month'] == (datetime.strptime(row['month'], '%Y-%m') + pd.DateOffset(months=1)).strftime('%Y-%m'))]

        df2.at[idx, 'previousMonthAmount'] = previous_month_row['monthlyRevenue'].sum() if not previous_month_row.empty else 0
        df2.at[idx, 'nextMonthAmount'] = next_month_row['monthlyRevenue'].sum() if not next_month_row.empty else 0


    # metrics calculation 

    # Define boolean conditions for calculations of metrics 
    condition1 = df2['monthlyRevenue'] == df2['previousMonthAmount']
    condition2 = df2['previousMonthAmount'] == 0
    condition3 = df2['monthlyRevenue'] > df2['previousMonthAmount']
    condition4 = df2['previousMonthAmount'] != 0
    condition5 = df2['monthlyRevenue'] < df2['previousMonthAmount']
    condition6 = df2['nextMonthAmount'] != 0
    condition7 = df2['nextMonthAmount'] == 0
    condition8 = df2['monthlyRevenue'] > 0
   
    # Apply the conditions to calculate the 'newBusiness' column
    df2['newBusiness'] = 0
    df2.loc[condition2, 'newBusiness'] = df2.loc[condition2, 'monthlyRevenue']

    # Apply the conditions to calculate the 'upSell' column
    df2['upSell'] = 0
    df2.loc[condition3 & condition4, 'upSell'] = df2['monthlyRevenue'] - df2['previousMonthAmount']

    # Apply the conditions to calculate the 'downSell' column
    df2['downSell'] = 0
    df2.loc[condition5 & condition6, 'downSell'] = df2['previousMonthAmount'] - df2['monthlyRevenue']

    # Apply the conditions to calculate the 'downSell' column
    df2['churn'] = 0
    df2.loc[condition7 & condition8, 'churn'] = df2['monthlyRevenue']  

    return df2


def create_monthly_rr_analysis(df):
    """
    Process contract data and return a new DataFrame with aggregated values.

    Parameters:
    - df (pd.DataFrame): Original contract data DataFrame.

    Returns:
    - pd.DataFrame: Processed DataFrame with aggregated values.
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

    # Function to calculate total months and monthly contract value
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

    # Update the 'previousMonthAmount' and 'nextMonthAmount' columns
    df2['previousMonthAmount'] = df2.groupby('customerId')['monthlyRevenue'].shift(fill_value=0)
    df2['nextMonthAmount'] = df2.groupby('customerId')['monthlyRevenue'].shift(-1, fill_value=0)



    # metrics calculation 

    # Define boolean conditions for calculations of metrics 
    condition1 = df2['monthlyRevenue'] == df2['previousMonthAmount']
    condition2 = df2['previousMonthAmount'] == 0
    condition3 = df2['monthlyRevenue'] > df2['previousMonthAmount']
    condition4 = df2['previousMonthAmount'] != 0
    condition5 = df2['monthlyRevenue'] < df2['previousMonthAmount']
    condition6 = df2['nextMonthAmount'] != 0
    condition7 = df2['nextMonthAmount'] == 0
    condition8 = df2['monthlyRevenue'] > 0
   
    # Apply the conditions to calculate the 'newBusiness' column
    df2['newBusiness'] = 0
    df2.loc[condition2, 'newBusiness'] = df2.loc[condition2, 'monthlyRevenue']

    # Apply the conditions to calculate the 'upSell' column
    df2['upSell'] = 0
    df2.loc[condition3 & condition4, 'upSell'] = df2['monthlyRevenue'] - df2['previousMonthAmount']

    # Apply the conditions to calculate the 'downSell' column
    df2['downSell'] = 0
    df2.loc[condition5 & condition6, 'downSell'] = df2['previousMonthAmount'] - df2['monthlyRevenue']

    # Apply the conditions to calculate the 'downSell' column
    df2['churn'] = 0
    df2.loc[condition7 & condition8, 'churn'] = df2['monthlyRevenue']

    return df2






def create_arr_metrics(df):
    """
    Process df containing monthly rr values for each customer and generates aggregated value.
    Also create the wwaterfall or flow of ARR 

    Parameters:
    - df (pd.DataFrame): Dataframe with each row containing customer and month level contract value, 
    new buessiness, upsell, downsell and churn

    Returns:
    - pd.DataFrame: Dataframe with transposed data - for each month becoming a column, also gives customer level aggregated revenue
    - pd.DataFrame: Gives the over all metrics for each month - MRR, ARR, newBusiness, upSell, downSell, churn 
    """


    # Print the original dataframe
    print("Original DataFrame:")

    # select only the required columns 
    df = df.loc[:, ['customerId', 'month','monthlyRevenue','newBusiness', 'upSell', 'downSell','churn']]

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

    print(transposed_df)
    #transposed_df = transposed_df.reindex(columns=['customerId', 'measureType'] + list(months))


    # Display the transposed dataframe
    print("\nTransposed DataFrame:")
    #print(transposed_df)



    # Define a custom order for the 'Category' column
    custom_sort_order = ['monthlyRevenue','newBusiness', 'upSell', 'downSell','churn']

    # Convert 'Category' to a categorical column with the custom order
    transposed_df['measureType'] = pd.Categorical(transposed_df['measureType'], categories=custom_sort_order, ordered=True)
    print('cat')
    #print(transposed_df)

    # Sort the DataFrame by a combination of columns (e.g., 'Category' and 'Salary')
    transposed_df_sorted = transposed_df.sort_values(by=['customerId', 'measureType'], ascending=[True, True])

    # Display the sorted DataFrame
    print("\nSorted DataFrame by Combination of Columns with Custom Sort Order:")
    #print(transposed_df_sorted)



    transpose_df = transposed_df_sorted
    metrics_df = create_aggregated_arr_metrics(transpose_df)
    return transpose_df, metrics_df


def create_aggregated_arr_metrics(df):
    """
    Process df containing transposed monthly metrics for each customer, aggregates the values for all customers and returns the aggregated df

    Parameters:
    - df (pd.DataFrame): transposed monthly metrics for each customerlevel with revenue, new buessiness, upsell, downsell and churn

    Returns:
    - pd.DataFrame: Gives the over all metrics for each month - MRR, ARR, newBusiness, upSell, downSell, churn 
    """


    # Group by 'customerId' and aggregate the sum across all measureTypes for each month
    aggregated_df = df.groupby(['measureType']).agg({col: 'sum' for col in df.columns[2:]}).reset_index()

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
