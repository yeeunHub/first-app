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

# pivot data
df3=df2.pivot(index='Year', columns='Entity', values='Individuals using the Internet (% of population)')

# Add title and header
st.title("Cool Internet Speed Map")
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

st.header("GDP")
df4=df1[['Entity','Year','Individuals using the Internet (% of population)','gdpPercap']]
fig1 = px.choropleth_mapbox(df4, 
                           geojson=geo_ds, 
                           color="gdpPercap",
                           locations="Entity", 
                           featureidkey="properties.ADMIN",  #the point for combining the two data sets "geojson", 'ds'
                           center={"lat": 35.9078, "lon": 127.7669},
                           mapbox_style="carto-positron", zoom=2)
st.plotly_chart(fig1)


# st.header("Multigroup Regression analysis between GDP and internet usage")

# import seaborn as sns

# #create scatterplot with regression line
# import seaborn as sns
# sns.set()
# sns.set_style('whitegrid')

# countries = ['China','Japen']
# df5 = df4[df4['Entity'].isin(countries)]
# # sns.lmplot(x="year", y="pop", data=europeData, hue='country',
# #    order=2, ci=False)
# fig2 = sns.regplot(data=df5, x='gdpPercap', y='Individuals using the Internet (% of population)', ci=None)
# st.pyplot(fig2)