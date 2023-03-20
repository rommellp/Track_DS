import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import plotly.express as px
import os


#st.set_page_config(layout="wide")

#os.chdir(r"C:\Users\5luca\Documents\Python\Projects\Track_DS\1merged_df")


#calling in data and remocing unnecessary column
Data48  = pd.read_csv("merged_400m_800m_df.csv", index_col = "ID Number")
Data48  = Data48.drop(columns=['Unnamed: 0'])

Data415 = pd.read_csv("merged_400m_1500m_df.csv", index_col = "ID Number")
Data415  = Data415.drop(columns=['Unnamed: 0'])

Data416 = pd.read_csv("merged_400m_1600m_df.csv", index_col = "ID Number")
Data416  = Data416.drop(columns=['Unnamed: 0'])

Data815 = pd.read_csv("merged_800m_1500m_df.csv", index_col = "ID Number")
Data815  = Data815.drop(columns=['Unnamed: 0'])

Data816 = pd.read_csv("merged_800m_1600m_df.csv", index_col = "ID Number")
Data816  = Data816.drop(columns=['Unnamed: 0'])
                      
#Add sidebar to the app
st.sidebar.markdown("### My first Awesome App")
st.sidebar.markdown("Welcome to my first awesome app. This app is built using Streamlit and uses data source from redfin housing market data. I hope you enjoy!")

#Add title and subtitle to the main interface of the app
st.title("U.S. Real Estate Insights")
st.markdown("Where are the hottest housing markets in the U.S.? Select the housing market metrics you are interested in and your insights are just a couple clicks away. Hover over the map to view more details.")

# add two tabs for different purposes
tab1, tab2 = st.tabs(["Data Visualization","Something else you might think of"])

#start of tab 1
with tab1:
    
    #Create two columns/filters
    col1, col2 = st.columns(2)
    with col1:
    
        racetype=st.selectbox("View by race type",['400m to 800m', '400m to 1500m','400m to 1600m','800m to 1500m','800m to 1600m'],index=0)
         
        if (racetype == '400m to 800m'): 
            df = Data48
        elif (racetype == '400m to 1500m'): 
            df = Data415
        elif (racetype == '400m to 1600m'): 
            df = Data416
        elif (racetype == '800m to 1500m'): 
            df = Data815
        elif (racetype == '800m to 1600m'): 
            df = Data816

    with col2:
        
        grade = st.selectbox("Select a grade level", ['9th Grade', '10th Grade', '11th Grade', '12th Grade'], index=0)
        racdf = df.loc[df['Grade Level']== grade]
        
    with st.expander("Click to view.....", expanded=True):
        st.write("Here are more details demonstrating.....")          
        st.write(racdf)
    with st.expander("Click to view....."):
        st.write("Here are more details demonstrating.....")
        #col1, col2 = st.columns(2)
        #with col1:
        
        
 
        if (racetype == '400m to 800m'): 
            df = Data48
            grade_type = df.loc[df['Grade Level']== grade]
            fig = px.scatter( grade_type, 
                             x = "400 Meters", 
                             y = "800 Meters", 
                             color = "Season", 
                             hover_name="Season",
                             #color_continuous_scale="")
                             size_max=150,)
            st.plotly_chart(fig, theme="streamlit", use_container_width=True)
            
        elif (racetype == '400m to 1500m'): 
            df = Data415
            grade_type = df.loc[df['Grade Level']== grade]
            fig = px.scatter( grade_type, 
                             x = "400 Meters", 
                             y = "1500 Meters", 
                             color = "Season", 
                             hover_name="Season",
                             #color_continuous_scale="")
                             size_max=150,)
            st.plotly_chart(fig, theme="streamlit", use_container_width=True)
          
            
        elif (racetype == '400m to 1600m'): 
            df = Data416
            grade_type = df.loc[df['Grade Level']== grade]
            fig = px.scatter( grade_type, 
                             x = "400 Meters", 
                             y = "1600 Meters", 
                             color = "Season", 
                             hover_name="Season",
                             #color_continuous_scale="")
                             size_max=150,)
            st.plotly_chart(fig, theme="streamlit", use_container_width=True)
            
        elif (racetype == '800m to 1500m'): 
            df = Data815
            grade_type = df.loc[df['Grade Level']== grade]
            fig = px.scatter( grade_type, 
                             x = "800 Meters", 
                             y = "1500 Meters", 
                             color = "Season", 
                             hover_name="Season",
                             #color_continuous_scale="")
                             size_max=150,)
            st.plotly_chart(fig, theme="streamlit", use_container_width=True)
            
        elif (racetype == '800m to 1600m'): 
            df = Data816
            grade_type = df.loc[df['Grade Level']== grade]
            fig = px.scatter( grade_type, 
                             x = "800 Meters", 
                             y = "1600 Meters", 
                             color = "Season", 
                             hover_name="Season",
                             #color_continuous_scale="")
                             size_max=150,)
            st.plotly_chart(fig, theme="streamlit", use_container_width=True)
            
with tab2: 
    
    grade2 = st.selectbox("Select a grade level",['9th Grade Level', '10th Grade Level', '11th Grade Level', '12th Grade Level'], index=1)
    #grade2
    #p1 = sns.relplot(data=Data48, x='400 Meters', y='800 Meters', kind='scatter', hue='Season', palette ='deep', col="Grade Level")
    #plt.subplots_adjust(wspace=0.2)
    #p1.set_axis_labels("400 Meter Time(s)", "800 Meter Time(s)")
    #p1.set(ylim=(100, None))
    #p1.set(xlim=(45, None))

    
    
    
    
    
    
    
    