import streamlit as st
from connection import get_coretemp_data
import pandas as pd
import altair as alt

def create_dashboard():
    st.title("Dashboard")
    st.write("Welcome to the dashboard!")

    df = get_coretemp_data()


if __name__ == "__main__":
    create_dashboard()