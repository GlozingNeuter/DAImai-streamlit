#!/usr/bin/env python3

import streamlit as st
import pandas as pd
import folium


st.markdown('### **1️⃣ Upload CSV files 👇 **')

@st.cache_data
def load_data(files) :

    df_full = pd.DataFrame()

    for file in files:
        df = pd.read_csv(file)
        df["table"] = str(file.name)
        df_full = pd.concat([df_full, df])
    return df_full

uploaded_files = st.file_uploader("Upload CSV files", type="csv", key='file_uploader', accept_multiple_files=True)

if uploaded_files is not None:
    df_full = load_data(uploaded_files)


st.write(df_full)

if 'df' not in st.session_state:
    st.session_state['df'] = df_full
