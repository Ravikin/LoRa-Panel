import streamlit as st
import requests
import json

import pandas as pd
import numpy as np

token = st.text_input("Bearer Token")
bearer = "Bearer "+str(token)
headers = {'Accept': 'application/json', 'Authorization':bearer}
devices = ["eui-2cf7f1205100a1e0","eui-mkrwan1310-1-a861","eui-a8610a3438306602","eui-2cf7f1205100b6a2-uno-main"]
types =  [ "uplink_message", "uplink_normalized", "join_accept", "downlink_ack", "downlink_nack", "downlink_sent", "downlink_failed", "downlink_queued", "downlink_queue_invalidated", "location_solved", "service_data"]
baseUrlAll="https://eu1.cloud.thethings.network/api/v3/as/applications/ravikin-test-app/packages/storage/{type}"
baseUrlDev="https://eu1.cloud.thethings.network/api/v3/as/applications/ravikin-test-app/devices/"#{device_id}/packages/storage/{type}"
limit = str(1)


# link = "https://eu1.cloud.thethings.network/api/v3/as/applications/ravikin-test-app/packages/storage/uplink_normalized?limit="+limit
link = baseUrlDev+devices[1]+"/packages/storage/"+types[1]+"?limit=1"
r = requests.get(link,headers=headers)

jsonObj = json.loads(r.text)

temp1 = jsonObj["result"]["uplink_message"]["decoded_payload"]["temp"]
humi1 = jsonObj["result"]["uplink_message"]["decoded_payload"]["humi"]
volt1 = jsonObj["result"]["uplink_message"]["decoded_payload"]["volt"]

st.header("LoRa Sensor Data")
st.subheader(str(devices[1]))
col1, col2, col3 = st.columns(3)
col1.metric(label="Temperature", value=temp1)
col2.metric(label="Humidity", value=humi1)
col3.metric(label="Battery Voltage", value=volt1)



link = baseUrlDev+devices[2]+"/packages/storage/"+types[1]+"?limit=1"
r = requests.get(link,headers=headers)

jsonObj = json.loads(r.text)

temp2 = jsonObj["result"]["uplink_message"]["decoded_payload"]["temp"]
humi2 = jsonObj["result"]["uplink_message"]["decoded_payload"]["humi"]
volt2 = jsonObj["result"]["uplink_message"]["decoded_payload"]["volt"]

st.subheader(str(devices[2]))
col1, col2, col3 = st.columns(3)
col1.metric(label="Temperature", value=temp2)
col2.metric(label="Humidity", value=humi2)
col3.metric(label="Battery Voltage", value=volt2)

link = baseUrlDev+devices[0]+"/packages/storage/"+types[1]+"?limit=1"
r = requests.get(link,headers=headers)

jsonObj = json.loads(r.text)

temp0 = jsonObj["result"]["uplink_message"]["decoded_payload"]["temp"]
humi0 = jsonObj["result"]["uplink_message"]["decoded_payload"]["humi"]
volt0 = "∞"

st.subheader(str(devices[0]))
col1, col2, col3 = st.columns(3)
col1.metric(label="Temperature", value=temp0)
col2.metric(label="Humidity", value=humi0)
col3.metric(label="Battery Voltage", value=volt0)


data = {
    'Location': [str(devices[0]), str(devices[1]), str(devices[2])],
    'Latitude': [52.3634621, 52.3634621, 52.3634621],
    'Longitude': [52.3634621, 52.3634621, 52.3634621],
    'Humidity (%)': [humi0, humi1, humi2],
    'Temperature (°C)': [temp0, temp1, temp2]
}

df = pd.DataFrame(data)

# Sidebar inputs
st.sidebar.header('Input Parameters')
selected_point = st.sidebar.selectbox('Select a point:', df['Location'])
selected_data = df[df['Location'] == selected_point].iloc[0]
st.sidebar.write(f"Latitude: {selected_data['Latitude']}")
st.sidebar.write(f"Longitude: {selected_data['Longitude']}")
st.sidebar.write(f"Humidity: {selected_data['Humidity (%)']}%")
st.sidebar.write(f"Temperature: {selected_data['Temperature (°C)']}°C")

# Display the map
st.header('Map with Points')
st.map(df[['Latitude', 'Longitude']].values)