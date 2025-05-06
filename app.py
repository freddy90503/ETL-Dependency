
import streamlit as st
from PIL import Image

st.set_page_config(layout="wide")
st.title("ETL Dependency Chain (Final Accurate Version)")
st.write("This static graph shows the complete dependency map using all 156 ETL rows. Zoom with your browser to view details.")

import os
image = Image.open(os.path.join(os.path.dirname(__file__), "etl_dependency_graph_complete.png"))
st.image(image, use_column_width=True)
