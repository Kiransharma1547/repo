import streamlit as st
from modules import app, aws, linux

st.set_page_config(page_title="Multi-Module Platform", layout="centered")

st.title("📦 Modular Streamlit Platform")
st.markdown("Select a module to run its logic below:")

module_choice = st.sidebar.radio("Choose Module", ["App", "AWS", "Linux"])

st.divider()

if module_choice == "App":
    result = app.run()
elif module_choice == "AWS":
    result = aws.run()
elif module_choice == "Linux":
    result = linux.run()
else:
    result = "Please select a valid module."

st.success(result)
