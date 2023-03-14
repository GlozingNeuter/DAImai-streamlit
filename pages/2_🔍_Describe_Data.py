#!/usr/bin/env python3
import streamlit as st
import pandas as pd
import folium


st.markdown( "### Describe your dataset so it can be properly interpreted")

df = pd.DataFrame()
df_old = pd.DataFrame()

@st.cache_data
def callback(dataframe, color, name, option,df_old):
    table = st.dataframe()
    dataframe["color"] = color
    dataframe["name"] = name
    dataframe["option"] = option
    table.add_rows(dataframe)


col1, col2 = st.columns(2)
with col1 :
    color = st.color_picker('Couleur des points', '#00f900')
with col2 :
    option = st.radio("Type de données", ["Liste de lecteurs", "Liste de magasins", "Liste de clubs", "Autre"])

name = st.text_input("Nom des données", value="New layer", max_chars=50)

uploaded_file = st.file_uploader("Ajouter des données")
if uploaded_file is not None:
    dataframe = pd.read_csv(uploaded_file)
    callback(dataframe,color,name,option,df_old)
    st.download_button(label="Download edited dataframe",data=df.to_csv(),mime="text/csv")
