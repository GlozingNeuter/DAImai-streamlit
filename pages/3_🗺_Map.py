#!/usr/bin/env python3

import streamlit as st
from streamlit_folium import st_folium, folium_static
import pandas as pd
import folium
from folium.plugins import GroupedLayerControl, BeautifyIcon, AntPath

icon_dict = {
    "Liste de lecteurs": "user",
    "Liste de magasins": "shop",
    "Liste de clubs": "people-roof",
    "Autre": "circle",
}

club_dict = {
    "BX": [44.841225, -0.5800364],
    "DCA": [48.8588897, 2.320041],
    "IDC Liège": [50.640108, 5.5708564],
    "CARO": [50.4062694, 4.442313],
    "DAIC": [50.8113254, 4.3382402],
}


def map_df(data):
    m = folium.Map(location=[45.5, 6], tiles="cartodbpositron", zoom_start=5)
    for index, row in data.iterrows():
        if pd.isna(row["lat"]) is False and pd.isna(row["lng"]) is False:
            if 35 > int(row["lng"]) > -20:  # Solution temporaire pour éliminer les erreurs de géocodage
                boutique = ""
                clubs = []
                if "Boutique" in data.columns:
                    boutique = row["Boutique"]
                if "Club" in data.columns:
                    if "/" in str(row["Club"]):
                        clubs = row["Club"].split("/")
                    else:
                        clubs.append(row["Club"])

                city = row["Ville"]
                date = row["date"]
                img = ""
                html = f"""
                <img src="{img}"> <br>
                <b>{date} </b><br>
                {city} <br>
                {boutique}{clubs}
                """
                iframe = folium.IFrame(html)
                popup = folium.Popup(iframe, min_width=200, max_width=300)
                location=[row["lat"], row["lng"]]
                color = row["color"]
                icon_type = icon_dict[row["type"]]
                folium.Marker(
                    location=location,
                    popup=popup,
                    icon=BeautifyIcon(border_color=color,
                                      prefix="fa",
                                      icon=icon_type)
                ).add_to(m)

                for club in clubs:
                    if club in club_dict.keys():
                        club_loc = club_dict[club]
                        AntPath([location,club_loc],
                                hardwareAccelerated=True,
                                delay=800).add_to(m)
    return m


m = folium.Map(location=[45.5, 6], tiles="cartodbpositron", zoom_start=5)
st.markdown("### Map of points of interest")
if hasattr(st.session_state, "df"):
    df = st.session_state.df
    m = map_df(df)
else:
    st.markdown("Load data to add point to the map")
st_data = folium_static(m, height=700, width=800)
