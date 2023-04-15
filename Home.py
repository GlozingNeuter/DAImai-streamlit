#!/usr/bin/env python3

import streamlit as st
from streamlit_folium import st_folium, folium_static
import pandas as pd
import folium
from folium.plugins import GroupedLayerControl, BeautifyIcon, AntPath
import streamlit as st

st.set_page_config(
    page_title="Hello",
    )

st.markdown(
    """
    # DAImap

    ### Tool to map archive data

    """
)
st.components.v1.iframe("https://kipple.be/d3-fig/map.html", height=700)

