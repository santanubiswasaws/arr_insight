import streamlit as st
import pandas as pd
from arr_lib.column_mapping import map_columns
from arr_lib.column_mapping import PREDEFINED_COLUMN_HEADERS
from arr_lib.arr_analysis import create_monthly_buckets
from arr_lib.arr_analysis import create_arr_metrics
from arr_lib.arr_analysis import create_customer_and_aggregated_metrics
from arr_lib.column_mapping_ui import perform_column_mapping


from arr_lib.styling import BUTTON_STYLE

def main():

    #st.set_page_config(page_title="ARR Analysis")
    st.set_page_config(page_title="ARR Analysis" , layout='wide')
    st.header("Analyze Annual Recurring Revnue (ARR)")


    st.markdown(BUTTON_STYLE, unsafe_allow_html=True)

    # Upload CSV file
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

    if uploaded_file is not None:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(uploaded_file)


            # Display mapped data 
        if not st.checkbox('Hide uploaded data'):
            # Display the uploaded DataFrame
            st.subheader('Uploaded Data :', divider='green') 
            st.write(df)


        st.markdown("<br>", unsafe_allow_html=True)


        # Column Mapping Section 

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
            # Display mapped data 
            if not st.checkbox('Hide mapped data'):
                st.subheader("Mapped Data :", divider='green') 
                st.dataframe(st.session_state.mapped_df, use_container_width=False)


        st.markdown("<br><br>", unsafe_allow_html=True)


        # Monthly bucket

        # initialize arr_df 
        if 'arr_df' not in st.session_state:
                st.session_state.arr_df = pd.DataFrame()


        # Add a button to calculate monthly contract values

        if st.button("Generate Monthly Buckets", type="primary"):
            try:
                # Call the method to create df2
                with st.spinner("Calculating Monthly Numbers ..."):
                    # Call the method to create df2
                    mapped_df = st.session_state.mapped_df
                    # arr_df = create_monthly_rr_analysis(mapped_df)
                    arr_df = create_monthly_buckets(mapped_df)                    

                    # Initialize or update st.session_state.arr_df
                    if 'arr_df' not in st.session_state:
                        st.session_state.arr_df = arr_df
                    else:
                        st.session_state.arr_df = arr_df

            except ValueError as e:
                st.error(f"Error: {str(e)}")
    

        if st.session_state.arr_df is not None:
            if not st.checkbox('Hide monthly buckets'):
            # Display monthly arr df
                st.subheader('Monthly buckets :', divider='green') 
                st.dataframe(st.session_state.arr_df.round(2), use_container_width=False, hide_index=True)

        
        st.markdown("<br><br>", unsafe_allow_html=True)

        # Metrics Calculation section
        if 'transpose_df' not in st.session_state:
                st.session_state.transpose_df = pd.DataFrame(columns=['customerId', 'measureType'])

        if 'metrics_df' not in st.session_state:
                st.session_state.metrics_df = pd.DataFrame(columns=['customerId', 'measureType'])

        # Add a button to calculate monthly contract values
        if st.button("Generate ARR Metrics", type="primary"):       
            try:
                with st.spinner("Calculating ARR Metrics"):
                    
                    # Call the method to create the metrics df
                    arr_df = st.session_state.arr_df
                    # transpose_df, metrics_df = create_arr_metrics(arr_df)
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
            # Display customer level detailes 
            if st.checkbox('Show Customer level ARR details'):
                # Display customer level ARR metrics
                st.subheader('Customer Level ARR Metrics :', divider='green') 

                # set inde to customerId, measureType - for freeze pane functionality
                display_transposed_df = st.session_state.transpose_df.round(2)
                display_transposed_df.set_index(['customerId', 'measureType'], inplace=True)
                st.dataframe(display_transposed_df, use_container_width=True)

            st.subheader('Aggregated ARR Metrics :', divider='green') 

            # set inde to customerId, measureType - for freeze pane functionality
            display_metrics_df= st.session_state.metrics_df.round(0)
            display_metrics_df.set_index(['customerId', 'measureType'], inplace=True)
            st.dataframe(display_metrics_df, use_container_width=True)
        

        # Replanning section 
        if 'planning_df' not in st.session_state:
                st.session_state.planning_df = pd.DataFrame(columns=['customerId', 'measureType'])

        if "random_key" not in st.session_state:
            st.session_state["random_key"] = 0

        # Add a button to calculate monthly contract values
        if st.button("Create or Reset Planing Sheet", type="primary"):    
            st.session_state["random_key"] += 1   
            try:
                with st.spinner("Creating planning sheet"):
                    
                    #reset panning_df 
                    if 'planning_df' in st.session_state:
                        st.session_state.planning_df = pd.DataFrame(columns=['customerId', 'measureType'])

                    # Call the method to create the metrics df
                    planning_df = st.session_state.transpose_df
                    planning_df = planning_df[planning_df['measureType'] == 'monthlyRevenue']      
                    st.session_state.planning_df = planning_df

            except ValueError as e:
                st.error(f"Error: {str(e)}")


        if st.session_state.planning_df is not None:
            if not st.checkbox('Hide replan scratchpad'):
            # Display monthly arr df           
                st.subheader('Planning scratchpad - you can edit :', divider='green') 
                try:

                    # set inde to customerId - for freeze pane functionality
                    display_planning_df = st.session_state.planning_df.round(2)
                    display_planning_df.set_index(['customerId'], inplace=True)
                    edited_df = st.data_editor(display_planning_df, key=st.session_state["random_key"], disabled=('customerId', 'measureType'), num_rows='dynamic', hide_index=False, use_container_width=True)
                    
                    # reset index to numeric value 
                    edited_df.reset_index(inplace=True)
                    st.session_state.edited_df = edited_df
                except Exception as e:
                    st.error(f"An error occurred: {e}")


        # Replanning section 

        if 'replan_transpose_df' not in st.session_state:
                st.session_state.replan_transpose_df= pd.DataFrame(columns=['customerId', 'measureType'])

        if 'replan_metrics_df' not in st.session_state:
                st.session_state.replan_metrics_df = pd.DataFrame(columns=['customerId', 'measureType'])

        # Add a button to calculate monthly contract values
        if st.button("Replan ARR Metrics", type="primary"):       
            try:
                with st.spinner("Replanning ARR Metrics"):
                    
                    # Call the method to create the metrics df
                    edited_df = st.session_state.edited_df
                    replan_transpose_df, replan_metrics_df = create_customer_and_aggregated_metrics(edited_df)

                    # Initialize or update st.session_state.arr_df
                    if 'replan_transpose_df' not in st.session_state:
                        st.session_state.replan_transpose_df = replan_transpose_df
                    else:
                        st.session_state.replan_transpose_df = replan_transpose_df

                    # Initialize or update st.session_state.arr_df
                    if 'replan_metrics_df' not in st.session_state:
                        st.session_state.replan_metrics_df = replan_metrics_df
                    else:
                        st.session_state.replan_metrics_df = replan_metrics_df
                    
            except ValueError as e:
                st.error(f"Error: {str(e)}")

        if st.session_state.replan_metrics_df is not None:
            # Display customer level detailes 
            if st.checkbox('Show customer level replan details'):
                st.subheader('Replanned Customer Level ARR Metrics :', divider='green') 

                # set inde to customerId, measureType - for freeze pane functionality
                display_eplan_transpose_df = st.session_state.replan_transpose_df.round(2)
                display_eplan_transpose_df.set_index(['customerId', 'measureType'], inplace=True)
                st.dataframe(display_eplan_transpose_df, use_container_width=True)

            st.subheader('Replanned Aggregated ARR Metrics :', divider='green') 

            # set inde to customerId, measureType - for freeze pane functionality
            display_replan_metrics_df = st.session_state.replan_metrics_df.round(0)
            display_replan_metrics_df.set_index(['customerId', 'measureType'], inplace=True)
            st.dataframe(display_replan_metrics_df, use_container_width=True)


    # -- Create sidebar for plot controls
    st.sidebar.title('AI helper')
    query= st.sidebar.text_area('Ask your question - not implemented yet')
    st.sidebar.button(label="Ask - not functional yet - @todo")

if __name__ == "__main__":
    main()


