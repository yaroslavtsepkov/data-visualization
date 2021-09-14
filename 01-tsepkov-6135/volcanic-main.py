import pandas as pd
import streamlit as st
import plotly.express as px

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
    return df

def main():
    df = preprocessing()
    with st.expander("Click for view dataset"):
        st.dataframe(df)
    with st.container():
        source = df.groupby(["Country"]).agg({"Name":"count"}).sort_values("Name",ascending=False).reset_index().rename(columns={"Name":"Count vulcans"})
        
        temp = st.sidebar.slider("Count country on Histogram",min_value=10, max_value=source.shape[0])
        chart = px.bar(data_frame=source.iloc[:temp],x="Country",y="Count vulcans",title="Distributed vulcans by World")
        st.plotly_chart(chart, True)
        
    with st.container():
        region = st.sidebar.selectbox("Select region", df["Region"].unique())
        source = df.query("Region == @region")
        cols = st.columns([2,1,1])
        with cols[0]:
            chart = px.bar(data_frame=source.groupby(["Country"]).agg({"Name":"count"}).rename(columns={"Name":"Count vulcans"}).sort_values("Count vulcans",ascending=False), y="Count vulcans")
            st.plotly_chart(chart, True)
        with cols[1]:
            chart = px.pie(data_frame=source, names="Type")
            st.plotly_chart(chart, True)
        with cols[2]:
            chart = px.pie(data_frame=source, names="Activity Evidence")
            st.plotly_chart(chart, True)
    

if __name__=='__main__':
    main()