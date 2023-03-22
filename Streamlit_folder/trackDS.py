import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import plotly.express as px
import os
import joblib
import time


#st.set_page_config(layout="wide")

os.chdir(r"C:\Users\5luca\Documents\Python\Projects\Track_DS\1merged_df")
#os.chdir(r"C:\Users\5luca\Documents\Python\Projects\Track_DS\models")
#os.chdir("/Users/rommellp/Desktop/Track_DS_Project/Clean_visual_code/1merged_df/")

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
    final_model_reloaded = joblib.load("final_model_linreg.pkl") #calling the ML model
    col3, col4 = st.columns(2)
    with col3:
            with st.form("my_form"): #creating a for for the user
                st.write("Inside the form") #WRITE HERE
                pastgrade=st.selectbox("Select your grade level",['9th Grade', '10th Grade', '11th Grade', '12th Grade'] ,index=0)
                
                #conditions for how each individual grade uses a unique array in the ML model
                if(pastgrade == '9th Grade'):
                        array1 = [1,0,0,0]
                elif (pastgrade == '10th Grade'):
                          array1 = [0,1,0,0]
                elif (pastgrade == '11th Grade'):
                          array1 = [0,0,1,0]
                elif (pastgrade == '12th Grade'):
                        array1 = [0,0,0,1]
                        
                #user will input thier time in seconds        
                number = st.number_input('Enter your time:', format = '%f', help=None) 
                array0 = np.array([number]) #putting float into an array 
                array3 = np.concatenate((array0,array1), axis=0) #combining array 0 and array 1 to format data input for ML model
                new_data = array3.reshape(1,-1) #correct array shape to horizantal            
                predictions = final_model_reloaded.predict(new_data)#pushing data from the user into the ML model
                predictions1 = predictions.astype(int)# i dont think this is needed anymore check on this again
                
                submitted = st.form_submit_button("Submit") #submit button 
                
                if submitted:
                    progress = st.progress(0) #the start of progress bar = 0
                    for i in range (100):
                        time.sleep(0.05)# modify number if you want to change how long the progress takes, lower the number the faster 
                        progress.progress(i+1)
                        
                    st.write("Estimated time for 800m:", predictions1[0], "seconds") #prints out results
                    
                  
                
                
                
                
                