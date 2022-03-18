import streamlit as st
import pandas as pd
import requests
import json
from os.path import exists
from collections import Counter


  # Requires the PyMongo package.
# https://api.mongodb.com/python/current

# insertOne_URI = "https://data.mongodb-api.com/app/data-qhlxu/endpoint/data/beta/action/insertOne"
# findOne_URI = "https://data.mongodb-api.com/app/data-qhlxu/endpoint/data/beta/action/findOne"
# find_URI = "https://data.mongodb-api.com/app/data-qhlxu/endpoint/data/beta/action/find"
# insertMany_URI = "https://data.mongodb-api.com/app/data-qhlxu/endpoint/data/beta/action/insertMany"
# updateOne_URI = "https://data.mongodb-api.com/app/data-qhlxu/endpoint/data/beta/action/updateOne"

# headers = {'Content-Type': 'application/json', 'Access-Control-Request-Headers': '*', 'api-key': 'a2pJneejPLob94PzqiGZbsJqzxHnIEmyDXFG8S3QqZUHGQAkky00piofpaJTiJap'}

# find_payload = json.dumps({"collection": "posts", "database": "ethiopian_music", "dataSource": "Cluster0", "filter": {"_id":link[i]}})
# update_payload = json.dumps({"collection": "posts", "database": "ethiopian_music", "dataSource": "Cluster0", "filter": {"_id":link[i]}, "update": {"$set": {"views": "complete"}}})

# response = requests.request("POST", find_URI, headers=headers, data=payload)

channel_list = pd.read_csv('link.csv')
channels_list = ['All Sources']
data = {}
frame = []
for name in channel_list['Names'].values:
    file_path = f'{name}.csv'
    if exists(file_path):
      channels_list.append(name)
      df = pd.read_csv(file_path)
      data[name] = df
      frame.append(df)
result = pd.concat(frame)

data['All Sources'] = result

def channel_data(data, option, period):
  if period == "Last Week":
    df = data[option].sort_values("view_delta", ascending=False)
    df = df.drop_duplicates()
  elif period == "All Time":
    df = data[option].sort_values("Views_03/12", ascending=False)
    df = df.drop_duplicates()
    
  if df.shape[0]>100:
    return df[['Posts', 'Channel', 'Views_03/03', 'Views_03/12', 'view_delta']].head(100)
  else:
    return df[['Posts', 'Channel','Views_03/03', 'Views_03/12', 'view_delta']]

st.header("Music Chart")
container_00 = st.container()

c1, c2 = container_00.columns(2)

channels = c1.selectbox("Channels", channels_list)
period = c2.selectbox("Period", ["Last Week","All Time"])


chart = container_00.table(channel_data(data, channels, period))