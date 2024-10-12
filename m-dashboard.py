import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from threading import Thread
import requests

# FastAPI setup for endpoints
app = FastAPI()

class InfoRequest(BaseModel):
    message: str

@app.get("/info")
async def get_info():
    return {"message": "This is data from the sub-app hosted in Streamlit Cloud."}

# Run FastAPI server in a separate thread
def run_fastapi():
    uvicorn.run(app, host="0.0.0.0", port=8001)

thread = Thread(target=run_fastapi)
thread.setDaemon(True)
thread.start()

# Streamlit UI for the dashboard
st.set_page_config(layout="wide", page_title="Master Streamlit Dashboard")

# Sidebar - App title and input widgets
st.sidebar.title("Network Map Dashboard")
year = st.sidebar.selectbox("Select Year", [2019, 2020, 2021, 2022])
color_theme = st.sidebar.selectbox("Select Color Theme", ["Blues", "Reds", "Greens"])

# Columns Layout
col1, col2, col3 = st.columns([1, 2, 1])

# Column 1 - States with Highest Inbound/Outbound Migration
with col1:
    st.subheader("Gains/Losses")
    st.metric(label="Texas", value="29.0 M", delta="+3.7 K")
    st.metric(label="New York", value="19.5 M", delta="-27 K")
    
    st.subheader("States Migration")
    st.metric(label="Inbound", value="23%")
    st.metric(label="Outbound", value="3%")

    # Percentage of states with migration > 50,000
    st.subheader("Migration > 50,000")
    st.write("23% of states have annual inbound migration greater than 50,000.")

# Column 2 - Network Map Visualization
with col2:
    st.subheader("Master and Sub-App Network")
    
    # Create a NetworkX graph
    G = nx.Graph()
    
    # Add nodes for master and sub-apps
    G.add_node("Master App", size=3000, color='skyblue')
    G.add_node("Sub-App 1", size=2000, color='lightgreen')
    G.add_node("Sub-App 2", size=2000, color='lightgreen')
    G.add_node("Sub-App 3", size=2000, color='lightgreen')
    
    # Add edges between master app and sub-apps
    G.add_edge("Master App", "Sub-App 1")
    G.add_edge("Master App", "Sub-App 2")
    G.add_edge("Master App", "Sub-App 3")
    
    # Draw the network graph
    pos = nx.spring_layout(G)
    plt.figure(figsize=(10, 6))
    nx.draw(G, pos, with_labels=True, node_size=[G.nodes[n]['size'] for n in G.nodes], node_color=[G.nodes[n]['color'] for n in G.nodes], font_size=10, font_color='black')
    
    # Display network map in Streamlit
    st.pyplot(plt)

# Column 3 - Top States by Population
with col3:
    st.subheader("Top States")
    # Placeholder data for visualization
    data = {
        "State": ["California", "Texas", "Florida", "New York", "Illinois"],
        "Population": [39500000, 29000000, 21500000, 19500000, 12500000]
    }
    df = pd.DataFrame(data)
    st.write("State population shown in descending order.")
    st.table(df.sort_values(by="Population", ascending=False))

    # Further Information
    st.subheader("About")
    st.write("Data source: US Census Bureau")
    st.write("Gains/Losses: States with high inbound/outbound migration for selected year.")
    st.write("States Migration: Percentage of states with annual inbound/outbound migration > 50,000.")

# Custom Interactions Section
st.header("Interact with Hosted Endpoints")
if st.button("Get Info from Hosted Endpoint"):
    try:
        response = requests.get("http://localhost:8001/info")
        if response.status_code == 200:
            st.write("Hosted Endpoint Response:", response.json())
        else:
            st.error(f"Failed to connect to the hosted endpoint. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to the hosted endpoint: {e}")
