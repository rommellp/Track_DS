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
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,)

st.set_page_config(layout="wide", page_title="Track DS")

os.chdir(r"C:\Users\5luca\Documents\Python\Projects\Track_DS\1merged_df")
#os.chdir(r"C:\Users\5luca\Documents\Python\Projects\Track_DS\models")
#os.chdir("/Users/rommellp/Desktop/Track_DS_Project/Clean_visual_code/1merged_df/")
#os.chdir("/Users/rommellp/Desktop/Track_DS_Project/Clean_visual_code/models/Modeling_400_800_final.ipynb")

#This is what gets an image for the background

def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    
    st.markdown(page_bg_img, unsafe_allow_html=True)
    return

#set_background('track.png') #here goes the image name, since we are going to 1merged_df, the image must be in that folder


#calling in data and removing unnecessary column
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
    col1, col2= st.columns(2)
    with col1:
    
        racetype=st.selectbox("View by race type",['400m to 800m', '400m to 1500m','400m to 1600m','800m to 1500m','800m to 1600m'],index=0)
         
        if (racetype == '400m to 800m'): 
            df1 = Data48
        elif (racetype == '400m to 1500m'): 
            df1 = Data415
        elif (racetype == '400m to 1600m'): 
            df1 = Data416
        elif (racetype == '800m to 1500m'): 
            df1 = Data815
        elif (racetype == '800m to 1600m'): 
            df1 = Data816

    with col2:
        
        grade = st.selectbox("Select a grade level", ['9th Grade', '10th Grade', '11th Grade', '12th Grade'], index=0)
        df = df1.loc[df1['Grade Level']== grade]
        
    col3, col4 = st.columns(2)
            
    with col3: #Filter code
        def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
                    modify = st.checkbox("Add filters")

                    if not modify:
                        return df

                    df = df.copy()

                    for col in df.columns:
                        if is_object_dtype(df[col]):
                            try:
                                df[col] = pd.to_datetime(df[col])
                            except Exception:
                                pass

                        if is_datetime64_any_dtype(df[col]):
                            df[col] = df[col].dt.tz_localize(None)

                    modification_container = st.container() 

                    with modification_container:
                        to_filter_columns = st.multiselect("Filter dataframe on", df.columns)
                        for column in to_filter_columns:
                            left, right = st.columns((1, 20))
                            # Treat columns with < 10 unique values as categorical
                            if is_categorical_dtype(df[column]) or df[column].nunique() < 10:
                                user_cat_input = right.multiselect(
                                    f"Values for {column}",
                                    df[column].unique(),
                                    default=list(df[column].unique()),
                                )
                                df = df[df[column].isin(user_cat_input)]
                            elif is_numeric_dtype(df[column]):
                                _min = float(df[column].min())
                                _max = float(df[column].max())
                                step = (_max - _min) / 100
                                user_num_input = right.slider(
                                    f"Values for {column}",
                                    min_value=_min,
                                    max_value=_max,
                                    value=(_min, _max),
                                    step=step,
                                )
                                df = df[df[column].between(*user_num_input)]
                            elif is_datetime64_any_dtype(df[column]):
                                user_date_input = right.date_input(
                                    f"Values for {column}",
                                    value=(
                                        df[column].min(),
                                        df[column].max(),
                                    ),
                                )
                                if len(user_date_input) == 2:
                                    user_date_input = tuple(map(pd.to_datetime, user_date_input))
                                    start_date, end_date = user_date_input
                                    df = df.loc[df[column].between(start_date, end_date)]
                            else:
                                user_text_input = right.text_input(
                                    f"Substring or regex in {column}",
                                )
                                if user_text_input:
                                    df = df[df[column].astype(str).str.contains(user_text_input)]

                    return df       
        st.dataframe(filter_dataframe(df)) #print data with filter

    with col4:   
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