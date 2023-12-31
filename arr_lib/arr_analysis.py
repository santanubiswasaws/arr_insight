import pandas as pd
from datetime import datetime

def create_monthly_rr_analysis(df):
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
    df2 = pd.DataFrame(columns=['customerId', 'month', 'currentMonthContractValue', 'previousMonthAmount', 'nextMonthAmount'])


    # Iterate over each row in the original dataframe
    for _, row in df.iterrows():
        # Use pd.to_datetime to convert 'contractStartDate' and 'contractEndDate' to datetime format
        try:
            row['contractStartDate'] = pd.to_datetime(row['contractStartDate'], format='%m/%d/%y')
            row['contractEndDate'] = pd.to_datetime(row['contractEndDate'], format='%m/%d/%y')
        except ValueError:
            raise ValueError("Invalid date format in 'contractStartDate' or 'contractEndDate'. Use 'mm/dd/yy' format.")

        # Validate contract value
        if not pd.notna(row['totalContractValue']) or row['totalContractValue'] <= 0:
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
            if existing_record.empty or existing_record['currentMonthContractValue'].sum() == 0:
                df2_rows.append({
                    'customerId': row['customerId'],
                    'month': current_month.strftime('%Y-%m'),
                    'currentMonthContractValue': monthly_contract_value,
                    'previousMonthAmount': 0,  # Placeholder for now
                    'nextMonthAmount': 0  # Placeholder for now
                })

    # Create the DataFrame after the loop
    df2 = pd.DataFrame(df2_rows)

    # Group by customerId and month, sum the currentMonthContractValue
    df2 = df2.groupby(['customerId', 'month'], as_index=False).agg({'currentMonthContractValue': 'sum'})

    # Update the 'previousMonthAmount' and 'nextMonthAmount' columns
    for idx, row in df2.iterrows():
        previous_month_row = df2[(df2['customerId'] == row['customerId']) & (df2['month'] == (datetime.strptime(row['month'], '%Y-%m') - pd.DateOffset(months=1)).strftime('%Y-%m'))]
        next_month_row = df2[(df2['customerId'] == row['customerId']) & (df2['month'] == (datetime.strptime(row['month'], '%Y-%m') + pd.DateOffset(months=1)).strftime('%Y-%m'))]

        df2.at[idx, 'previousMonthAmount'] = previous_month_row['currentMonthContractValue'].sum() if not previous_month_row.empty else 0
        df2.at[idx, 'nextMonthAmount'] = next_month_row['currentMonthContractValue'].sum() if not next_month_row.empty else 0

    return df2
