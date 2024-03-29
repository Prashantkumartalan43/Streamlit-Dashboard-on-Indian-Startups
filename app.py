
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide", page_title="Startup Analysis")
st.sidebar.image("startup.jpg")
st.image("startup.jpg")

df = pd.read_csv("startup.csv")
# converting date column into datetime object
df["date"] = pd.to_datetime(df["date"], errors="coerce")
# extract month
df["month"] = df["date"].dt.month
# extract year
df["year"] = df["date"].dt.year

st.sidebar.title("Startup Funding Analysis")
option = st.sidebar.selectbox("Select One", ["Overall Analysis", "Startup", "Investor"])

# Getting Overall Analysis
def load_overall_analysis():
    # st.title("Overall Analysis")
    st.markdown("<h1 style='color: red;'>Overall Analysis</h1>", unsafe_allow_html=True)
    # total amount funded
    total_funding = round(df["amount"].sum())

    # Maximum amount funded
    max_funding = df.groupby("startup")["amount"].max().sort_values(ascending=False)[0]

    # average amount funded
    avg_funding = round(df.groupby("startup")["amount"].sum().mean())

    # total funded startups
    total_startups = df["startup"].nunique()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Amount Funded", str(total_funding) + " Cr")
    with col2:
        st.metric("Maximum Amount Funded", str(max_funding) + " Cr")
    with col3:
        st.metric("Average Amount Funded", str(avg_funding) + " Cr")
    with col4:
        st.metric("Total Funded Startups", total_startups)

# Getting Investor details
def load_investor_details(investor_name):
    # st.markdown("<h1 style='color: red;'>investor_name</h1>", unsafe_allow_html=True)
    st.title(investor_name)
    # st.title("Investor Analysis")
    # st.markdown("<h1 style='color: red;'>Investor Analysis</h1>", unsafe_allow_html=True)

    # getting the recent investments by the investor
    recent_five_invests = df[df["investors"].str.contains(investor_name)].head()[["date", "startup", "vertical",
                                                              "city", "round", "amount"]]
    st.subheader("Most Recent Investments")
    st.dataframe(recent_five_invests)

    # getting the biggest investments

    col1, col2 = st.columns(2)

    with col1:
        biggest_investments = df[df["investors"].str.contains(investor_name)].groupby("startup")["amount"].sum().sort_values(
            ascending=False).head()
        st.subheader("Biggest Investments")
        # st.dataframe(biggest_investments)
        # showing the bar graph
        fig, ax = plt.subplots()
        ax.bar(biggest_investments.index, biggest_investments.values)
        st.pyplot(fig)

    with col2:
        investors_sectors = df[df["investors"].str.contains(investor_name)].groupby("vertical")["amount"].sum().\
            sort_values(ascending=False)
        st.subheader("Sectors invested in ")
        fig1, ax1 = plt.subplots()
        ax1.pie(investors_sectors, labels=investors_sectors.index, autopct="%0.01f%%")
        st.pyplot(fig1)

    col3, col4 = st.columns(2)
    # getting the investors invested rounds
    with col3:
        round_info = df[df["investors"].str.contains(investor_name)].groupby("round")["amount"].sum().sort_values(
            ascending=False)
        st.subheader("Invested Rounds")
        fig2, ax2 = plt.subplots()
        ax2.pie(round_info, labels=round_info.index, autopct="%0.01f%%")
        st.pyplot(fig2)

    # getting the investors loved city
    with col4:
        city_info = df[df["investors"].str.contains(investor_name)].groupby("city")["amount"].sum().sort_values(
            ascending=False)
        st.subheader("Invested Cities")
        fig3, ax3 = plt.subplots()
        ax3.pie(city_info, labels=city_info.index, autopct="%0.01f%%")
        st.pyplot(fig3)

    col5, col6 = st.columns(2)
    # getting year-on-year investment made by investors
    with col5:
        df["year"] = df["date"].dt.year
        year_on_year_info = df[df["investors"].str.contains(investor_name)].groupby("year")["amount"].sum()  # plot(grid=True, color="green")
        st.subheader("Year-On-Year Investment")
        fig4, ax4 = plt.subplots()
        ax4.plot(year_on_year_info.index, year_on_year_info.values)
        st.pyplot(fig4)


# Getting Startup details
def load_startup_details(startup_name):
    st.title(startup_name)

    # getting the recent investments in a startup
    investments = df[df["startup"].str.contains(startup_name)].head()[["date", "vertical", "city", "round", "amount"]]
    st.subheader("Investors")
    st.dataframe(investments)

    col1, col2 = st.columns(2)
    # getting the biggest investors
    with col1:
        st.subheader("Top Investors")
        biggest_investors = df[df["startup"].str.contains(startup_name)].groupby("investors")["amount"].sum().sort_values(ascending=False)
        fig, ax = plt.subplots()
        ax.bar(biggest_investors.index, biggest_investors.values)
        st.pyplot(fig)

    # getting the top investors in a given startup
    with col2:
        st.subheader("Investment Rounds")
        if df[df["startup"].str.contains(startup_name)].groupby("round")["amount"].sum().sort_values(ascending=False).any() == 0:
            st.text("Not Disclosed")
        else:
            investment_rounds = df[df["startup"].str.contains(startup_name)].groupby("round")["amount"].sum().sort_values(
                ascending=False)
            fig1, ax1 = plt.subplots()
            ax1.pie(investment_rounds, labels=investment_rounds.index, autopct="%0.01f%%")
            st.pyplot(fig1)

    col3, col4 = st.columns(2)
    # find the city
    with col3:
        st.subheader("City")
        if df[df["startup"].str.contains(startup_name)].groupby("city")["amount"].sum().sort_values(ascending=False).any() == 0:
            st.text("Not Disclosed")
        else:
            invested_city = df[df["startup"].str.contains(startup_name)].groupby("city")["amount"].sum().sort_values(ascending=False)
            fig2, ax2 = plt.subplots()
            ax2.pie(invested_city, labels=invested_city.index, autopct="%0.01f%%")
            st.pyplot(fig2)

    # year by year investment
    with col4:
        df["year"] = df["date"].dt.year
        st.subheader("Year on Year Investment")
        year_by_year_invest = df[df["startup"].str.contains(startup_name)].groupby("year")["amount"].sum()
        invested_city = df[df["startup"].str.contains(startup_name)].groupby("city")["amount"].sum().sort_values(
            ascending=False)
        fig3, ax3 = plt.subplots()
        ax3.plot(year_by_year_invest.index, year_by_year_invest.values)
        st.pyplot(fig3)


# Overall Analysis
if option == "Overall Analysis":
    # st.title("Overall Analysis")
    btn0 = st.sidebar.button("Find Overall Analysis")
    if btn0:
        load_overall_analysis()

# Startup Analysis
elif option == "Startup":
    selected_startup = st.sidebar.selectbox("Select Startup", sorted(df["startup"].unique().tolist()))
    btn1 = st.sidebar.button("Find Startup details")
    # st.title("Startup Analysis")
    st.markdown("<h1 style='color: red;'>Startup Analysis</h1>", unsafe_allow_html=True)
    if btn1:
        load_startup_details(selected_startup)

# Investor Analysis
else:
    selected_investor = st.sidebar.selectbox("Select Investor", sorted(set(df["investors"].str.split(',').sum())))
    btn2 = st.sidebar.button("Find Investors details")
    if btn2:
        load_investor_details(selected_investor)

