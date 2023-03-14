#!/usr/bin/env python3

import streamlit as st
from streamlit_folium import st_folium, folium_static
import pandas as pd
import folium
from folium.plugins import GroupedLayerControl, BeautifyIcon, AntPath




m = folium.Map(location = [45.5,6], tiles = "cartodbpositron", zoom_start = 5)

dainamic_geo = pd.read_csv("../data/out/dainamic1986_geo.csv")
daiclic_geo = pd.read_csv("../data/out/daiclic_geo.csv")
daiclic2_geo = pd.read_csv("../data/out/newdaiclic_geo.csv")
revendeurs_geo = pd.read_csv("../data/out/revendeurs_geo.csv")

club_dict = {
    "BX": [44.841225, -0.5800364],
    "DCA":[48.8588897, 2.320041],
    "IDC Liège" :[],
    "IDC Charleroi":[],
    "D.A.I.C":[],
}

def addtomap(data,name,color="red",show = False, img="",date ="", icon = "info-sign")  :
    name = ""
    city = ""
    feature_group = folium.FeatureGroup(name=name, show=show)
    for index, row in data.iterrows():
        if pd.isna(row["lat"]) == False and pd.isna(row["lng"]) == False:
            if 35 > row["lng"] > -20 :
                boutique = ""
                club = ""
                if "Boutique" in data.columns :
                    boutique = row["Boutique"]
                if "Club" in data.columns:
                    club = row["Club"]

                city = row["Ville"]
                html=f"""
                <img src="{img}"> <br>
                <b>{date} </b><br>
                {city} <br>
                {boutique}{club}
                """
                iframe = folium.IFrame(html)
                popup = folium.Popup(iframe, min_width=200, max_width=300)
                location=[row["lat"], row["lng"]]
                folium.Marker(
                location=location,
                popup=popup,
                icon=BeautifyIcon(border_color=color, prefix="fa", icon=icon)
                ).add_to(feature_group)

                if club in club_dict.keys():
                    club_loc = club_dict[club]
                    AntPath([location,club_loc], hardwareAccelerated=True, delay=800).add_to(feature_group)

    return feature_group

dainamic_markers = addtomap(
    data=dainamic_geo,
    name="DAInamic:12-1986",
    color="red",
    show = True,
    img="https://i.imgur.com/VjoBThG.png",
    date = "décembre 1986",
    icon = "user"
    )
m.add_child(dainamic_markers)

daiclic_markers = addtomap(
    data=daiclic_geo,
    name="DAIclic:12-1986",
    color="green",
    img="https://i.imgur.com/QptchDT.png",
    date="décembre 1986",
    icon = "user"
    )
m.add_child(daiclic_markers)

daiclic2_markers = addtomap(
    data=daiclic2_geo,
    name="DAIclic:1988",
    color="blue",
    img="https://i.imgur.com/QptchDT.png",
    date="1988",
    icon = "user"
    )
m.add_child(daiclic2_markers)

revendeurs_markers = addtomap(
    data=revendeurs_geo,
    name="Revendeurs",
    color="orange",
    img="",
    date="1981-1982",
    icon = "shop"
    )
m.add_child(revendeurs_markers)
st_data=folium_static(m, height = 700, width = 800)
