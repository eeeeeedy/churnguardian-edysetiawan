import streamlit as st
import pandas as pd
import pickle
import numpy as np
import matplotlib.pyplot as plt

def run():

    # Initialize session state for the DataFrame
    if 'all_data' not in st.session_state:
        st.session_state.all_data = pd.DataFrame()

    # Load the pipelines
    with open("fp_classifier.pkl", "rb") as f:
        classification_pipeline = pickle.load(f)

    with open("clustering_pipeline_with_filter.pkl", "rb") as f:
        clustering_pipeline = pickle.load(f)

    # Choice of input: Upload or Manual Input
    choice = st.selectbox("How would you like to input data?", ["Upload CSV File", "Manual Input"])

    # A. For CSV
    if choice == "Upload CSV File":
        st.caption("""
    Please add a CSV file containing the following columns:
    **Numerical Columns:**
    - Tenure in Months
    - Number of Referrals
    - Total Revenue
    **Categorical Columns:**
    - Contract
    - Offer
    - Online Security
    - Premium Tech Support
    - Device Protection Plan
    You may download CSV here for testing purposes : https://github.com/eeeeeedy/churnguardian-edysetiawan/blob/main/dataset/data_testing_for_application.csv
    """)
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
        if uploaded_file is not None:
            df_uploaded = pd.read_csv(uploaded_file)

            # Classification prediction
            y_pred_uploaded = classification_pipeline.predict(df_uploaded)
            df_uploaded['cust_stat_pred'] = y_pred_uploaded

            # Filter the DataFrame for rows where 'cust_stat_pred' is 1
            df_filtered = df_uploaded[df_uploaded['cust_stat_pred'] == 1]

            # Clustering prediction for filtered DataFrame
            y_cluster_uploaded = clustering_pipeline.predict(df_filtered)
            df_filtered['Cluster'] = y_cluster_uploaded

            # Merge the clustering results back into the original DataFrame
            df_uploaded = df_filtered.copy()

            # Filter to only show final DataFrame where 'cust_stat_pred' is 1
            df_uploaded_final = df_uploaded[df_uploaded['cust_stat_pred'] == 1]

            # Display Prediction Results in Uploaded DataFrame
            st.write("Prediction Results in Uploaded DataFrame")
            st.write(df_uploaded_final)

            # Aggregating data by cluster
            agg_data = df_uploaded_final.groupby(['Cluster']).agg({'tenure_in_months': 'mean',
                                                                'number_of_referrals': 'mean',
                                                                'total_revenue': 'mean'})

            # Create subplots
            fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(18, 6))

            # Loop through each subplot to populate it
            for ax, column in zip(axes, agg_data.columns):
                agg_data[column].plot(kind='bar', color=['blue', 'orange', 'green'], ax=ax)
                ax.set_title(f'Average {column} by Cluster')
                ax.set_xlabel('Cluster')
                ax.set_ylabel(f'Average {column}')
                ax.set_xticks(range(len(agg_data[column])))
                ax.set_xticklabels(agg_data.index, rotation=0)

            # Ensure layout looks good
            plt.tight_layout()

            # Display the plot in Streamlit
            st.pyplot(fig)

            fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(15, 15))
            categorical_columns = ['contract', 'offer', 'online_security', 'premium_tech_support', 'device_protection_plan']

            for ax, column in zip(axes.flatten(), categorical_columns):
                df_uploaded_final.groupby(['Cluster', column]).size().unstack().plot(kind='bar', ax=ax)
                ax.set_title(f'Distribution of {column} by Cluster')
                ax.set_xlabel('Cluster')
                ax.set_ylabel('Count')
                ax.set_xticklabels(ax.get_xticklabels(), rotation=0)

            fig.delaxes(axes[2, 1])

            plt.tight_layout()
            st.pyplot(fig)

    # B. For Manual Input
    else:
        # Manual input
        Contract = st.radio(label='What is your current contract type ?',options=["One Year", "Two Years", "Month-to-Month"], key=1)
        Offer = st.radio(label='What is the last marketing offer that your received ?',options=["None", "Offer A", "Offer B", "Offer C", "Offer D", "Offer E"], key=2)
        Online_Security = st.radio("Does the credit history meet guidelines?", ["Yes", "No", "No Internet"], key=3)
        with st.expander('Explanation'):
            st.caption('If you put the answer above the answer will follow')
        if Online_Security == "Yes":
            Premium_Tech_Support = st.radio("Are you subscribes to premium technical support services?", ["Yes"])
            Device_Protection_Plan = st.radio("Are you subscribes to a device protection plan?", ["Yes"])
        elif Online_Security == "No":
            Premium_Tech_Support = st.radio("Are you subscribes to premium technical support services?", ["No"])
            Device_Protection_Plan = st.radio("Are you subscribes to a device protection plan?", ["No"])
        else:
            Premium_Tech_Support = st.radio("Are you subscribes to premium technical support services?", ["No Internet"])
            Device_Protection_Plan = st.radio("Are you subscribes to a device protection plan?", ["No Internet"])
        Tenure_in_Months = st.number_input(label='How much is your Tenure in months?', min_value= 0, key= 7)
        with st.expander('Explanation'):
            st.caption('Put your number')
        Number_of_Referrals = st.number_input(label='How many times you referred to someone else ?', min_value= 0, step= 1, key=8)
        with st.expander('Explanation'):
            st.caption('Put your number')
        Total_Revenue = st.number_input(label='How much is your Total Revenues ?', min_value= 0, step=2, key=9)
        with st.expander('Explanation'):
            st.caption('Put your number')

        new_data = pd.DataFrame({
        'contract' : [Contract],
        'offer': [Offer],
        'online_security': [Online_Security],
        'premium_tech_support': [Premium_Tech_Support],
        'device_protection_plan': [Device_Protection_Plan],
        'tenure_in_months': [Tenure_in_Months],
        'number_of_referrals': [Number_of_Referrals],
        'total_revenue': [Total_Revenue]
        })

        if st.button('Submit'):
            st.session_state.all_data = pd.concat([st.session_state.all_data, new_data], ignore_index=True)
            st.write("Current Data")  # Immediately show the updated DataFrame
            st.write(st.session_state.all_data)

        if st.button('Predict'):
            # Make a copy of the DataFrame to ensure prediction lengths match
            df_to_predict = st.session_state.all_data.copy()

            # Classification prediction
            y_pred_inf = classification_pipeline.predict(df_to_predict)
            df_to_predict['cust_stat_pred'] = y_pred_inf

            # Filter the DataFrame for rows where 'cust_stat_pred' is 1
            df_filtered = df_to_predict[df_to_predict['cust_stat_pred'] == 1]

            # Clustering prediction for filtered DataFrame
            y_cluster_inf = clustering_pipeline.predict(df_filtered)
            df_filtered['Cluster'] = y_cluster_inf

            # Merge the clustering results back into the original DataFrame
            df_to_predict = pd.merge(df_to_predict, df_filtered[['Cluster']], left_index=True, right_index=True, how='left')

            # Filter to only show final DataFrame where 'cust_stat_pred' is 1
            df_to_predict_final = df_to_predict[df_to_predict['cust_stat_pred'] == 1]

            st.session_state.all_data = df_to_predict  # Update the session state DataFrame

            st.write("Prediction Results in DataFrame")
            st.write(df_to_predict_final)

            # Aggregating data by cluster
            agg_data = df_to_predict_final.groupby(['Cluster']).agg({'tenure_in_months': 'mean',
                                                                'number_of_referrals': 'mean',
                                                                'total_revenue': 'mean'})

            # Create subplots
            fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(18, 6))

            # Loop through each subplot to populate it
            for ax, column in zip(axes, agg_data.columns):
                agg_data[column].plot(kind='bar', color=['blue', 'orange', 'green'], ax=ax)
                ax.set_title(f'Average {column} by Cluster')
                ax.set_xlabel('Cluster')
                ax.set_ylabel(f'Average {column}')
                ax.set_xticks(range(len(agg_data[column])))
                ax.set_xticklabels(agg_data.index, rotation=0)

            # Ensure layout looks good
            plt.tight_layout()

            # Display the plot in Streamlit
            st.pyplot(fig)

            fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(15, 15))
            categorical_columns = ['contract', 'offer', 'online_security', 'premium_tech_support', 'device_protection_plan']

            for ax, column in zip(axes.flatten(), categorical_columns):
                df_to_predict_final.groupby(['Cluster', column]).size().unstack().plot(kind='bar', ax=ax)
                ax.set_title(f'Distribution of {column} by Cluster')
                ax.set_xlabel('Cluster')
                ax.set_ylabel('Count')
                ax.set_xticklabels(ax.get_xticklabels(), rotation=0)

            fig.delaxes(axes[2, 1])

            plt.tight_layout()
            st.pyplot(fig)

# Run the app
if __name__ == '__main__':
    run()