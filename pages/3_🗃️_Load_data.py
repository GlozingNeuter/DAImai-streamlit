#!/usr/bin/env python3

import streamlit as st
import pandas as pd
import folium


uploaded = st.file_uploader("Importer des fichiers CSV", type="csv", accept_multiple_files=True)

df_full = pd.DataFrame()

for file in uploaded:
    df = pd.read_csv(file)
    df["table"] = str(file.name)
    df_full = pd.concat([df_full, df])

st.write(df_full)
