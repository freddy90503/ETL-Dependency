
import streamlit as st
import pandas as pd
from pyvis.network import Network
import networkx as nx
import tempfile
import os

# Load data
df = pd.read_csv("etl_dependencies.csv")

# Create a directed graph
G = nx.DiGraph()

# Add nodes and edges
for _, row in df.iterrows():
    source = row["ETL"]
    target = row["Output"]
    input_info = row["Input"]
    output_info = row["Output"]

    # Edge from ETL to its output
    G.add_edge(source, target, label="produces")

    # Edge from input to ETL (to infer full chain)
    G.add_edge(input_info, source, label="used by")

# Create Pyvis Network
net = Network(height="750px", width="100%", directed=True, bgcolor="#ffffff", font_color="black")
net.from_nx(G)

# Customize nodes with tooltips
for node in net.nodes:
    label = node["label"]
    if label in df["ETL"].values:
        inputs = df[df["ETL"] == label]["Input"].dropna().unique()
        outputs = df[df["ETL"] == label]["Output"].dropna().unique()
        node["title"] = f"<b>{label}</b><br>Inputs:<br>" + "<br>".join(inputs) + "<br><br>Outputs:<br>" + "<br>".join(outputs)
        node["color"] = "#AED6F1"
    else:
        node["title"] = label
        node["color"] = "#F9E79F"

# Enable physics and interaction
net.toggle_physics(True)

# Save to HTML
tmp_dir = tempfile.gettempdir()
html_path = os.path.join(tmp_dir, "etl_net.html")
net.save_graph(html_path)

# Display in Streamlit
st.title("ETL Dependency Visualization")
st.write("Hover to see inputs/outputs. Click to highlight connections.")
st.components.v1.html(open(html_path, "r", encoding="utf-8").read(), height=800, scrolling=True)
