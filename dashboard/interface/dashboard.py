import streamlit as st
from connection import get_coretemp_data

def create_dashboard():
    st.title("Dashboard")
    st.write("Welcome to the dashboard!")

    df = get_coretemp_data()
    print(df)

if __name__ == "__main__":
    create_dashboard()