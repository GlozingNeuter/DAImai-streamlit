#!/usr/bin/env python3

import streamlit as st
import pandas as pd
from geopy import OpenCage

def clean_db(db) :
    """
    Nettoie une dataframe en adaptant le nom des pays selon ISO 3166 et retire les numéros de rue des adresses
    """

    country = { "Belgique" : "BE",
                "BELGIQUE" : "BE",
                "FRANCE" : "FR",
                "France" : "FR",
                "FRANCE" : "FR",
                "SPAIN" : "ES",
                "ENGLAND" : "UK",
                "ITALIA" : "IT",
                "SPAIN" : "ES",
                "SCHEWEIZ" : "CH",
                "SUISSE" : "CH",
                "SWISSE" : "CH",
                "SWISS" : "CH",
                "Swisse" : "CH",
                "W. GERMANY" : "DE",
                "W. Germany" : "DE",
                "DEUTSCHLAND" : "DE",
                "DEUTSCHLAND" : "DE",
                "R.F.A" : "DE",
                "Nederland" : "NL",
                "IRELAND" : "IE",
                "ITALY" : "IT",
                "Italie" : "IT",
                "N64 4GE ENGLAND" : "UK",
                "BUNDESREP. DEUTSCHLAND" : "DE",
                "SCOTLAND" : "UK",
                "YUGOSLAVIA" : "HR",
                "SCOTLAND ML2 OOR" : "UK",
                "Scotland" : "UK",
                "LUXEMBOURG" : "LU",

                }
    db["Adresse_short"] = ""
    for index, row in db.iterrows():
        row["Adresse_short"] = "".join([i for i in str(row["Adresse"]).split(" ") if i.isdigit() == False])


    db["Country"] = db["Pays"].map(country)
    db = db.drop(columns="Adresse")
    return db

def geocode_opencage(data, api_key="13d6984effa44de6b0e21d572f69cab2"):

    """
    Géocode les adresse d'une dataframe avec l'API OpenCage.
    Utilise les séries Adresse_short, Country et en option un série Ville pour ajouter les séries lng et lat.
    """

    for index, row in data.iterrows():
        st.progress(text = "Geocoding anonymized addresses", value = index)
        geolocator = OpenCage(api_key=api_key)
        geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
        address = row['Adresse_short']
        # postal_code = row['postal_code']
        country = row['Country']
        if "Ville" in data.columns:
            city = row['Ville']
        else:
            city = ""
        query = {"street" : address,
                 "city" : city,
                 "country" : country}
        full_address = str(address) + ' '  + str(city) + ' ' + str(country)
        # location = geocode(query)
        location = geocode(full_address)

        if location is not None:
            print(location.latitude, location.longitude)
            data.loc[index, 'lat'] = location.latitude
            data.loc[index, 'lng'] = location.longitude
        else:



            print('Not found')
    return data


file = st.file_uploader(label="Dataframe to prepare")

df = pd.read_csv(file)

st.write(clean_db(df))


api = st.text_input(label="OpenCage API key")
st.button(label="Geocode dataframe",on_click=geocode_opencage,kwargs={"data": df, "api_key":api})
