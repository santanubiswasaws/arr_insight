import streamlit as st
import pandas as pd
from arr_lib.column_mapping import map_columns
from arr_lib.column_mapping import PREDEFINED_COLUMN_HEADERS
from arr_lib.column_mapping import PREDEFINED_DATE_FORMATS
from arr_lib.arr_validations import validate_input_data
from arr_lib.arr_validations import validate_mapping
import os
import base64

# column mapper with dateformat picker
def perform_column_mapping(predefined_columns, predefined_date_formats, input_df):


    # Column names from the DataFrame
    column_names = list(input_df.columns)

    # Create a DataFrame
    df = pd.DataFrame({'columnHeaders': predefined_columns, 'columnNames': 'double click to select .. ', 'dateFormat': 'pick appropriate date format'})
    print(df)

    # populate the df from session if exists 

    if 'loaded_map_df' not in st.session_state:
        st.session_state.loaded_map_df = pd.DataFrame()
    else: 
        loaded_map_df = st.session_state.loaded_map_df
        if (not loaded_map_df.empty): 
                    df = loaded_map_df


    # Initialize the mapping dictionary in session state
    if 'column_mapping' not in st.session_state:
        st.session_state.column_mapping = {}

    st.subheader("Map columns", divider='green')    

    col1a, col2a = st.columns([1,7], gap="small")
    with col2a: 
        if st.button("Load Saved Column Map"):
            try:
                file_path = os.path.join('data/column_map.csv')
                loaded_map_df = pd.read_csv(file_path)
                st.session_state.loaded_map_df = loaded_map_df
                st.success(f"Saved map loaded")

                loaded_map_df = st.session_state.loaded_map_df

                if (not loaded_map_df.empty): 
                    df = loaded_map_df

            except FileNotFoundError:
                st.error(f"File '{file_path}' not found. Please save the DataFrame first.")


    col1, col2, col3 = st.columns([1,5,2], gap="small")
    with col2: 
        st.markdown(f"Map columns")
        result_df= st.data_editor(
            df, 
            column_config={
                "columnNames": st.column_config.SelectboxColumn(
                    "File Columns",
                    help="The category of the app",
                    width="medium",
                    options=column_names,
                    required=True,
                ), 
                "columnHeaders": st.column_config.TextColumn(
                    disabled=True,
                ), 
                "dateFormat" : st.column_config.SelectboxColumn(
                    "Date Format",
                    width="meadium",
                    options=predefined_date_formats,
                )
            }, 
            hide_index=True,
            )
        st.session_state.result_df = result_df

    with col3:
        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button('Save/Overwrite Column Map'):
            file_path = os.path.join('data/column_map.csv')
            result_df.to_csv('data/column_map.csv', index=False)
            st.success(f"Column mapped saved")

    with col2:

        result_df = st.session_state.result_df
       
        if st.button('Process mapping'):
            
            # Validate that the mapping is complete 
            valid_map = validate_mapping(column_names, predefined_date_formats, result_df)
            if not valid_map : 
                if 'column_mapping_status' not in st.session_state:
                    st.session_state.column_mapping_status = False
                return False; 
        
            # change the column header of the input_df based on mapped column
            if result_df is not None:
                mapped_df = map_columns (input_df, result_df)
                st.session_state.mapped_df = mapped_df


                validation_status = validate_input_data(st.session_state.mapped_df)

                st.session_state.column_mapping_status = validation_status

            return validation_status
        else: 
            # # initialize validation status
            if 'column_mapping_status' not in st.session_state:
                    st.session_state.column_mapping_status = False
            return st.session_state.column_mapping_status




# another implementation using tables and dropdown lists 
def perform_column_mapping_2(predefined_values, column_names):
    st.subheader("Map columns", divider='green') 

    # Create a form for user interaction
    with st.form("column_mapping_form"):

        # Initialize the mapping dictionary in session state
        if 'column_mapping' not in st.session_state:
            st.session_state.column_mapping = {}

        for value in predefined_values:
            # Generate a 4-column layout
            col1, col2 = st.columns([1, 3], gap="small")



            # Dropdown for selecting actual column name
            with col1:
                st.markdown(f"<div style='vertical-align:top; padding:20px;'>", unsafe_allow_html=True)
                st.markdown(f"<span style='font-size: 18px; font-weight: bold; vertical-align:bottom;'>{value} :</span>", unsafe_allow_html=True)

            with col2:
                selected_column = st.selectbox("", column_names, key=f"{value}_dropdown")
                st.markdown(f"</div>", unsafe_allow_html=True)

            # Update the mapping in session state
            st.session_state.column_mapping[value] = selected_column

        # Button to perform the mapping
        submit_button = st.form_submit_button("Perform Mapping", type="primary")

    if submit_button:
        # Return a message to signal that the mapping is complete
        return st.session_state.column_mapping

    # If no submit button is pressed, return None
    return None


