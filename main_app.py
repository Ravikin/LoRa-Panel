import streamlit as st
import requests
import json
import pandas as pd
import numpy as np
import folium

headers = {'Accept': 'application/json', 'Authorization':'Bearer NNSXS.KNEAMVSK4GGOAJ6ZQT5GF4GI44WFDHG6BMGLOZQ.COQXVOSUBLBX7HGVTYWXNZYODOV3V5O2Z5SSSUJES6CFWEP5JCHQ'}
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
st.metric(label="Temperature", value=temp)
st.metric(label="Humidity", value=humi)
st.metric(label="Battery Voltage", value=volt)