# Streamlit live coding script
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from urllib.request import urlopen
import json
from copy import deepcopy
from plotly.subplots import make_subplots

# First some MPG Data Exploration
# @st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    return df


internet_df_raw = load_data(path="share-of-individuals-using-the-internet.csv")
internet_df = deepcopy(internet_df_raw)

# Add title and header
st.title("Cool Internet Speed Map")
st.header("Choropleth Map")

# Creat checkbox for showing the dataframe

df_type=st.checkbox("Data", ["Internet_df"])

if df_type:
    #st.dataframe(data=mpg_df)
    st.table(data=internet_df)






