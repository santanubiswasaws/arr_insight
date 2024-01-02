import streamlit as st
import pandas as pd
from arr_lib.column_mapping import map_columns
from arr_lib.column_mapping import PREDEFINED_COLUMN_HEADERS
from arr_lib.arr_analysis import create_monthly_rr_analysis
from arr_lib.arr_analysis import create_arr_metrics
from arr_lib.column_mapping_ui import perform_column_mapping
from arr_lib.styling import BUTTON_STYLE

def main():

    #st.set_page_config(page_title="ARR Analysis")
    st.set_page_config(page_title="ARR Analysis", layout='wide')
    st.header("Analyze Annual Recurring Revnue (ARR)")


    st.markdown(BUTTON_STYLE, unsafe_allow_html=True)

    # Upload CSV file
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

    if uploaded_file is not None:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(uploaded_file)

        # Display the uploaded DataFrame
        st.subheader('Uploaded Data :', divider='green') 
        st.write(df)


        st.markdown("<br>", unsafe_allow_html=True)

        # Column names from the DataFrame
        column_names = list(df.columns)

        # Call the perform_column_mapping method - to render mapping UI 
        column_mapping_result = perform_column_mapping(PREDEFINED_COLUMN_HEADERS, column_names)

        # initialize mapped_df
        if 'mapped_df' not in st.session_state:
                st.session_state.mapped_df = pd.DataFrame()

        # Display the result
        if column_mapping_result is not None:
            mapped_df = map_columns (df, column_mapping_result)
            st.session_state.mapped_df = mapped_df

        if st.session_state.mapped_df is not None:
            st.subheader("Mapped Data :", divider='green') 
            st.dataframe(st.session_state.mapped_df, use_container_width=True)


        st.markdown("<br><br>", unsafe_allow_html=True)


        # initialize arr_df 
        if 'arr_df' not in st.session_state:
                st.session_state.arr_df = pd.DataFrame()

        # Add a button to calculate monthly contract values
        if st.button("Generate monthly numbers : ", type="primary"):
            try:
                # Call the method to create df2
                with st.spinner("Calculating Monthly Numbers ..."):
                    # Call the method to create df2
                    mapped_df = st.session_state.mapped_df
                    arr_df = create_monthly_rr_analysis(mapped_df)

                    # Initialize or update st.session_state.arr_df
                    if 'arr_df' not in st.session_state:
                        st.session_state.arr_df = arr_df
                    else:
                        st.session_state.arr_df = arr_df

            except ValueError as e:
                st.error(f"Error: {str(e)}")
    
        if st.session_state.arr_df is not None:
            # Display monthly arr df
            st.subheader('Monthly buckets :', divider='green') 
            st.dataframe(st.session_state.arr_df.round(0), use_container_width=True)

        
        st.markdown("<br><br>", unsafe_allow_html=True)

        # initialize metrics_df 
        if 'transpose_df' not in st.session_state:
                st.session_state.transpose_df = pd.DataFrame()

        if 'metrics_df' not in st.session_state:
                st.session_state.metrics_df = pd.DataFrame()

        # Add a button to calculate monthly contract values
        if st.button("Generate ARR Metrics", type="primary"):       
            try:
                with st.spinner("Calculating ARR Metrics"):
                    
                    # Call the method to create the metrics df
                    arr_df = st.session_state.arr_df
                    transpose_df, metrics_df = create_arr_metrics(arr_df)

                    # Initialize or update st.session_state.arr_df
                    if 'transpose_df' not in st.session_state:
                        st.session_state.transpose_df = transpose_df
                    else:
                        st.session_state.transpose_df = transpose_df
                    
                    # Initialize or update st.session_state.arr_df
                    if 'metrics_df' not in st.session_state:
                        st.session_state.metrics_df = metrics_df
                    else:
                        st.session_state.metrics_df = metrics_df

            except ValueError as e:
                st.error(f"Error: {str(e)}")

        if st.session_state.metrics_df is not None:
            # Display monthly arr df
            st.subheader('Customer Level ARR Metrics :', divider='green') 
            st.dataframe(st.session_state.transpose_df.round(0), use_container_width=True)

            st.subheader('Aggregated ARR Metrics :', divider='green') 
            st.dataframe(st.session_state.metrics_df.round(0), use_container_width=True)


if __name__ == "__main__":
    main()


