import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Officer Mess Chhawla",
    page_icon="🏨",
    layout="wide"
)

SHEET_URL = "https://docs.google.com/spreadsheets/d/1Kxbp6W4cb-_k9LD9V--ZJsysEDrcg3whYPj2TuHKfwU/edit"

@st.cache_data(ttl=300)
def load_data():
    url = SHEET_URL.replace("/edit", "/export?format=csv")
    df = pd.read_csv(url)

    return df


st.title("Officer Mess Chhawla")
st.caption("Occupancy & Booking Dashboard")

try:
    df = load_data()

    st.success(f"Connected to Google Sheet — {len(df)} records loaded")

    st.subheader("Raw Booking Data")
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

except Exception as e:
    st.error("Unable to load the Google Sheet.")
    st.exception(e)
