from altair.vegalite.v4.schema.channels import Column
import pandas as pd
from pydeck.bindings import map_styles
from pydeck.bindings.map_styles import DARK, LIGHT, ROAD, SATELLITE
import streamlit as st
import plotly.express as px
from urllib.request import urlopen
import json
import pydeck as pdk

def preprocessing():
    df = pd.read_csv("Volcanic Eruptions in the Holocene Period.csv",\
        usecols=["Name","Country","Region","Type","Activity Evidence","Last Known Eruption","Latitude","Longitude","Elevation (Meters)"])
    return df

def main():
    df = preprocessing()
    with st.expander("Click for view dataset"):
        st.dataframe(df)
    with st.container():
        cols = st.columns([2,1])
        with cols[0]:
            filt_activity = st.sidebar.selectbox("Choose volcans by Activity type", df["Activity Evidence"].unique())
            chart_data = df.query("`Activity Evidence` == @filt_activity")
            chart = px.histogram(data_frame=chart_data,x="Country",title="Count of Volcanic by {}".format(filt_activity))
            st.plotly_chart(chart,True)
            chart_data = df[["Longitude","Latitude","Activity Evidence"]].query("`Activity Evidence` == @filt_activity").dropna()
            lays = pdk.Layer(
                "TextLayer",\
                chart_data,\
                get_text="Name",\
                get_size=16,\
                get_position=["Longitude","Latitude"])
            st.pydeck_chart(pdk.Deck(layers=[lays],tooltip={f"text":"{Name}"}))
        with cols[1]:
            filt_country = st.sidebar.selectbox("Choose volcans by Country type", df["Country"].unique())
            chart_data = df.query("`Country`==@filt_country")
            chart = px.pie(data_frame=chart_data,names="Activity Evidence",title="Distribution of Volcanic type by {}".format(filt_country))
            st.plotly_chart(chart,True)
        
if __name__=='__main__':
    main()