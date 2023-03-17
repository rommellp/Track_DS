import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


Data48  = pd.read_csv("merged_400m_800m_df.csv")
Data415 = pd.read_csv("merged_400m_1500m_df.csv")
Data416 = pd.read_csv("merged_400m_1600m_df.csv")
Data815 = pd.read_csv("merged_800m_1500m_df.csv")
Data816 = pd.read_csv("merged_800m_1600m_df.csv")
                      
#Add sidebar to the app
st.sidebar.markdown("### My first Awesome App")
st.sidebar.markdown("Welcome to my first awesome app. This app is built using Streamlit and uses data source from redfin housing market data. I hope you enjoy!")

#Add title and subtitle to the main interface of the app
st.title("U.S. Real Estate Insights")
st.markdown("Where are the hottest housing markets in the U.S.? Select the housing market metrics you are interested in and your insights are just a couple clicks away. Hover over the map to view more details.")

tab1, tab2 = st.tabs(["Data Visualization","Something else you might think of"])

with tab1:
    #Create three columns/filters
    col1 = st.columns(1)

    racetype = st.selectbox("View by race type", ['400m to 800m', '400m to 1500m', '400m to 1600m','800m to 1500m','800m to 1600m'] , index=0)
    st.write ('The race type is' , racetype) 


    if (racetype == '400m to 800m'): 
        df = Data48
        #st.dataframe(df)

    elif (racetype == '400m to 1500m'): 
        df = Data415
        #st.dataframe(df)

    elif (racetype == '400m to 1600m'): 
        df = Data416
        #st.dataframe(df)

    elif (racetype == '800m to 1500m'): 
        df = Data815
        #st.dataframe(df)

    elif (racetype == '800m to 1600m'): 
        df = Data816
        #st.dataframe(df)
                      


    grade = st.selectbox("Select a grade level", ['9th Grade', '10th Grade', '11th Grade', '12th Grade'], index=0)
    racdf = df.loc[df['Grade Level']== grade]
    #gradedf = racdf['Grade Level']]

    #gradedf = racdf.loc[racdf['Grade Level']== grade]
    #racdf[Grade Level)

    st.dataframe(racdf)

with tab2: 
    
    #grade2 = st.selectbox("Select a grade level",['9th Grade Level', '10th Grade Level', '11th Grade Level', '12th Grade Level'], index=1)
    #grade2
    #p1 = sns.relplot(data=Data48, x='400 Meters', y='800 Meters', kind='scatter', hue='Season', palette ='deep', col="Grade Level")
    #plt.subplots_adjust(wspace=0.2)
    #p1.set_axis_labels("400 Meter Time(s)", "800 Meter Time(s)")
    #p1.set(ylim=(100, None))
    #p1.set(xlim=(45, None))
    #st.pyplot(p1)