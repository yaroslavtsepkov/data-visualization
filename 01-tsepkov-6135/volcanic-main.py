from altair.vegalite.v4.schema.channels import Column
from numpy import angle
import pandas as pd
from pydeck.bindings import map_styles
from pydeck.bindings.map_styles import DARK, LIGHT, ROAD, SATELLITE
import streamlit as st
import altair as alt
from urllib.request import urlopen
import json
import pydeck as pdk
from sympy import source

st.set_page_config(
    page_title="Vulcans visualization",
    layout="wide"
)

def preprocessing():
    df = pd.read_csv("Volcanic Eruptions in the Holocene Period.csv",\
        usecols=["Name","Country","Region","Type","Activity Evidence","Last Known Eruption","Latitude","Longitude","Elevation (Meters)"])
    df = df.dropna()
    return df

def main():
    df = preprocessing()
    with st.expander("Click for view dataset"):
        st.dataframe(df)
    with st.container():
        source = df.groupby(["Country"]).agg({"Name":"count"}).sort_values("Name",ascending=False).iloc[:10].reset_index()
        chart = alt.Chart(source,title="Top 10 country by count vulcans").mark_bar().encode(
            x=alt.X("Country:N", sort="-y"),y=alt.Y("Name:Q")
        )
        text = chart.mark_text(
            align="center",
            baseline="middle",
            dy=15,
        ).encode(
            text="Name:Q",
            color=alt.ColorValue("white")
        )
        cols = st.columns([3,1])
        with cols[0]:
            st.altair_chart(chart+text, True)
        with cols[1]:
            st.altair_chart(
                alt.Chart(source).mark_bar().encode(
                    x=alt.X("Name:N"), y=alt.Y("Elevation (Meters):Q")
                ),True
            )


if __name__=='__main__':
    main()