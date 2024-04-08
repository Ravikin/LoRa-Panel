import folium
import streamlit as st

from streamlit_folium import st_folium
import requests
import json

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

temp = jsonObj["result"]["uplink_message"]["decoded_payload"]["temp"]
humi = jsonObj["result"]["uplink_message"]["decoded_payload"]["humi"]
volt = jsonObj["result"]["uplink_message"]["decoded_payload"]["volt"]

st.header("LoRa Sensor Data")
st.subheader(str(devices[1]))
col1, col2, col3 = st.columns(3)
col1.metric(label="Temperature", value=temp)
col2.metric(label="Humidity", value=humi)
col3.metric(label="Battery Voltage", value=volt)



link = baseUrlDev+devices[2]+"/packages/storage/"+types[1]+"?limit=1"
r = requests.get(link,headers=headers)

jsonObj = json.loads(r.text)

temp = jsonObj["result"]["uplink_message"]["decoded_payload"]["temp"]
humi = jsonObj["result"]["uplink_message"]["decoded_payload"]["humi"]
volt = jsonObj["result"]["uplink_message"]["decoded_payload"]["volt"]

st.subheader(str(devices[2]))
col1, col2, col3 = st.columns(3)
col1.metric(label="Temperature", value=temp)
col2.metric(label="Humidity", value=humi)
col3.metric(label="Battery Voltage", value=volt)

link = baseUrlDev+devices[0]+"/packages/storage/"+types[1]+"?limit=1"
r = requests.get(link,headers=headers)

jsonObj = json.loads(r.text)

temp = jsonObj["result"]["uplink_message"]["decoded_payload"]["temp"]
humi = jsonObj["result"]["uplink_message"]["decoded_payload"]["humi"]
volt = "∞"

st.subheader(str(devices[0]))
col1, col2, col3 = st.columns(3)
col1.metric(label="Temperature", value=temp)
col2.metric(label="Humidity", value=humi)
col3.metric(label="Battery Voltage", value=volt)