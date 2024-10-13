import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network

# Streamlit UI for the dashboard
st.set_page_config(layout="wide", page_title="C2 Network Dashboard")

# Sidebar - App title and input widgets
st.sidebar.title("Command & Control (C2) Network Dashboard")
year = st.sidebar.selectbox("Select Year", [2019, 2020, 2021, 2022])
color_theme = st.sidebar.selectbox("Select Color Theme", ["Blues", "Reds", "Greens"])

# Columns Layout
col1, col2, col3 = st.columns([1, 2, 1])

# Column 2 - C2 Network Visualization
with col2:
    st.subheader("C2 Node and Subordinate Nodes Network Visualization")

    # Create a directed NetworkX graph to show flow direction
    G = nx.DiGraph()  # Using a directed graph for command flow representation

    # Add nodes with C2-specific attributes
    G.add_node("Master Node", size=5000, color='red', label='Command Node', role='C2')
    G.add_node("Sub-Node 1", size=3000, color='yellow', label='Bot 1', role='Subordinate')
    G.add_node("Sub-Node 2", size=3000, color='yellow', label='Bot 2', role='Subordinate')
    G.add_node("Sub-Node 3", size=3000, color='yellow', label='Bot 3', role='Subordinate')

    # Add directional edges representing commands and responses
    G.add_edge("Master Node", "Sub-Node 1", command="Command: Scan Network", weight=3)
    G.add_edge("Master Node", "Sub-Node 2", command="Command: Gather Data", weight=3)
    G.add_edge("Master Node", "Sub-Node 3", command="Command: Report Status", weight=3)

    # Add reverse edges to represent responses
    G.add_edge("Sub-Node 1", "Master Node", command="Response: Scan Completed", weight=1)
    G.add_edge("Sub-Node 2", "Master Node", command="Response: Data Collected", weight=1)
    G.add_edge("Sub-Node 3", "Master Node", command="Response: Status OK", weight=1)

    # Draw the network graph for C2 structure
    pos = nx.spring_layout(G, seed=42)  # Use a fixed layout for consistency

    plt.figure(figsize=(12, 8))
    nx.draw_networkx_nodes(G, pos, node_size=[G.nodes[n]['size'] for n in G.nodes], node_color=[G.nodes[n]['color'] for n in G.nodes])
    nx.draw_networkx_labels(G, pos, labels={n: n for n in G.nodes}, font_size=10, font_color='black')
    nx.draw_networkx_edges(G, pos, edgelist=G.edges(), edge_color='gray', arrows=True, arrowstyle='-|>', arrowsize=15, width=2)

    # Display network map in Streamlit
    st.pyplot(plt)

# Column 3 - Interactive C2 Network Visualization with Pyvis
with col3:
    st.subheader("Interactive C2 Network Visualization")

    # Creating an interactive network with Pyvis
    net = Network(height="700px", width="100%", bgcolor="#222222", font_color="white", directed=True)

    # Add C2 nodes with detailed attributes
    net.add_node("Master Node", size=60, color='red', title="Master Command Node")
    net.add_node("Sub-Node 1", size=40, color='yellow', title="Subordinate Node 1")
    net.add_node("Sub-Node 2", size=40, color='yellow', title="Subordinate Node 2")
    net.add_node("Sub-Node 3", size=40, color='yellow', title="Subordinate Node 3")

    # Add command edges (directed from Master to Sub-nodes)
    net.add_edge("Master Node", "Sub-Node 1", title="Command: Scan Network")
    net.add_edge("Master Node", "Sub-Node 2", title="Command: Gather Data")
    net.add_edge("Master Node", "Sub-Node 3", title="Command: Report Status")

    # Add response edges (directed from Sub-nodes to Master)
    net.add_edge("Sub-Node 1", "Master Node", title="Response: Scan Completed")
    net.add_edge("Sub-Node 2", "Master Node", title="Response: Data Collected")
    net.add_edge("Sub-Node 3", "Master Node", title="Response: Status OK")

    # Save and display the network graph
    net.save_graph("c2_network.html")
    st.components.v1.html(open("c2_network.html", 'r', encoding='utf-8').read(), height=700)
