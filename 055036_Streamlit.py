import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Apply custom styling (dark background and white text)
st.markdown(
    """
    <style>
    body {
        background-color: black;
        color: white;
    }
    .stTextInput label, .stSelectbox label, .stDateInput label, .stMultiSelect label, .stSidebar, .stHeader {
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Load the dataset into df_uq
file_path = "C:/Users/rahul/OneDrive/Documents/FORE/Term_1/DEVP/Project/Imports_Exports_Dataset.csv"

try:
    df_uq = pd.read_csv(file_path)

    # Convert the 'Date' column to datetime format
    df_uq['Date'] = pd.to_datetime(df_uq['Date'], errors='coerce')  # Convert with coercion to handle invalid dates

    # Sidebar for user selections
    st.sidebar.header("Filter Options")

    # Multi-select widgets to select variables to visualize
    categorical_options = ['Country', 'Product', 'Import_Export', 'Category', 'Port', 'Shipping_Method', 'Supplier', 'Customer', 'Payment_Terms']
    numeric_options = ['Quantity', 'Value', 'Weight']

    # Allow users to choose categorical variables
    selected_categorical_var = st.sidebar.multiselect(
        'Select Categorical Variables for Visualization',
        categorical_options,
        default=['Import_Export', 'Category', 'Shipping_Method', 'Payment_Terms']  # Default selected
    )

    # Allow users to choose non-categorical variables for scatter plot
    selected_numeric_x = st.sidebar.selectbox(
        'Select X-axis for Scatter Plot (Numeric)',
        numeric_options
    )

    selected_numeric_y = st.sidebar.selectbox(
        'Select Y-axis for Scatter Plot (Numeric)',
        numeric_options,
        index=1  # Default to the second option
    )

    # Allow users to select Date range (optional)
    min_date = df_uq['Date'].min()
    max_date = df_uq['Date'].max()
    date_range = st.sidebar.date_input("Select Date Range:", [min_date, max_date])

    # Filter dataset by selected date range
    if date_range:
        df_uq = df_uq[(df_uq['Date'] >= pd.Timestamp(date_range[0])) & (df_uq['Date'] <= pd.Timestamp(date_range[1]))]

    # Dynamic Pie Charts for selected categorical variables
    st.write("### Categorical Variables - Pie Charts")
    cols = st.columns(2)
    for i, var in enumerate(selected_categorical_var):
        size = df_uq[var].value_counts()
        with cols[i % 2]:  # Display two pie charts side by side
            plt.figure(figsize=(4, 4))
            plt.pie(size, labels=size.index, autopct='%1.1f%%', startangle=140)
            plt.title(f'Pie Chart of {var}', color='black')
            plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
            st.pyplot(plt)
            plt.clf()

    # Bar Plot for Payment Terms
    if 'Payment_Terms' in selected_categorical_var:
        st.write("### Bar Plot - Payment Terms")
        plt.figure(figsize=(10, 6))
        sns.countplot(data=df_uq, x='Payment_Terms', order=df_uq['Payment_Terms'].value_counts().index)
        plt.title('Bar Plot of Payment Terms', color='black')
        plt.xlabel('Payment Terms')
        plt.ylabel('Count')
        plt.xticks(rotation=45)
        st.pyplot(plt)
        plt.clf()

    # Line Chart - Quantity over Time (Date)
    if 'Date' in df_uq.columns and pd.api.types.is_datetime64_any_dtype(df_uq['Date']):
        st.write("### Line Chart - Quantity over Time")
        plt.figure(figsize=(10, 6))
        df_uq.groupby('Date')['Quantity'].sum().plot(kind='line', color='black')
        plt.title('Line Chart of Quantity over Time', color='black')
        plt.xlabel('Date')
        plt.ylabel('Total Quantity')
        plt.grid(True)
        st.pyplot(plt)
        plt.clf()
    else:
        st.warning("The 'Date' column is missing or not in datetime format.")

    # Scatter Plot for selected numeric variables
    st.write(f"### Scatter Plot - {selected_numeric_x} vs {selected_numeric_y}")
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df_uq, x=selected_numeric_x, y=selected_numeric_y)
    plt.title(f'Scatter Plot of {selected_numeric_x} vs {selected_numeric_y}', color='black')
    plt.xlabel(selected_numeric_x)
    plt.ylabel(selected_numeric_y)
    plt.grid(True)
    st.pyplot(plt)
    plt.clf()

    # Box Plot - Value Distribution per Shipping Method
    if 'Shipping_Method' in selected_categorical_var:
        st.write("### Box Plot - Value Distribution per Shipping Method")
        plt.figure(figsize=(10, 6))
        sns.boxplot(data=df_uq, x='Shipping_Method', y='Value')
        plt.title('Box Plot of Value Distribution by Shipping Method', color='black')
        plt.xlabel('Shipping Method')
        plt.ylabel('Value')
        plt.xticks(rotation=45)
        st.pyplot(plt)
        plt.clf()

    # Sidebar filter for heatmap
    st.sidebar.subheader("Heatmap Filter")
    selected_heatmap_vars = st.sidebar.multiselect(
        'Select Numeric Variables for Heatmap',
        numeric_options,
        default=numeric_options  # Default to all
    )

    # Heatmap - Correlation of Selected Numeric Variables
    if selected_heatmap_vars:
        st.write("### Heatmap of Numeric Variables")
        correlation_matrix = df_uq[selected_heatmap_vars].corr()

        plt.figure(figsize=(10, 6))
        sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap='coolwarm', cbar=True, square=True)
        plt.title("Heatmap of Selected Numeric Variables", color='black')
        st.pyplot(plt)
        plt.clf()

except FileNotFoundError:
    st.error(f"File not found at {file_path}. Please check the path and try again.")