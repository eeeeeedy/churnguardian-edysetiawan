import streamlit as st
from streamlit_extras.let_it_rain import rain
from streamlit_extras.app_logo import add_logo
import model, eda
from sklearn.base import BaseEstimator, TransformerMixin

class FilterAndSelect(BaseEstimator, TransformerMixin):
    def __init__(self, churn_column='cust_stat_pred', selected_features=None):
        self.churn_column = churn_column
        self.selected_features = selected_features
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        churned_customers = X[X[self.churn_column] == 1]
        if self.selected_features:
            return churned_customers[self.selected_features]
        return churned_customers
    

# Set page title and icon
st.set_page_config(page_title='Final Project', page_icon='⭐')

# Create sidebar navigation
st.markdown(
    f"""
    <style>
        [data-testid="stSidebar"] {{
            background-image: url(https://github.com/eeeeeedy/churnguardian-edysetiawan/blob/main/assets/ChurnGuardian-Logo-Transparants.png?raw=true);
            background-repeat: no-repeat;
            padding-top: 20px;
            background-position: 10px 50px;
            background-size: 310px 85px;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

selected_page = st.sidebar.radio('Select Page', ('📋 Home Page', '📊 Exploratory Data Analysis', '💻 Model'))

# Halaman Home Page
if selected_page == '📋 Home Page':
    st.image("https://github.com/eeeeeedy/churnguardian-edysetiawan/blob/main/assets/ChurnGuardian-Logo-Transparants.png?raw=true", use_column_width=True)
    # st.title('Machine Learning Application Project')
    st.markdown('Made by <a href="hhttps://www.linkedin.com/in/edysetiawan/" target="_blank" style="font-size: 35px;">Edy Setiawan</a>', unsafe_allow_html=True)
    st.header('Background')
    st.markdown('''
                The telecommunications industry is highly competitive, and customer churn is a significant concern. Retaining existing customers is often more cost-effective than acquiring new ones.
                Therefore, predicting customer churn and understanding the underlying reasons can provide invaluable insights for customer retention strategies.
                ''')
    st.header('Data Overview')
    st.markdown('''
                This dataset contains detailed information about customers in the telecommunications industry, with a specific focus on a wide range of attributes that could potentially serve as indicators of customer churn.
                ''')
    st.header('Project Objective')
    st.markdown('''
    To develop a machine learning model that predicts customer churn in the telecommunications industry with at least 85% accuracy, 
    and to segment the identified "at-risk" customers into clusters for targeted retention strategies.
                ''')
    st.header('CSV for Model Testing')
    st.markdown('''
    For model testing, you may download example CSV file here : https://github.com/eeeeeedy/churnguardian-edysetiawan/blob/main/dataset/data_testing_for_application.csv
                ''')

# Halaman EDA
elif selected_page == '📊 Exploratory Data Analysis':
    eda.run()
    
# Halaman Model
elif selected_page == '💻 Model':
    model.run()
