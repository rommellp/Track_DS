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
import datetime
import base64
from PIL import Image

os.chdir(r"C:\Users\5luca\Documents\Python\Projects\Track_DS\1merged_df")
#os.chdir(r"C:\Users\5luca\Documents\Python\Projects\Track_DS\models")
#os.chdir("/Users/rommellp/Desktop/Track_DS_Project/Clean_visual_code/1merged_df/")
#os.chdir("/Users/rommellp/Desktop/Track_DS_Project/Clean_visual_code/models/Modeling_400_800_final.ipynb")

# Loading Image using PIL
#im = Image.open('TrackDS_icon.jpg')
# Adding Image to web app
st.set_page_config(page_title="Track DS")
#st.set_page_config(layout="wide")




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
st.sidebar.markdown("Welcome to my first app. This app is built using Streamlit and uses data source from Athletic.net. I hope you enjoy!")

#Add title and subtitle to the main interface of the app
st.title("Analyszing the Correlation Between 400m and 800m Runners")
st.markdown("On the left tab we have the data in a chart where you can filter the event pairs and grade level. Below the chart is a scatter plot that uses the same filer. This plot also colors each \
            point by season to further visualize the trend over time. On the right tab we have the machine learning model that predicts your 800m time based on the input of your 400m time and \
            grade level.")

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
    #os.chdir("/Users/rommellp/Desktop/Track_DS_Project/Clean_visual_code/models/")
    
    
    
    st.markdown("The prediction below is for predicting an 800m time based on their 400m time and grade level. This example is one of the many pairs of models. There is a model for every \
            event pair seen on the charts on the data visualization tab.")
    
    st.markdown("The model used to predict is a linear regression model. As seen on the plot on the visualization tab, each combination of events and grade level shows a clear linear \
            correlation. Although many different regression models were tried, the simply linear regression model produced the best results. The results of this model were a RMSE of 8.7, and \
            an accuracy score of 59%. ")
    col3, col4 = st.columns(2)
    with col3:
            
            with st.form("my_form"): #creating a form for the user
                st.write("ML model for the 400m and 800m") #WRITE HERE
                pastgrade=st.selectbox("Select a grade level:",['9th Grade', '10th Grade', '11th Grade', '12th Grade'] ,index=0)
                
                final_model_reloaded = joblib.load("final_model_linreg.pkl") #calling the ML model
                
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
                number = st.number_input('Enter your time in seconds:', format = '%f', help=None) 
                array0 = np.array([number]) #putting float into an array 
                array3 = np.concatenate((array0,array1), axis=0) #combining array 0 and array 1 to format data input for ML model
                new_data = array3.reshape(1,-1) #correct array shape to horizantal            
                predictions = final_model_reloaded.predict(new_data)#pushing data from the user into the ML model
                predictions1 = predictions.astype(int)# i dont think this is needed anymore check on this again
                
                submitted = st.form_submit_button("Submit") #submit button 
                
                if submitted:
                    progress = st.progress(0) #the start of progress bar = 0
                    for i in range (100):
                        time.sleep(0.005)# modify number if you want to change how long the progress takes, lower the number the faster 
                        progress.progress(i+1)
                        
                    seconds = predictions1[0]

                    minutes, seconds = divmod(seconds, 60)
                    #hours, minutes = divmod(minutes, 60)
                    st.write("Estimated time for 800m is:")
                    st.write("%02d:%02d" % (minutes, seconds))
                    
                    #st.write("Estimated time for 800m:",minutes, "seconds") #prints out results

    with col4: 
        
            with st.form ("Second Model"):
                st.write("Add title")
                mse_rft = joblib.load("mse_rft.pkl") #calling the ML model
                
                gradeslc = st.selectbox("Select your grade level",['9th Grade', '10th Grade', '11th Grade', '12th Grade'] ,index=0)
                
                if (gradeslc == '9th Grade'):
                    arrayin = [1,0,0,0]
                elif (gradeslc == '10th Grade'):
                    arrayin = [0,1,0,0]
                elif (gradeslc == '11th Grade'):
                    arrayin = [0,0,1,0]
                elif (gradeslc == '12th Grade'):
                    arrayin = [0,0,0,1]
                    
                timein = st.number_input('Enter your time:', format = '%f', help=None)
                 
                array0 = np.array([timein]) #putting float into an array 
                array3 = np.concatenate((array0,array1), axis=0) #combining array 0 and array 1 to format data input for ML model
                new_data = array3.reshape(1,-1) #correct array shape to horizantal            
                predictions = final_model_reloaded.predict(new_data)#pushing data from the user into the ML model
                predictions1 = predictions.astype(int)# i dont think this is needed anymore check on this again
                
                submitted1 = st.form_submit_button("Submit") #submit button 
                
                if submitted1:
                    progress = st.progress(0) #the start of progress bar = 0
                    for i in range (100):
                        time.sleep(0.05)# modify number if you want to change how long the progress takes, lower the number the faster 
                        progress.progress(i+1)
                        
                        seconds = predictions1[0]

                    minutes, seconds = divmod(seconds, 60)
                    #hours, minutes = divmod(minutes, 60)
                    st.write("Estimated time for 800m in the next grade is:")
                    st.write("%02d:%02d" % (minutes, seconds))
                    #st.write("Estimated time for 800m:", predictions1[0], "seconds") #prints out results