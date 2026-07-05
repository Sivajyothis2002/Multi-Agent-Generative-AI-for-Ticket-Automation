import streamlit as st
import pandas as pd
import requests
import base64


# =========================================
# PAGE CONFIG
# =========================================
st.set_page_config(
    page_title="System History Logs",
    layout="wide"
)


# =========================================
# LOAD BG IMAGE
# =========================================
def get_base64(file_path):

    with open(file_path, "rb") as f:
        data = f.read()

    return base64.b64encode(data).decode()


bg_image = get_base64(
    "assets/zach-m-7F9PhBM1gFM-unsplash.jpg"
)


# =========================================
# CINEMATIC UI CSS
# =========================================
st.markdown(f"""
<style>

.stApp {{

    position: relative;

    background: url("data:image/jpeg;base64,{bg_image}") !important;

    background-size: cover !important;
    background-position: center !important;
    background-attachment: fixed !important;

    overflow: hidden;
}}

/* BLURRED CINEMATIC LAYER */
.stApp::before {{

    content: "";

    position: fixed;

    inset: 0;

    background: url("data:image/jpeg;base64,{bg_image}");

    background-size: cover;
    background-position: center;
    background-attachment: fixed;

    filter: blur(10px) brightness(0.78);

    transform: scale(1.04);

    z-index: 0;
}}

/* SOFT OVERLAY */
.stApp::after {{

    content: "";

    position: fixed;

    inset: 0;

    background: rgba(0,0,0,0.10);

    z-index: 1;
}}

/* KEEP CONTENT ABOVE EVERYTHING */
.main,
.block-container,
[data-testid="stAppViewContainer"] {{

    position: relative;

    z-index: 2;
}}

/* REMOVE STREAMLIT BOXES */
[data-testid="stVerticalBlockBorderWrapper"] {{
    border: none !important;
    background-color: transparent !important;
    box-shadow: none !important;
}}

/* REMOVE HEADER */
header,
[data-testid="stHeader"] {{

    background: transparent !important;

    backdrop-filter: none !important;
}}

footer {{
    visibility: hidden;
}}

/* PAGE SPACING */
.stMainBlockContainer {{
    padding-top: 4rem !important;
    padding-bottom: 0rem !important;
}}

/* TITLE */
.history-title {{

    font-family: 'Times New Roman', serif;

    font-size: 48px;

    letter-spacing: 18px;

    color: rgba(255,255,255,0.95);

    text-align: center;

    margin-bottom: 8px;

    text-transform: uppercase;
}}

.history-subtitle {{

    font-family: 'Times New Roman', serif;

    font-size: 15px;

    letter-spacing: 8px;

    color: rgba(255,255,255,0.65);

    text-align: center;

    margin-bottom: 40px;

    text-transform: uppercase;
}}

/* TABLE CONTAINER */
[data-testid="stDataFrame"] {{

    background: rgba(255,255,255,0.03) !important;

    border: 1px solid rgba(255,255,255,0.08) !important;

    border-radius: 10px;

    backdrop-filter: blur(12px);

    padding: 10px;
}}

/* TABLE TEXT */
[data-testid="stDataFrame"] * {{

    color: white !important;
}}

/* SCROLLBAR */
::-webkit-scrollbar {{
    width: 8px;
}}

::-webkit-scrollbar-thumb {{
    background: rgba(255,255,255,0.2);
    border-radius: 10px;
}}

</style>
""", unsafe_allow_html=True)


# =========================================
# HEADER
# =========================================
st.markdown("""
<div class="history-title">
SYSTEM HISTORY LOGS
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="history-subtitle">
Autonomous Ticket Intelligence Archive
</div>
""", unsafe_allow_html=True)


# =========================================
# FETCH HISTORY
# =========================================
try:

    response = requests.get(
        "http://host.docker.internal:8000/history"
    )

    data = response.json()

    df = pd.DataFrame(data)

    if len(df) > 0:

        st.dataframe(
            df,
            use_container_width=True,
            height=600
        )

    else:

        st.warning("No history records found.")

except Exception as e:

    st.error(f"Unable to load history: {e}")