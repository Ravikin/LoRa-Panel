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


# link = "https://eu1.cloud.thethings.network/api/v3/as/applications/ravikin-test-app/packages/storage/uplink_normalized?limit="+limit+"
link = baseUrlDev+devices[1]+"/packages/storage/"+types[1]+""
r = requests.get(link,headers=headers)

jsonObj = json.loads(r.text)

temp1 = jsonObj["result"]["uplink_message"]["decoded_payload"]["temp"]
humi1 = jsonObj["result"]["uplink_message"]["decoded_payload"]["humi"]
volt1 = jsonObj["result"]["uplink_message"]["decoded_payload"]["volt"]
rec1 =  jsonObj["result"]["received_at"]

st.header("LoRa Sensor Data")
st.subheader(str(devices[1]+" "+rec1))
col1, col2, col3 = st.columns(3)
col1.metric(label="Temperature", value=temp1)
col2.metric(label="Humidity", value=humi1)
col3.metric(label="Battery Voltage", value=volt1)


link = baseUrlDev+devices[2]+"/packages/storage/"+types[1]+""
r2 = requests.get(link,headers=headers)

jsonObj2 = json.loads(r2.text)

temp2 = jsonObj2["result"]["uplink_message"]["decoded_payload"]["temp"]
humi2 = jsonObj2["result"]["uplink_message"]["decoded_payload"]["humi"]
volt2 = jsonObj2["result"]["uplink_message"]["decoded_payload"]["volt"]
rec2 =  jsonObj2["result"]["received_at"]

st.subheader(str(devices[2]+" "+rec2))
col1, col2, col3 = st.columns(3)
col1.metric(label="Temperature", value=temp2)
col2.metric(label="Humidity", value=humi2)
col3.metric(label="Battery Voltage", value=volt2)

link = baseUrlDev+devices[0]+"/packages/storage/"+types[1]+""
r0 = requests.get(link,headers=headers)

jsonObj0 = json.loads(r0.text)

temp0 = jsonObj0["result"]["uplink_message"]["decoded_payload"]["temp"]
humi0 = jsonObj0["result"]["uplink_message"]["decoded_payload"]["humi"]
volt0 = "∞"
rec0 =  jsonObj0["result"]["received_at"]


st.subheader(str(devices[0]+" "+rec0))
col1, col2, col3 = st.columns(3)
col1.metric(label="Temperature", value=temp0)
col2.metric(label="Humidity", value=humi0)
col3.metric(label="Battery Voltage", value=volt0)


data = {
    'Location': ["eui-2cf7f1205100a1e0", "eui-mkrwan1310-1-a861", "eui-a8610a3438306602"],
    'latitude': [52.3639741, 52.3634742, 52.3622212],
    'longitude': [21.0535907, 21.0505278, 21.0497551],
    'Humidity': [humi0, humi1, humi2],
    'Temperature': [temp0, temp1, temp2],
    'Size':  [temp0, temp1, temp2]
}

df = pd.DataFrame(data)

# Sidebar inputs
st.sidebar.header('Input Parameters')
selected_point = st.sidebar.selectbox('Select a point:', df['Location'])
selected_data = df[df['Location'] == selected_point].iloc[0]
st.sidebar.write(f"latitude: {selected_data['latitude']}")
st.sidebar.write(f"longitude: {selected_data['longitude']}")
st.sidebar.write(f"Humidity: {selected_data['Humidity']}%")
st.sidebar.write(f"Temperature: {selected_data['Temperature']}°C")


def get_color(temperature):
    # Normalize temperature between 0 and 1
    normalized_temperature = (temperature - df['Temperature'].min()) / (df['Temperature'].max() - df['Temperature'].min())
    # Interpolate between green and red
    r = int(np.interp(normalized_temperature, [0, 100], [0, 255]))
    g = int(np.interp(normalized_temperature, [0, 100], [255, 0]))
    b = 0
    return f'#{r:02x}{g:02x}{b:02x}'

df['Color'] = df['Temperature'].apply(get_color)

st.header('Map with Points')
st.map(df,
    latitude='latitude',
    longitude='longitude',
    size='Size',
    color='Color')

