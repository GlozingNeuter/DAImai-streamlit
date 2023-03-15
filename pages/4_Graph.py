#!/usr/bin/env python3

import streamlit as st
import pandas as pd
import pydeck as pdk
import numpy as np

club_dict = {
    "BX": [44.841225, -0.5800364],
    "DCA":[48.8588897, 2.320041],
    "IDC Liège" :[50.640108, 5.5708564],
    "CARO":[50.4062694, 4.442313],
    "DAIC":[50.8113254, 4.3382402],
}
df = st.session_state.df



chart_data = pd.DataFrame(
   np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
   columns=['lat', 'lon'])

st.pydeck_chart(pdk.Deck(
    map_style=None,
    initial_view_state=pdk.ViewState(
        latitude=37.76,
        longitude=-122.4,
        zoom=11,
        pitch=50,
    ),
    layers=[
        pdk.Layer(
           'HexagonLayer',
           data=chart_data,
           get_position='[lon, lat]',
           radius=200,
           elevation_scale=4,
           elevation_range=[0, 1000],
           pickable=True,
           extruded=True,
        ),
        pdk.Layer(
            'ScatterplotLayer',
            data=chart_data,
            get_position='[lon, lat]',
            get_color='[200, 30, 0, 160]',
            get_radius=200,
        ),
    ],
))


def clubmap(data):
    df = data.dropna(subset=["Club"])
    df_cleaned = pd.DataFrame()
    for index, row in df.iterrows():
        if pd.isna(row["lat"]) == False and pd.isna(row["lng"]) == False:
            if 35 > int(row["lng"]) > -20 : # Solution temporaire pour éliminer les erreurs de géocodage

                club = ""
                row["location"] = [row["lat"], row["lng"]]
                if "Club" in df.columns.values:
                    club = row["Club"]
                    if club in club_dict.keys():
                        row["club_lng"] = float(club_dict[club][1])
                        row["club_lat"] = float(club_dict[club][0])
                        df_cleaned = df_cleaned.append(row)
    #cleaned_df = df[df["Club"].isin(club_dict.keys())]
    st.write(df_cleaned[["lng","lat","club_lng","club_lat"]])
    return df_cleaned

df_cleaned = clubmap(df)

GREEN_RGB = [0, 255, 0, 40]
RED_RGB = [240, 100, 0, 40]

st.pydeck_chart(pdk.Deck(
    map_style=None,
    initial_view_state = pdk.ViewState(latitude=45.5, longitude=6, pitch=50, zoom=4,),
    layers = [ pdk.Layer("ArcLayer",
                          data = df_cleaned[["lng","lat","club_lng","club_lat"]],
                          get_source_position=["lng","lat"],
                          get_target_position=["club_lng","club_lat"],
                          get_source_color=RED_RGB,
                          get_target_color=GREEN_RGB,
                          get_width=7,
                       ),
              ],
    ))
