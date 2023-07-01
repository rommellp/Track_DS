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

st.set_page_config(layout="wide", page_title="Track DS") #sets the page to a wide layout and adds title to the app 

#os.chdir(r"C:\Users\5luca\Documents\Python\Projects\Track_DS\Streamlit_folder\merged_df")
#os.chdir(r"C:\Users\5luca\Documents\Python\Projects\Track_DS\models")
#os.chdir("/Users/rommellp/Desktop/Track_DS_Project/Clean_visual_code/1merged_df/")
#os.chdir("/Users/rommellp/Desktop/Track_DS_Project/Clean_visual_code/models/Modeling_400_800_final.ipynb")
    
@st.cache_resource
def read_csv(path):
    return pd.read_csv(path, index_col = "ID Number")

filename1 = 'merged_df/merged_400m_800m_df.csv'
filename2 = 'merged_df/merged_400m_1500m_df.csv'
filename3 = 'merged_df/merged_400m_1600m_df.csv'
filename4 = 'merged_df/merged_800m_1500m_df.csv'
filename5 = 'merged_df/merged_800m_1600m_df.csv'

Data48 = read_csv(filename1)
Data415 = read_csv(filename2)
Data416 = read_csv(filename3)
Data815 = read_csv(filename4)
Data816 = read_csv(filename5)

#calling in data and removing unnecessary column
Data48  = Data48.drop(columns=['Unnamed: 0', 'Gender_y'])
Data48  = Data48.rename(columns={"Gender_x": "Gender"})

Data415  = Data415.drop(columns=['Unnamed: 0', 'Gender_y'])
Data415  = Data415.rename(columns={"Gender_x": "Gender"})

Data416  = Data416.drop(columns=['Unnamed: 0', 'Gender_y'])
Data416  = Data416.rename(columns={"Gender_x": "Gender"})

Data815  = Data815.drop(columns=['Unnamed: 0', 'Gender_y'])
Data815  = Data815.rename(columns={"Gender_x": "Gender"})

Data816  = Data816.drop(columns=['Unnamed: 0', 'Gender_y'])
Data816  = Data816.rename(columns={"Gender_x": "Gender"})
                      
#Add sidebar to the app
st.sidebar.markdown("### My first Awesome App")
st.sidebar.markdown("Welcome to my first app. This app is built using Streamlit and uses data source from Athletic.net. I hope you enjoy!")

#Add title and subtitle to the main interface of the app
st.title("Analyzing the Linear Correlation Between Runners That Compete in Track Event Pairs")
st.markdown("On the Data Visualization tab we have datafames where you can filter the event pairs and grade level. Below the chart is a scatter plot that uses the same filer. This plot also colors each point by season to further visualize the trend over time. On the right tab we have the machine learning model that predicts your 800m and 1500m time based on the input of your 400m and 800m time respectively, with grade level.")

# add two tabs for different purposes
tab1, tab2 = st.tabs(["Data Visualization","Prediction Modeling"])

#start of tab 1
with tab1:
    
    #Create two columns/filters
    col1, col2= st.columns(2)
    with col1:
        #select box for the user
        racetype=st.selectbox("View by race type",['400m to 800m', '400m to 1500m','400m to 1600m','800m to 1500m','800m to 1600m'],index=0)
        # if statements that chooses between the 5 different data sets
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
        grade = st.selectbox("Select a grade level", ['9th Grade', '10th Grade', '11th Grade', '12th Grade'], index=0) #grade selection
        df = df1.loc[df1['Grade Level']== grade] #filters grade types based on users selection
        
    #creating two more columns underneath col1 and col2    
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
        cleandata = filter_dataframe(df) #naming the filtered data to use for dataframe and scatter plots      
        st.dataframe(cleandata) #print data with filter

    with col4: #these if statemts determine the label axis of the graph, still using "cleandata"   
        if (racetype == '400m to 800m'):
            fig = px.scatter( cleandata, 
                             x = "400 Meters", 
                             y = "800 Meters", 
                             color = "Season", 
                             hover_name="Season",
                             #color_continuous_scale="")
                             size_max=150,)
            st.plotly_chart(fig, theme="streamlit", use_container_width=True)
            
        elif (racetype == '400m to 1500m'):
            fig = px.scatter( cleandata, 
                             x = "400 Meters", 
                             y = "1500 Meters", 
                             color = "Season", 
                             hover_name="Season",
                             #color_continuous_scale="")
                             size_max=150,)
            st.plotly_chart(fig, theme="streamlit", use_container_width=True)
               
        elif (racetype == '400m to 1600m'):
            fig = px.scatter( cleandata, 
                             x = "400 Meters", 
                             y = "1600 Meters", 
                             color = "Season", 
                             hover_name="Season",
                             #color_continuous_scale="")
                             size_max=150,)
            st.plotly_chart(fig, theme="streamlit", use_container_width=True)
            
        elif (racetype == '800m to 1500m'):
            fig = px.scatter( cleandata, 
                             x = "800 Meters", 
                             y = "1500 Meters", 
                             color = "Season", 
                             hover_name="Season",
                             #color_continuous_scale="")
                             size_max=150,)
            st.plotly_chart(fig, theme="streamlit", use_container_width=True)
            
        elif (racetype == '800m to 1600m'):
            fig = px.scatter( cleandata, 
                             x = "800 Meters", 
                             y = "1600 Meters", 
                             color = "Season", 
                             hover_name="Season",
                             #color_continuous_scale="")
                             size_max=150,)
            st.plotly_chart(fig, theme="streamlit", use_container_width=True)

with tab2:

    
    
    st.markdown("The prediction below is for predicting an 800m time based on their 400m time and grade level. This example is one of the many pairs of models. \
                There is a model for every event pair seen on the charts on the data visualization tab.")
        
    st.markdown(":red[Try out the two models above and let us know how accurate the predictions are for you!]")
    
    col5, col6 = st.columns(2)
    with col5:
            
            with st.form("my_form"): #creating a form for the user
                st.write("ML prediction model for 400m and 800m") #Title for the form
                pastgrade=st.selectbox("Select a grade level:",['9th Grade', '10th Grade', '11th Grade', '12th Grade'] ,index=0)
                
                final_model_reloaded = joblib.load("merged_df/final_model_linreg.pkl") #calling the ML model
                
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
                    st.write("Estimated time for 800m is:")
                    st.write("%02d:%02d" % (minutes, seconds))
    with col6:
        
        with st.form ("Second Model"):
                st.write("ML Prediction Model for 800m and 1500m") #Title for the form
                mse_rft = joblib.load("merged_df/mse_rft.pkl") #calling the ML model
                
                gradeslc = st.selectbox("Select your grade level",['9th Grade', '10th Grade', '11th Grade', '12th Grade'] ,index=0)
                #conditions for how each individual grade uses a unique array in the ML model
                if (gradeslc == '9th Grade'):
                    arrayin = [1,0,0,0]
                elif (gradeslc == '10th Grade'):
                    arrayin = [0,1,0,0]
                elif (gradeslc == '11th Grade'):
                    arrayin = [0,0,1,0]
                elif (gradeslc == '12th Grade'):
                    arrayin = [0,0,0,1]
                    
                timein = st.number_input('Enter your time in seconds:', format = '%f', help=None)
                 
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
                    st.write("Estimated time for 800m in the next grade is:")
                    st.write("%02d:%02d" % (minutes, seconds))
                    
    st.markdown("The model used for 400/800m is the linear regression model. As seen on the plot on the visualization tab, each combination of events and grade \
                level shows a clear linear correlation. Although many different regression models were tried, the simply linear regression model produced the \
                best results. The results of this model were a RMSE of 8.7, and an accuracy score of 59%. ")

    st.markdown("The model used for 800/1500m is the RandomForestRegressor with optimized parameters. The data used for this model can be viewed in the \
                visualization tab, just as with the previous model. The results for this model were an RMSE of 14.8 and an accuracy score of 75%. I \
                consider this a good result for this model in the context of the limitations mentioned with the first model. ")

    st.markdown("Now that you've had a chance to use the models above, give a thought about how accurate it is for you. \
                If you noticed that the 800/1500 model was more accurate, that could be because the dataset used for that \
                model is almost twice as big! That size different likely had a huge part to play with the substantial \
                difference in accuracy scores of both models. Thank you to Athletic.net for collecting this data. It \
                was a dream to be able to work on this project and visualize trends I've heard for ages in Track and field, but never tested.")
        
            
        
            
