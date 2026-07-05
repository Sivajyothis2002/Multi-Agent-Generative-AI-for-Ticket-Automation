import streamlit as st
import requests
import time
import base64

# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(
    page_title="Neural Routing AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================================================
# LOAD BACKGROUND IMAGE
# ==================================================
def get_base64(image_path):
    try:
        with open(image_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except:
        return ""

# Ensure this path is correct for your local machine
bg_image = get_base64("assets/zach-m-7F9PhBM1gFM-unsplash.jpg")

# ==================================================
# ELITE CYBER-NOIR CSS
# ==================================================
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syncopate:wght@400;700&family=Inter:wght@300;400;700&display=swap');

/* GLOBAL DEFAULTS */
.stApp {{
    background: url("data:image/jpeg;base64,{bg_image}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    color: #ffffff;
    font-family: 'Inter', sans-serif;
    overflow: hidden;
}}

/* PUT IT HERE */
header,
[data-testid="stHeader"] {{
    background: transparent !important;
}}

header::before {{
    content: "";

    position: fixed;

    top: 0;
    left: 0;

    width: 100%;
    height: 180px;

    background: linear-gradient(
        to bottom,
        rgba(0,0,0,0.75) 0%,
        rgba(0,0,0,0.45) 35%,
        rgba(0,0,0,0.12) 70%,
        transparent 100%
    );

    pointer-events: none;

    z-index: 999;
}}
/* RECLAIMING VIEWPORT SPACE */
.block-container {{
    padding: 0rem !important;
    max-width: 100%;
}}

/* ANIMATION DEFINITIONS */
@keyframes letterSpacingReveal {{
    0% {{ opacity: 0; letter-spacing: 25px; filter: blur(20px); transform: translateY(30px); }}
    100% {{ opacity: 1; letter-spacing: 4px; filter: blur(0px); transform: translateY(0); }}
}}

@keyframes subFadeIn {{
    0% {{ opacity: 0; transform: translateY(10px); }}
    100% {{ opacity: 1; transform: translateY(0); }}
}}

@keyframes borderGlow {{
    0%, 100% {{ border-color: rgba(255,255,255,0.1); }}
    50% {{ border-color: rgba(255,255,255,0.5); }}
}}
@keyframes cinematicLeft {{
    0% {{
        opacity: 0;
        transform: translateX(-120px);
        filter: blur(12px);
        letter-spacing: 18px;
    }}

    100% {{
        opacity: 1;
        transform: translateX(0px);
        filter: blur(0px);
        letter-spacing: 12px;
    }}
}}

@keyframes cinematicRight {{
    0% {{
        opacity: 0;
        transform: translateX(120px);
        filter: blur(12px);
        letter-spacing: 14px;
    }}

    100% {{
        opacity: 1;
        transform: translateX(0px);
        filter: blur(0px);
        letter-spacing: 6px;
    }}
}}

/* HERO PAGE STYLING */
.hero-wrapper {{
    height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: flex-end; /* Keeps center clear for background AI image */
    align-items: center;
    text-align: center;
    padding-bottom: 10vh;
    background: radial-gradient(circle, rgba(0,0,0,0) 30%, rgba(0,0,0,0.8) 100%);
}}

.hero-title {{
    font-family: 'Syncopate', sans-serif;
    font-size: clamp(40px, 5vw, 65px);
    font-weight: 700;
    text-transform: uppercase;
    margin-bottom: 0px;
    background: linear-gradient(180deg, #ffffff 0%, #64748b 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: letterSpacingReveal 2s cubic-bezier(0.19, 1, 0.22, 1) both;
}}

.hero-subtitle {{
    font-size: 12px;
    font-weight: 300;
    color: #94a3b8;
    letter-spacing: 8px;
    text-transform: uppercase;
    margin-top: 15px;
    animation: subFadeIn 1.5s ease-out 1s both;
}}

/* SECOND PAGE INTERFACE */
.interface-container {{
    padding: 10vh 15% 0 15%;
    animation: subFadeIn 1s ease-out;
}}

.glass-card {{
    background: rgba(5, 5, 5, 0.8);
    backdrop-filter: blur(30px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    padding: 50px;
    box-shadow: 0 0 50px rgba(0,0,0,0.8);
    animation: borderGlow 4s infinite;
}}

/* INTERACTIVE BUTTONS */
div.stButton > button {{
    width: 100%;
    background: transparent;
    border: 1px solid rgba(255,255,255,0.4);
    color: #fff;
    font-family: 'Syncopate', sans-serif;
    padding: 18px;
    letter-spacing: 4px;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    border-radius: 0px;
    text-transform: uppercase;
    margin-top: 20px;
}}

div.stButton > button:hover {{
    background: #ffffff;
    color: #000000;
    box-shadow: 0 0 40px rgba(255,255,255,0.3);
    transform: translateY(-2px);
}}

/* UI DECORATION */
.status-bar {{
    position: fixed;
    bottom: 20px;
    left: 40px;
    font-size: 10px;
    color: rgba(255,255,255,0.2);
    letter-spacing: 3px;
    text-transform: uppercase;
}}

</style>
""", unsafe_allow_html=True)

# ==================================================
# SESSION STATE
# ==================================================
if "started" not in st.session_state:
    st.session_state.started = False

# ==================================================
# PAGE 1: MOTION POSTER LANDING
# ==================================================
if not st.session_state.started:
    st.markdown("""
<div class="hero-wrapper">
    <div class="hero-title">AI Ticket Routing</div>
    <div class="hero-subtitle">Multi-Agent Intelligence System</div>
</div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="display:flex; justify-content:center; margin-top:20px;">
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1.75, 0.8, 1.55])

    with c2:
        if st.button("Initialize Core"):
            st.session_state.started = True
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
else:
    # Minimalist CSS to blur background and make inputs transparent
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

    /* REMOVE ALL STREAMLIT BOX ARTIFACTS */
    [data-testid="stVerticalBlockBorderWrapper"] {{
        border: none !important;
        background-color: transparent !important;
        box-shadow: none !important;
    }}
    
    /* REMOVE THE GLASS CARD CONTAINER */
    .glass-card {{
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        backdrop-filter: none !important;
        padding: 0px !important;
        width: 100%;
        max-width: 900px;
        margin: auto;
    }}

    /* HUD-STYLE INPUTS */
    div[data-baseweb="input"], 
    div[data-baseweb="textarea"],
    div[data-baseweb="base-input"] {{

        background-color: rgba(255,255,255,0.02) !important;

        border: 1px solid rgba(255, 255, 255, 0.18) !important;

        border-radius: 2px !important;

        backdrop-filter: blur(8px);

        transition: all 0.4s ease !important;
    }}

    /* INPUT TEXT */
    textarea,
    input {{

        background-color: transparent !important;

        color: white !important;
    }}

    /* SUBTLE FOCUS GLOW */
    div[data-baseweb="input"]:focus-within, 
    div[data-baseweb="textarea"]:focus-within {{

        border-color: rgba(255, 255, 255, 0.45) !important;

        background-color: rgba(255, 255, 255, 0.04) !important;

        box-shadow: 0 0 20px rgba(255,255,255,0.06);
    }}

    /* CLEAN WHITE LABELS */
    label p {{

        font-family: 'Syncopate', sans-serif !important;

        font-size: 9px !important;

        letter-spacing: 2px !important;

        color: #ffffff !important;

        text-transform: uppercase;

        opacity: 0.8;
    }}

    /* BUTTONS */
    div.stButton > button {{

        background: rgba(255,255,255,0.03);

        border: 1px solid rgba(255,255,255,0.15);

        color: white;

        backdrop-filter: blur(10px);

        font-family: 'Syncopate', sans-serif;

        letter-spacing: 3px;

        transition: all 0.4s ease;

        height: 55px;
    }}

    div.stButton > button:hover {{

        background: rgba(255,255,255,0.08);

        border: 1px solid rgba(255,255,255,0.35);

        transform: translateY(-2px);

        box-shadow: 0 0 25px rgba(255,255,255,0.08);
    }}

    /* HIDE SYSTEM OVERLAYS */
    footer {{visibility: hidden;}}

    /* REMOVE TOP OVERLAY FROM PAGE 2 */
    

    /* REMOVE HEADER EFFECT */
    header,
    [data-testid="stHeader"] {{

        background: transparent !important;

        backdrop-filter: none !important;
    }}

    .stMainBlockContainer {{
        padding-top: 5rem !important;
    }}

    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="interface-container">', unsafe_allow_html=True)
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    # Minimalist Header
    st.markdown(
        '''
        <h2 style="
            font-family: 'Times New Roman', serif;
            font-size: 44px;
            font-weight: 400;
            letter-spacing: 18px;
            margin-bottom: 6px;
            color: rgba(255,255,255,0.96);
            text-align: center;
            text-transform: uppercase;
            animation: cinematicLeft 2s cubic-bezier(0.19, 1, 0.22, 1) both;
        ">
        SERVICE MANAGEMENT CONSOLE
        </h2>
        ''',
        unsafe_allow_html=True
    )

    st.markdown(
        '''
        <p style="
            font-family:'Times New Roman', serif;
            font-size:15px;
            font-weight:400;
            letter-spacing:8px;
            color:rgba(255,255,255,0.62);
            margin-bottom:25px;
            text-align:center;
            text-transform:uppercase;
            animation: cinematicRight 2.2s cubic-bezier(0.19, 1, 0.22, 1) both;
        ">
        Autonomous Service Operations Platform
        </p>
        ''',
        unsafe_allow_html=True
    )
    # Inputs
    subject = st.text_input(
        "IDENTIFIER / SUBJECT",
        placeholder="Specify the ticket vector..."
    )
    body = st.text_area(
        "RAW DATA / DESCRIPTION",
        placeholder="Enter logs for analysis...",
        height=250
    )
    st.markdown(
        '<div style="margin-top:30px;"></div>',
        unsafe_allow_html=True
    )
    
    col_a, col_b = st.columns([1.55, 2.35])

    with col_a:
        if st.button("⬅ Exit System"):
            st.session_state.started = False
            st.rerun()
    result = None
    # ==================================================
# PROCESS BUTTON
# ==================================================

    result = None
    with col_b:
        if st.button("⚡ Process Data"):
            if subject and body:
                payload = {
                    "subject": subject,
                    "body": body
                }
                with st.spinner("AI Agents Processing Ticket..."):
                    try:
                        response = requests.post(
                            "http://host.docker.internal:8000/predict",
                            json=payload
                        )
                        result = response.json()
                    except Exception as e:

                        st.error(f"API CONNECTION FAILED: {e}")
            else:
                st.error("DATA MISSING")

    # ==================================================
    # FULL WIDTH RESULTS UI
    # ==================================================

    if result:
        st.markdown("""
        <style>
        @keyframes fadeSlideUp {
            0% {
                opacity: 0;
                transform: translateY(40px);
                filter: blur(12px);
            }
            100% {
                opacity: 1;
                transform: translateY(0px);
                filter: blur(0px);
            }
        }
        .cinematic-card {
            background: rgba(255,255,255,0.035);
            border: 1px solid rgba(255,255,255,0.08);
            backdrop-filter: blur(14px);
            padding: 28px;
            text-align: center;
            border-radius: 18px;
            transition: all 0.4s ease;
            animation: fadeSlideUp 0.8s ease forwards;
            overflow: hidden;
            position: relative;
        }
        .cinematic-card:hover {
            transform: translateY(-4px);
            border-color: rgba(255,255,255,0.18);
            box-shadow: 0 0 35px rgba(255,255,255,0.06);
        }
        .cinematic-card::before {
            content: "";
            position: absolute;
            inset: 0;
            background: linear-gradient(
                135deg,
                rgba(255,255,255,0.04),
                transparent 50%
            );
            pointer-events: none;
        }
        .response-panel {
            width: 100%;
            margin-top: 40px;
            background: rgba(8,12,24,0.78);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 26px;
            overflow: hidden;
            backdrop-filter: blur(20px);
            box-shadow: 0 0 50px rgba(0,0,0,0.45);
            animation: fadeSlideUp 1s ease;
        }
        .response-header {
            padding: 22px 32px;
            border-bottom: 1px solid rgba(255,255,255,0.06);
            background: linear-gradient(
                90deg,
                rgba(0,255,170,0.08),
                rgba(255,255,255,0.02)
            );
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .response-title {
            color: #7CFFB2;
            font-size: 13px;
            letter-spacing: 5px;
            font-family: 'Syncopate', sans-serif;
            text-transform: uppercase;
        }
        .response-dot {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: #00ff88;
            box-shadow: 0 0 18px #00ff88;
        }
        .response-body {
            padding: 48px;
            color: rgba(255,255,255,0.92);
            font-size: 18px;
            line-height: 2.1;
            font-family: 'Inter', sans-serif;
            letter-spacing: 0.3px;
        }
        </style>
        """, unsafe_allow_html=True)
        st.success("ANALYSIS COMPLETE")

        # =========================
        # RESULT CARDS
        # =========================

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(f"""
            <div class="cinematic-card">
                <p style="
                    letter-spacing:4px;
                    font-size:11px;
                    opacity:0.55;
                    margin-bottom:20px;
                    text-transform:uppercase;
                ">
                Type
                </p>
                <h2 style="
                    font-weight:400;
                    color:white;
                ">
                {result["predicted_type"]}
                </h2>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="cinematic-card">
                <p style="
                    letter-spacing:4px;
                    font-size:11px;
                    opacity:0.55;
                    margin-bottom:20px;
                    text-transform:uppercase;
                ">
                Priority
                </p>
                <h2 style="
                    font-weight:400;
                    color:white;
                ">
                {result["predicted_priority"]}
                </h2>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class="cinematic-card">
                <p style="
                    letter-spacing:4px;
                    font-size:11px;
                    opacity:0.55;
                    margin-bottom:20px;
                    text-transform:uppercase;
                ">
                Queue
                </p>
                <h2 style="
                    font-weight:400;
                    color:white;
                ">
                {result["predicted_queue"]}
                </h2>
            </div>
            """, unsafe_allow_html=True)

        # =========================
        # CLEAN RESPONSE
        # =========================

        clean_response = result["generated_response"] \
            .replace("<p>", "") \
            .replace("</p>", "") \
            .replace("<br>", "<br><br>")

        # =========================
        # CINEMATIC RESPONSE PANEL
        # =========================

        st.markdown(
            f"""
            <div class="response-panel">
                <div class="response-header">
                    <div class="response-title">
                        GENERATED RESPONSE
                    </div>
                    <div class="response-dot"></div>
                </div>
                <div class="response-body">
                    {clean_response}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)