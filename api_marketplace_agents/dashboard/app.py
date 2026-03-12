import streamlit as st
import requests

st.title("AI API Marketplace Negotiation System")

query = st.text_input("Enter your API requirement")

if st.button("Find Best API"):

    url = "http://127.0.0.1:8000/select-api"

    response = requests.post(url, params={"query": query})

    data = response.json()

    st.subheader("Results")

    st.write("Service:", data["requirements"]["service"])
    st.write("Best API:", data["selected_api"])
    st.write("Monitoring Status:", data["monitoring_status"])