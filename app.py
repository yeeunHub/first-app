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
import seaborn as sns
sns.set()
sns.set_style('whitegrid')
import matplotlib.pyplot as plt

# Loading the data
def load_data(path):
    df = pd.read_csv(path)
    return df

internet_df_raw = load_data(path="data/share-of-individuals-using-the-internet.csv")
internet_df = deepcopy(internet_df_raw)
data = px.data.gapminder()
new_df = pd.merge(internet_df, data,  how='left', left_on=['Entity','Year'], right_on = ['country','year'])

# Data cleaning
df1=new_df[(new_df['Entity']=="North Korea") | (new_df['Entity']=="South Korea") | (new_df['Entity']=="China")| (new_df['Entity']=="Japan")]
df2=df1[['Entity','Year','Individuals using the Internet (% of population)']]
df5=new_df[['Entity','Year','Individuals using the Internet (% of population)','gdpPercap']]
df5=df5[(df5['Year']==1992)| (df5['Year']==1997)| (df5['Year']==2002)|(df5['Year']==2007)]

# pivot data
df3=df2.pivot(index='Year', columns='Entity', values='Individuals using the Internet (% of population)')

# Add title and header
st.title("Internet across the world")
st.header("Choropleth Map")

# Creat checkbox for showing the dataframe

df_type=st.checkbox("Data", ["df2"])
if df_type:
    st.dataframe(data=df3)


with open("data/countries.geojson") as response:
    geo_ds = json.load(response)

st.header("Internet")
year=st.selectbox('Year',[1990,2000,2018])

# st.dataframe(data=new_df[new_df['Year']==year])

fig = px.choropleth_mapbox(df2, 
                           geojson=geo_ds, 
                           color="Individuals using the Internet (% of population)",
                           locations="Entity", 
                           featureidkey="properties.ADMIN",  #the point for combining the two data sets "geojson", 'ds'
                           center={"lat": 35.9078, "lon": 127.7669},
                           mapbox_style="carto-positron", zoom=2)
st.plotly_chart(fig)

st.header("Association between GDP and internet usage")

lm = sns.lmplot(x="gdpPercap", y="Individuals using the Internet (% of population)", hue="Year", data=df5,
                     height=9, aspect=1.6, robust=True, palette='tab10',
                     scatter_kws=dict(s=100, linewidths=.9, edgecolors='black'))



st.pyplot(lm)