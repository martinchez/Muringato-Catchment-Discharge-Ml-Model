# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 10:56:22 2024

@author: HP
"""

import pandas as pd
import pickle
import streamlit as st
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestRegressor

data = pd.read_csv('discharge.csv')
# Drop rows with missing 'level' values
df = data.dropna(subset=['level'])
df['received_at'] = pd.to_datetime(df['received_at'])
df['created_at'] = pd.to_datetime(df['created_at'])


df['received_hour'] = df['received_at'].dt.hour
df['received_minute'] = df['received_at'].dt.minute


df = df.drop(columns=['id', 'received_at', 'created_at'])

#df['level'] = df['level'].fillna(df['level'].mean())
df['temp'] = df['temp'].fillna(df['temp'].mean())
df['voltage_temp'] = df['voltage_temp'].fillna(df['voltage_temp'].mean())
X = df.drop(columns=['level'])
y = df['level']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
# Building preprocessing pipeline for categorical and numerical features
categorical_features = ['device_id', 'application_id']
numerical_features = [col for col in X.columns if col not in categorical_features]

categorical_transformer = OneHotEncoder(handle_unknown='ignore')
numerical_transformer = SimpleImputer(strategy='mean')

preprocessor = ColumnTransformer(
    transformers=[
        ('cat', categorical_transformer, categorical_features),
        ('num', numerical_transformer, numerical_features)
    ])


model = Pipeline(steps=[('preprocessor', preprocessor),
                        ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))])

model.fit(X_train, y_train)





#preprocessor = pickle.load(open('path/to/your/preprocessor.sav', 'rb'))

# Sidebar for navigation
with st.sidebar:
    selected = st.selectbox('Choose Prediction', 
                            ['Discharge Level'])

# Discharge Level Prediction Page
if selected == 'Discharge Level':
    st.title('Discharge Level Prediction using ML')

    # Getting the input data from the user
    col1, col2, col3 = st.columns(3)

    with col1:
        device_id = st.selectbox('Device ID', ('rdms1', 'flow1', 'rdms2'))
       
    with col2:
        application_id = st.selectbox('Application ID',('muringato-discharge', 'discharge'))
    with col3:
        distance = st.number_input('Distance')
    
    with col1:
        pulse = st.number_input('Pulse')
    with col2:
        flow_rate = st.number_input('Flow Rate')
    with col3:
        voltage_battery = st.number_input('Voltage Battery')
    
    with col1:
        voltage_solar = st.number_input('Voltage Solar')
    with col2:
        temp = st.number_input('Temperature')
    with col3:
        voltage_temp = st.number_input('Voltage Temp')
    
   
    
    # Code for Prediction
    discharge_prediction = ''
    from datetime import datetime

# Get the current date and time
   # now = datetime.now()
    
    # Creating a button for Prediction
    if st.button('Predict Discharge Level'):
        # Creating a DataFrame with the user inputs
        input_data = pd.DataFrame([{
            'device_id': device_id,
            'application_id': application_id,
            'distance': distance,
            'pulse': pulse,
            'flow_rate': flow_rate,
            'voltage_battery': voltage_battery,
            'voltage_solar': voltage_solar,
            'temp': temp,
            'voltage_temp': voltage_temp,
          # 'received_at': received_at,
            'received_at': pd.Timestamp.now()  # Add this to align with the model's training
        }])

        # Predict the level for the new data
        # Preprocess the input data
        input_data['received_at'] = pd.to_datetime(input_data['received_at'])
        input_data['received_hour'] = input_data['received_at'].dt.hour
        input_data['received_minute'] = input_data['received_at'].dt.minute
        #input_data = input_data.drop(columns=['created_at'])

        # Handle missing values
        input_data['temp'] = input_data['temp'].fillna(input_data['temp'].mean())
        input_data['voltage_temp'] = input_data['voltage_temp'].fillna(input_data['voltage_temp'].mean())

        
       
        
        # Apply preprocessing
        #X_new_transformed = preprocessor.transform(input_data)
        prediction = model.predict(input_data)
        discharge_prediction = f'Predicted Discharge Level: {prediction[0]}'

    st.success(discharge_prediction)
