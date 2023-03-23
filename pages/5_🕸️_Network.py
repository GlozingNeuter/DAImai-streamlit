#!/usr/bin/env python3
import pandas as pd
import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config
from uuid import uuid4
size=25
nodes = []
edges = []
if hasattr(st.session_state, "df"):
    df = st.session_state.df

    if "Club" in df.columns.values :

        for value in list(df["Club"].unique()):
            nodes.append( Node(id = str(value),
                            size = size,
                            color = "red",
            ) )
        for index, row in df.iterrows():
            clubs = []
            row["uuid"] = str(uuid4())
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
    else :
        st.markdown("No data to map regarding club affiliation")
    config = Config(width=750,
                    height=950,
                    directed=True,
                    physics=True,
                    hierarchical=False,
                    )

    return_value = agraph(nodes=nodes,
                        edges=edges,
                        config=config)
else:
    st.markdown("Load data first to see the network graph")
