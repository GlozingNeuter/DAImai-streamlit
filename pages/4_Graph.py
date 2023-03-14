#!/usr/bin/env python3

import streamlit as st
import pandas as pd
import pydeck as pdk


club_dict = {
    "BX": [44.841225, -0.5800364],
    "DCA":[48.8588897, 2.320041],
    "IDC Liège" :[0,0],
    "IDC Charleroi":[0,0],
    "D.A.I.C":[0,0],
}


dataframe = pd.read_csv("../data/out/daiclic_geo.csv")
def clubmap(data):
    for index, row in data.iterrows():
        club = ""
        location = [row["lat"], row["lng"]]
        if "Club" in data.columns:
            club = row["Club"]
        if club in club_dict.keys() and pd.isna(row["Club"]):
            club_loc = club_dict[club]
            arc_layer = pdk.Layer(
                "Club_ArcLayer",
                data = data,
                get_width=50,
                get_source_position=location,
                get_target_position=club_loc,
                get_tilt=15,
                pickable=True,
                auto_highlight=True,
            )
            view_state = pdk.ViewState(latitude=45.5, longitude=6, bearing=45, pitch=50, zoom=7,)
            TOOLTIP_TEXT = {"html": "{S000} jobs <br /> Home of commuter in red; work location in green"}
            r = pdk.Deck(arc_layer, initial_view_state=view_state, tooltip=TOOLTIP_TEXT)
            return r

map = clubmap(dataframe)
st.pydeck_chart(map)
