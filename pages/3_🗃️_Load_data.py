#!/usr/bin/env python3

import streamlit as st
import pandas as pd


st.markdown("### Upload CSV files 👇 ")


@st.cache_data
def load_data(files):
    df_full = pd.DataFrame()

    for file in files:
        df = pd.read_csv(file)
        df["table"] = str(file.name)
        df_full = pd.concat([df_full, df])
    return df_full


uploaded_files = st.file_uploader("Upload CSV files",
                                  type="csv",
                                  key='file_uploader',
                                  accept_multiple_files=True)

if uploaded_files is not None:
    df_full = load_data(uploaded_files)
    st.session_state['df'] = df_full
if df_full is not None:
    st.write(df_full)

with st.sidebar:
    for file in uploaded_files:
        name = pd.read_csv(file)["name"][0]
        st.checkbox(label=name)
