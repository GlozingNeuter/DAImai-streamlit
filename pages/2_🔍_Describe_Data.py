#!/usr/bin/env python3
import streamlit as st
import pandas as pd
import folium


df_init = pd.DataFrame()
df = pd.DataFrame()
df_old = pd.DataFrame()


def callback(dataframe, color, name, option,df_old):
    dataframe["color"] = color
    dataframe["name"] = name
    dataframe["option"] = option
    table.add_rows(dataframe)


    uploaded_file = None

edited_df = st.experimental_data_editor(df, num_rows= "dynamic")
table = st.dataframe()
with st.expander("Ajouter des données"):
    col1, col2 = st.columns(2)
    with col1 :
        color = st.color_picker('Couleur des points', '#00f900')
    with col2 :
        option = st.radio("Type de données", ["Liste de lecteurs", "Liste de magasins", "Liste de clubs", "Autre"])

    name = st.text_input("Nom des données", value="New layer", max_chars=50)

    uploaded_file = st.file_uploader("Ajouter des données")
    if uploaded_file is not None:
        dataframe = pd.read_csv(uploaded_file)
        st.write(dataframe)
        st.button("Ajouter",on_click= callback(dataframe,color,name,option,df_old))

st.download_button(data=df,mime="text/csv")
