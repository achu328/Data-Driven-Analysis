import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import pymysql as db

# Database connection
db_cnct = db.connect(
    host='127.0.0.1',
    port=3306,
    database="mat1",
    user="mat",
    password='Durairaj@66'
)
curr = db_cnct.cursor()

# Function to fetch data
def fetch_data(query):
    curr.execute(query)
    data = curr.fetchall()
    columns = [desc[0] for desc in curr.description]
    return pd.DataFrame(data, columns=columns)

# Fetch all tables
volatility_df = fetch_data("SELECT * FROM mat1.volatility")
cumulative_df = fetch_data("SELECT * FROM mat1.cumulative")
sector_df = fetch_data("SELECT * FROM mat1.sector")
correlation_df = fetch_data("SELECT * FROM mat1.stock_correlation")
gainer_df = fetch_data("SELECT * FROM mat1.gainer")


# Sidebar Navigation
r = st.sidebar.radio("Navigation", ["Home", "Data Analysis"])

if r == "Home":
    st.title('Data Driven Stock Analysis')
    st.write("Welcome to the Data Driven Stock Analysis")
    st.image(r"C:\Users\achu1\Downloads\stock.jpg")

elif r == "Data Analysis":
    option = st.selectbox("Select a Visualization:", [
        "1. Volatility Analysis",
        "2. Cumulative Return Over Time",
        "3. Sector-wise Performance",
        "4. Stock Price Correlation",
        "5. Top 5 Gainers and Losers (Month-wise)"
    ])

    if option == "1. Volatility Analysis":
        st.header("Volatility Analysis")
        st.write(volatility_df)

        fig, ax = plt.subplots(figsize=(12, 6))
        ax.bar(volatility_df["Ticker"], volatility_df["Volatility"], color="red")
        ax.set_xlabel("Stock Ticker")
        ax.set_ylabel("Volatility (Standard Deviation of Daily Returns)")
        ax.set_title("Top 10 Most Volatile Stocks Over the Past Year")
        st.pyplot(fig)

    elif option == "2. Cumulative Return Over Time":
        st.header("Cumulative Return Over Time")
        cumulative_df["date"] = pd.to_datetime(cumulative_df["date"])
        st.write(cumulative_df)
        
        fig, ax = plt.subplots(figsize=(10,4))
        for ticker in cumulative_df["Ticker"]:
             stock_data = cumulative_df[cumulative_df["Ticker"] == ticker]
             ax.plot(stock_data["date"], stock_data["cumulative_return"], label=ticker, marker="o")
        ax.set_xlabel("Date")
        ax.set_ylabel("Cumulative Return")
        ax.set_title("Cumulative Return of Top 5 Performing Stocks Over the Year")
        ax.legend()
        ax.grid(True, linestyle="--", alpha=0.7)
        st.pyplot(fig)


    elif option == "3. Sector-wise Performance":
        st.header("Sector-wise Performance")
        st.write(sector_df)

        fig, ax = plt.subplots(figsize=(12, 6))
        sns.barplot(x="Sector", y="Yearly_Return", data=sector_df, palette="coolwarm", ax=ax)
        ax.set_xlabel("Sector")
        ax.set_ylabel("Average Yearly Return (%)")
        ax.set_title("Average Yearly Return by Sector")
        st.pyplot(fig)

    
    elif option == "4. Stock Price Correlation":
        st.header("Stock Price Correlation")
        correlation_matrix = correlation_df.set_index("Ticker").corr()
        st.write(correlation_df)

        fig, ax = plt.subplots(figsize=(60,30))  
        sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5, ax=ax)
        ax.set_title("Stock Price Correlation Matrix")
        st.pyplot(fig)


    elif option == "5. Top 5 Gainers and Losers (Month-wise)":
        st.header("Top 5 Gainers and Losers (Month-wise)")
        st.write(gainer_df)
        months = gainer_df["month"].unique()

        for month in months:
            fig, axes = plt.subplots(1, 2, figsize=(12, 5))

            gainers = gainer_df[gainer_df["month"] == month].nlargest(5, "Monthly_Return")
            losers = gainer_df[gainer_df["month"] == month].nsmallest(5, "Monthly_Return")

            sns.barplot(y=gainers["Ticker"], x=gainers["Monthly_Return"], palette="Greens_r", ax=axes[0])
            axes[0].set_title(f"Top 5 Gainers - {month}")

            sns.barplot(y=losers["Ticker"], x=losers["Monthly_Return"], palette="Reds_r", ax=axes[1])
            axes[1].set_title(f"Top 5 Losers - {month}")

            st.pyplot(fig)
