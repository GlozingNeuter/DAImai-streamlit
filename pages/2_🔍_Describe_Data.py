#!/usr/bin/env python3
import streamlit as st
import pandas as pd
import folium
import datetime

st.markdown( "### Describe your dataset so it can be properly interpreted")

starting_date = datetime.date(1980,1,1)

@st.cache_data
def update_df(dataframe, color, name, point_type):
    dataframe["color"] = color
    dataframe["name"] = name
    dataframe["type"] = point_type
    dataframe["date"] = date
    return dataframe

col1, col2 = st.columns(2)
with col1 :
    color = st.color_picker('Couleur des points', '#00f900')
with col2 :
    point_type = st.radio("Type de données", ["Liste de lecteurs", "Liste de magasins", "Liste de clubs", "Autre"])

name = st.text_input("Nom des données", value="New layer", max_chars=50)
date = st.date_input("Séléctionner une date", value = starting_date )
uploaded_file = st.file_uploader("Ajouter des données")
if uploaded_file is not None:
    dataframe = pd.read_csv(uploaded_file)
    df = update_df(dataframe,color,name,point_type)
    st.write(df)
    print(df)
    csv = df.to_csv().encode("utf-8")
    st.download_button(label="Download edited dataframe",data = csv ,mime="text/csv")
