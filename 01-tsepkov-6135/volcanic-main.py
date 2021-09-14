from curses import color_content
from turtle import color
import pandas as pd
import streamlit as st
import plotly.express as px
import pydeck as pdk
from pydeck.types import String

st.set_page_config(
    page_title="Vulcans visualization",
    layout="wide"
)

def preprocessing():
    df = pd.read_csv("Volcanic Eruptions in the Holocene Period.csv",\
        usecols=["Name","Country","Region","Type","Activity Evidence","Last Known Eruption","Latitude","Longitude","Elevation (Meters)"],dtype={
            "Name":str,
            "Country":str,
            "Region":str,
            "Type":str,
            "Activity Evidence":str,
            "Last Known Eruption":str,
            "Latitude":float,
            "Longitude":float,
            "Elevation (Meters)":int
        })
    df["Eruption"]=df["Last Known Eruption"].map(lambda x: False if x == "Unknown" else True)
    return df.dropna()

def main():
    df = preprocessing()
    with st.expander("Click for view dataset"):
        st.dataframe(df)
    with st.container():
        chart = pdk.Deck(
            layers=pdk.Layer(
                "HeatmapLayer",
                df,
                get_position=["Longitude","Latitude"],
                auto_highlight=True,
                get_radius=1,          # Radius is given in meter
                pickable=True,
            )
        )
        st.pydeck_chart(chart,True)
        
    with st.container():
        region = st.selectbox("Select region", df["Region"].unique())
        source = df.query("Region == @region")
        with st.expander("Describe"):
            chart = px.scatter_mapbox(source, lat="Latitude", lon="Longitude",
                color="Eruption",
                size_max=15, zoom=2,
                mapbox_style="carto-positron")
            st.plotly_chart(chart,True)
        cols = st.columns([2,1])
        with cols[0]:
            chart = px.bar(data_frame=source.groupby(["Country","Elevation (Meters)","Name"]).agg({"Name":"count"}).rename(columns={"Name":"Count vulcans"}).sort_values("Elevation (Meters)",ascending=False).reset_index(),x="Country", y="Count vulcans",color="Elevation (Meters)",hover_data=["Elevation (Meters)","Name"])
            st.plotly_chart(chart, True)
        with cols[1]:
            chart = px.sunburst(data_frame=source, path=["Country","Activity Evidence","Type"], hover_data=["Last Known Eruption"])
            st.plotly_chart(chart, True)
        with st.expander("Top vulcans by {}".format(region)):
            count = st.slider("Quntity vulcans for view", min_value=5,max_value=source.shape[0])
            source = source.sort_values("Elevation (Meters)", ascending=False).iloc[:count]
            chart = px.bar(data_frame=source, x="Name", y="Elevation (Meters)", color="Activity Evidence")
            st.plotly_chart(chart, True)
if __name__=='__main__':
    main()