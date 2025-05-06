
import streamlit as st

st.set_page_config(layout="wide")
st.title("ETL Dependency Chain Viewer (Fully Connected)")
st.write("Hover over any ETL job to see inputs/outputs. Click to focus and explore.")

with open("etl_static_net.html", "r", encoding="utf-8") as f:
    html_content = f.read()

st.components.v1.html(html_content, height=900, scrolling=True)
