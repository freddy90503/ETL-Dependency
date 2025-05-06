
import streamlit as st
import pandas as pd
from pyvis.network import Network
import networkx as nx
import tempfile
import os

# Load data
df = pd.read_csv("etl_dependencies.csv")

# Initialize a directed NetworkX graph
G = nx.DiGraph()

# Add nodes and edges to graph
for _, row in df.iterrows():
    etl = row["ETL"]
    input_data = row["Input"]
    output_data = row["Output"]

    # Create a connection: input -> ETL -> output
    if pd.notna(input_data):
        G.add_edge(input_data, etl, label="input")

    if pd.notna(output_data):
        G.add_edge(etl, output_data, label="output")

# Create Pyvis network from the graph
net = Network(height="900px", width="100%", bgcolor="#ffffff", font_color="black", directed=True)

# Customize physics for spacing
net.barnes_hut()

# Add all nodes with full input/output details as tooltips
for node in G.nodes:
    label = node
    tooltip = ""

    # If it's an ETL job, add input/output details
    if node in df["ETL"].values:
        inputs = df[df["ETL"] == node]["Input"].dropna().unique()
        outputs = df[df["ETL"] == node]["Output"].dropna().unique()
        tooltip += f"<b>{label}</b><br><b>Inputs:</b><br>" + "<br>".join(inputs) + "<br><b>Outputs:</b><br>" + "<br>".join(outputs)
        net.add_node(node, label=label, title=tooltip, shape="box", color="#AED6F1")
    else:
        # It's a data source or sink
        net.add_node(node, label=label, title=node, shape="ellipse", color="#F9E79F")

# Add edges
for source, target in G.edges:
    net.add_edge(source, target)

# Save to HTML
tmp_dir = tempfile.gettempdir()
html_path = os.path.join(tmp_dir, "etl_net_fullscreen.html")
net.save_graph(html_path)

# Streamlit UI
st.set_page_config(layout="wide")
st.title("ETL Dependency Visualization")
st.write("**Hover** over an ETL to see its inputs/outputs. **Click** a node to highlight its connections. Use your mouse to zoom and drag.")

# Render the HTML graph
with open(html_path, "r", encoding="utf-8") as f:
    html_content = f.read()
st.components.v1.html(html_content, height=900, scrolling=True)
