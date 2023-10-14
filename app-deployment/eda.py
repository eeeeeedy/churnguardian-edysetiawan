import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def run():
    # st.title('Selamat Datang Di Halaman EDA!')    
    plot_selection = st.sidebar.selectbox(label='Choose',options=['Customer Distribution','Top Total Churn City','Customer’s reasons for churning',
                                                                 'Churn Reason', 'Age Distribution Churn vs Stayed', 'Gender Distribution Churn vs Stayed'])
    
    url = "https://raw.githubusercontent.com/FTDS-assignment-bay/FTDS-007-HCK-group-002/main/dataset/telecom_customer_churn.csv"
    df = pd.read_csv(url)
    
    # Grafik 1
    def create_plot_1():
        st.header("Pie Chart for Customer Status Distribution")
        fig_1 = plt.figure()
        customer_status_count = df['Customer Status'].value_counts()
        fig_1, ax = plt.subplots()
        ax.pie(customer_status_count, labels=customer_status_count.index, autopct='%1.1f%%')
        ax.set_title('Customer Status Distribution')
        st.pyplot(fig_1)
        with st.expander('Explanation'):
            st.text('''
                The data frame indicates that 26.5% of customers have churned. 
                The "Joined" Category row will be removed, as it doesn't offer 
                any useful insights into the churn rate.
            ''')
            
    # Grafik 2
    def create_plot_2():
        st.header("Top Total Churn City")
        fig_2 = plt.figure()
        top_churned_cities = df['City'].value_counts().nlargest(10)
        plt.title("Top Total Churned Cities")
        plt.xlabel("Cities")
        plt.ylabel("Number of Clients")
        top_churned_cities.plot(kind="bar")
        st.pyplot(fig_2)
        with st.expander('Explanation'):
            st.text('''
                The cities listed may require further investigation to understand why the churn rate is high.
                For example, you might want to look into customer service metrics, quality of service, 
                or even competitive pricing in these specific locations.
            ''')

    # Grafik 3
    def create_plot_3():
        st.header("Customer’s reasons for churning")
        fig_3 = plt.figure()
        plt.rcParams["figure.figsize"] = (11, 5)
        churned_df = df[df['Customer Status'] == 'Churned']
        freq = churned_df['Churn Category'].value_counts()
        order = freq.index
        base_color = sns.color_palette()[5]
        sns.countplot(data=churned_df, x="Churn Category", order=order, color=base_color)
        plt.title("The Customer's Reasons for Churning")
        st.pyplot(fig_3)
        with st.expander('Explanation'):
            st.text('''
                The primary reason members are leaving is due to "competitor,"
                which appears most frequently as the cause.
            ''')
    

    # Grafik 4
    def create_plot_4():
        st.header('Churn Reason')
        fig_4, ax = plt.subplots(figsize=(6, 5))
        sns.countplot(data=df, y="Churn Reason", order=df["Churn Reason"].value_counts().index, color='purple', ax=ax)
        st.pyplot(fig_4)
        with st.expander('Explanation'):
            st.text('''
                    Upon exploring the reasons of customers for churning, 
                    it becomes apparent that "better devices from competitors," 
                    "better offers from competitors," and 
                    "Attitude of support person" are the most commonly cited factors.
                ''')
            
    # Grafik 5
    def create_plot_5():
        st.header('Age Distribution Churn vs Stayed')
        fig_5 = plt.figure()
        Customer_Stayed = df[df['Customer Status'] == 'Stayed']['Age']
        Customer_Churned = df[df['Customer Status'] == 'Churned']['Age']
        plt.xlabel('Age')
        plt.ylabel('Customers Numbers')
        plt.hist([Customer_Stayed,Customer_Churned], color=['blue','orange'],label=['Stayed','Churned'])
        plt.title('Customers Behavior',fontweight ="bold")
        plt.legend()
        st.pyplot(fig_5)
        with st.expander('Explanation'):
            st.text('''
                The histogram shows that age is not a significant factor in customer retention or churn. 
                The "Stayed" group is slightly skewed towards younger ages, but not significantly. 
                The "Churned" group is evenly distributed across all age ranges.
            ''')
    
    # Grafik 6
    def create_plot_6():
        st.header('Gender Distribution Churn vs Stayed')
        fig_6 = plt.figure()
        filtered_df = df[df['Customer Status'] != 'Joined']
        sns.countplot(data=filtered_df, x='Gender', hue='Customer Status')
        plt.title('Churn Rate by Payment Method')
        plt.xlabel('Payment Method')
        plt.ylabel('Count')
        st.pyplot(fig_6)
        with st.expander('Explanation'):
            st.text('''
                The bar chart shows that the churn rate is fairly consistent across both genders. 
                Neither gender appears to be a significant factor in influencing customer churn or retention.
            ''')
            
    # Menampilkan Halaman yang Dipilih
    if plot_selection == "Customer Distribution":
        create_plot_1()
    elif plot_selection == "Top Total Churn City":
        create_plot_2()
    elif plot_selection == "Customer’s reasons for churning":
        create_plot_3()
    elif plot_selection == "Churn Reason":
        create_plot_4()
    elif plot_selection == "Age Distribution Churn vs Stayed":
        create_plot_5()
    elif plot_selection == "Gender Distribution Churn vs Stayed":
        create_plot_6()