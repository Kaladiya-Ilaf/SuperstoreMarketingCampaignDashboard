import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np 
import matplotlib.cm as cm


data = pd.read_csv("superstorecampaign_data.csv")


# Title and header
st.title("Superstore Marketing Campaign Analysis")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)

st.subheader("Explore customer data and campaign performance")

  
# Customer demographics section
col1, col2 = st.columns((2))
with col1:
    # Multi-select dropdown for education selection (optional)
    st.header("Customer Demographics")
    education_options = data["Education"].unique()
    selected_education = st.multiselect("Select Education Levels (optional)", education_options)
    if selected_education:
        data = data[data["Education"].isin(selected_education)]

    # Matplotlib bar chart for education distribution
    plt.figure(figsize=(8, 6))
    plt.bar(data["Education"].value_counts().index, data["Education"].value_counts().values)
    plt.xlabel("Education Level")
    plt.ylabel("Number of Customers")
    plt.title("Education Distribution")
    st.pyplot(plt)
    
with col2:
    st.subheader("Marital Status Distribution")
    st.bar_chart(data["Marital_Status"].value_counts())

    #Interactive slider for age range
    age_range = st.slider("Select age range", min_value=data["Customer_Age"].min(), max_value=data["Customer_Age"].max(), value=(data["Customer_Age"].min(), data["Customer_Age"].max()))
    filtered_data_age = data[data["Customer_Age"].between(age_range[0], age_range[1])]


st.header("Spending Patterns")
col3, col4 = st.columns((2))

with col3:
    st.subheader("Average Spending per Product Category")
    product_options = ["MntWines","MntFruits","MntMeatProducts","MntFishProducts","MntSweetProducts","MntGoldProds"]
    product_options_array = np.array(product_options)

    selected_product = st.selectbox("Select Product", product_options_array)

    if selected_product in filtered_data_age.columns:
        avg_spending_category = filtered_data_age.groupby(selected_product)[selected_product].mean().reset_index(name="Average_Spending")

    # Create a figure with one subplot for clarity
        fig, ax = plt.subplots(figsize=(10, 6))

        ax.bar(avg_spending_category[selected_product], avg_spending_category["Average_Spending"])  # Use the new column name
        ax.set_xlabel(f"Product Category({selected_product})")
        ax.set_ylabel("Average Spending")
        ax.set_title("Average Spending per Product Category")
        st.pyplot(fig)
    else:
        st.warning(f"The '{selected_product}' column is not present in the filtered data. Average spending cannot be calculated.")
 
with col4: 
    st.subheader("Explore overall purchase behavior across channels")

        # Purchase channel selection for plotting
    purchase_channels = [
            "NumDealsPurchases",
            "NumWebPurchases",
            "NumCatalogPurchases",
            "NumStorePurchases",
        ]

    selected_channels = st.multiselect("Select Purchase Channels to Plot", purchase_channels)

    purchase_data = data[selected_channels]

    # Line chart to visualize average purchase trends
    fig, ax = plt.subplots(figsize=(10, 6))
    # Calculate average purchases per month across all customers
    average_purchases = purchase_data.mean(axis=0)
    ax.plot(average_purchases.index, average_purchases, label="Average Purchases")
    ax.set_xlabel("Month")
    ax.set_ylabel("Average Number of Purchases")
    ax.set_title(f"Average Purchase Trends Across Channels (Selected Channels)")
    ax.legend()
    plt.tight_layout()
    st.pyplot(fig)


st.header("Customer Segmentation")
col5, col6 = st.columns((2))

with col5:
    income_min, income_max = data["Income"].min(), data["Income"].max()
    income_filter = st.slider("Select income range", income_min, income_max, (income_min, income_max))
    filtered_data_income = data[data["Income"].between(income_filter[0], income_filter[1])]

        # Recency slider for interactive filtering
    recency_min, recency_max = filtered_data_income["Recency"].min(), filtered_data_income["Recency"].max()
    recency_filter = st.slider("Select recency range", recency_min, recency_max, (recency_min, recency_max))
    filtered_data_segment = filtered_data_income[filtered_data_income["Recency"].between(recency_filter[0], recency_filter[1])]

with col6:
    # Scatter plot for interaction between income and recency
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(filtered_data_segment["Income"], filtered_data_segment["Recency"], alpha=0.7)
    ax.set_xlabel("Income")
    ax.set_ylabel("Recency")
    ax.set_title("Interaction between Income and Recency (Filtered)")
    plt.tight_layout()
    st.pyplot(fig)



st.subheader("Explore responses, complaints, and enrollment duration")


# Enrollment year range slider
data["Years_Since_Enrollment"] = pd.to_numeric(data["Years_Since_Enrollment"], errors='coerce')

enrollment_min, enrollment_max = data["Years_Since_Enrollment"].min(), data["Years_Since_Enrollment"].max()
enrollment_filter = st.slider("Select Enrollment Duration Range (Years)", enrollment_min, enrollment_max, (enrollment_min, enrollment_max))
enrollment_filtered_data = data[data["Years_Since_Enrollment"].between(enrollment_filter[0], enrollment_filter[1])]
col7, col8 = st.columns((2))


    # Distribution of responses
with col7:
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.hist(enrollment_filtered_data["Response"], bins="auto", edgecolor="black")
    ax.set_xlabel("Response Category")
    ax.set_ylabel("Number of Customers")
    ax.set_title("Distribution of Responses (Filtered by Enrollment)")
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
    plt.tight_layout()
    st.pyplot(fig)

with col8:
        # Complaints vs. enrollment duration (scatter plot)
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.hist(enrollment_filtered_data["Complain"], bins="auto", edgecolor="black")
    ax.set_ylabel("Number of Customers")
    ax.set_xlabel("Complaints")
    ax.set_title("Complaints vs. Enrollment Duration (Filtered by Enrollment)")
    plt.tight_layout()
    st.pyplot(fig)