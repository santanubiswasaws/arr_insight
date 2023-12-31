import streamlit as st
import pandas as pd
from arr_lib.column_mapping import map_columns
from arr_lib.arr_analysis import create_monthly_rr_analysis
from arr_lib.column_mapping_ui import perform_column_mapping

def main():

    #st.set_page_config(page_title="ARR Analysis", layout='wide')
    st.set_page_config(page_title="ARR Analysis")
    st.header("Analyse Annual Recurring Revnue (ARR)")

    # Upload CSV file
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

    if uploaded_file is not None:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(uploaded_file)

        # Display the uploaded DataFrame
        st.subheader('Uploaded Data:')
        st.write(df)

        # Predefined values for mapping
        predefined_values = ['customerId', 'contractId', 'contractStartDate', 'contractEndDate', 'totalContractValue']

        # Column names from the DataFrame
        column_names = list(df.columns)

        # Call the perform_column_mapping method - to render mapping UI 
        column_mapping_result = perform_column_mapping(predefined_values, column_names)

        # Display the result
        if column_mapping_result is not None:
            #column_mapping_result = st.session_state.column_mapping
            mapped_df = map_columns (df, column_mapping_result)
            st.session_state.mapped_df = mapped_df
            st.subheader("Mapped Data:")
            st.dataframe(mapped_df, use_container_width=True)

        # Add a button to calculate monthly contract values
        if st.button("Calculate Monthly RR Analysis"):
            try:
                # Call the method to create df2
                mapped_df = st.session_state.mapped_df
                arr_df = create_monthly_rr_analysis(mapped_df)
    
                # Display df2
                st.subheader('Monthly bucket', divider='green') 
                st.dataframe(arr_df, use_container_width=True)


            except ValueError as e:
                st.error(f"Error: {str(e)}")


def create_mapped_dataframe(df):
    # Retrieve the mapping from session state
    column_mapping = st.session_state.column_mapping
    print(column_mapping)

    # Create a new DataFrame with mapped columns and values
    new_df = pd.DataFrame({key: df[value].tolist() for key, value in column_mapping.items()})

    return new_df

if __name__ == "__main__":
    main()


