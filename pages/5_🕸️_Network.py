#!/usr/bin/env python3
import pandas as pd
import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config
from uuid import uuid4
df = st.session_state.df
size=25
nodes = []
edges = []

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
    df = load_data(uploaded_files).reindex()
    df['uuid'] = df.apply(lambda _: str(uuid4()), axis=1)


st.write(df)

for value in list(df["Club"].unique()):
    nodes.append( Node(id = str(value),
                       size = size,
                       color = "red",
    ) )

for index, row in df.iterrows():
    clubs = []
    if pd.isna(row["Club"]) == False:
        nodes.append( Node(id=row["uuid"],
                           size=size
                           ) )
        if "/" in str(row["Club"]):
            clubs = row["Club"].split("/")
        else:
            clubs.append(row["Club"])
        for club in clubs:
            edges.append( Edge(source=row["uuid"],
                                label="Member of",
                                target=club,
                                )
                        )

config = Config(width=750,
                height=950,
                directed=True,
                physics=True,
                hierarchical=False,
                )

return_value = agraph(nodes=nodes,
                      edges=edges,
                      config=config)
