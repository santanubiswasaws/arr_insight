import streamlit as st
import pandas as pd

def perform_column_mapping(predefined_columns, column_names):

    # Create a DataFrame
    df = pd.DataFrame({'columnHeaders': predefined_columns, 'columnNames': 'double click to select .. '})

    # Initialize the mapping dictionary in session state
    if 'column_mapping' not in st.session_state:
        st.session_state.column_mapping = {}

    st.subheader("Map columns", divider='green')    

    col11, col2, col3 = st.columns(3)
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
                    disabled=True
                )      
            }, 
            hide_index=True,
            )

        if st.button('Process mapping'):
            # Return a message to signal that the mapping is complete
            return result_df.set_index('columnHeaders')['columnNames'].to_dict()
        
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
