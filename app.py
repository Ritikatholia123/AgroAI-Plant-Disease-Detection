import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from PIL import Image
from tensorflow.keras.models import load_model

from disease_data import disease_info, class_names
from utils import predict_disease
from report import show_report, generate_pdf
import os


# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title=" AgroAI Pro",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# LOAD CSS
# =====================================================

try:
    with open("style.css") as css:
        st.markdown(
            f"<style>{css.read()}</style>",
            unsafe_allow_html=True
        )
except FileNotFoundError:
    st.warning("style.css not found.")

# =====================================================
# LOAD MODEL
# =====================================================

MODEL_PATH = "model/plant_disease_model.keras"


@st.cache_resource
def get_model():
    return load_model(MODEL_PATH)


try:
    model = get_model()

except Exception as e:
    st.error(f"❌ Model Loading Error\n\n{e}")
    st.stop()

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.image(
    "https://cdn-icons-png.flaticon.com/512/2909/2909767.png",
    width=120
)

st.sidebar.title("🌿 AgroAI Pro")

st.sidebar.markdown("""
### Smart Plant Disease Detection

✅ AI Powered

✅ CNN Model

✅ PDF Report

✅ Farming Guide

✅ Organic Control

✅ Deep Learning
""")

st.sidebar.markdown("---")

st.sidebar.success("🌱 Healthy Plants, Healthy Future")

# =====================================================
# HERO SECTION
# =====================================================

st.markdown("""
<div class="hero">

<h1>🌿 AgroAI Pro</h1>

<h3>AI Powered Plant Disease Detection</h3>

<p>
Upload a plant leaf image and instantly detect disease using Deep Learning.
</p>

</div>
""", unsafe_allow_html=True)

st.divider()

st.success("🌿 Welcome to AgroAI Pro", icon="🌱")

# =====================================================
# IMAGE UPLOADER
# =====================================================

st.subheader("📤 Upload Plant Leaf Image")

uploaded_file = st.file_uploader(
    "Choose a plant leaf image",
    type=["jpg", "jpeg", "png"]
)
# =====================================================
# PREDICTION
# =====================================================

if uploaded_file is not None:

    # Load Image
    image = Image.open(uploaded_file).convert("RGB")

    # Prediction
    with st.spinner("🔍 AI is analyzing the leaf..."):
        disease, confidence, prediction = predict_disease(
            model,
            image,
            class_names
        )

    info = disease_info[disease]

    # =============================
    # LAYOUT
    # =============================

    col1, col2 = st.columns([1, 2], gap="large")

    # -----------------------------
    # LEFT : IMAGE
    # -----------------------------

    with col1:

        st.image(
            image,
            caption="📷 Uploaded Leaf",
            use_container_width=True
        )

    # -----------------------------
    # RIGHT : RESULT
    # -----------------------------

    with col2:

        st.success("✅ Prediction Completed Successfully")

        st.markdown(f"""
        <div class="disease-card">
            <h2>🌿 {disease.replace("_"," ")}</h2>
            <h4>Confidence : {confidence:.2f}%</h4>
        </div>
        """, unsafe_allow_html=True)

        fig = go.Figure(
            go.Indicator(

                mode="gauge+number",

                value=confidence,

                number={
                    "suffix": "%",
                    "font": {
                        "size": 42,
                        "color": "white"
                    }
                },

                title={
                    "text": "Confidence Score",
                    "font": {
                        "size": 22,
                        "color": "white"
                    }
                },

                gauge={

                    "axis": {
                        "range": [0, 100],
                        "tickcolor": "white"
                    },

                    "bar": {
                        "color": "#38BDF8"
                    },

                    "bgcolor": "rgba(0,0,0,0)",

                    "borderwidth": 2,

                    "bordercolor": "#22C55E",

                    "steps": [

                        {
                            "range": [0, 40],
                            "color": "#EF4444"
                        },

                        {
                            "range": [40, 70],
                            "color": "#FACC15"
                        },

                        {
                            "range": [70, 100],
                            "color": "#22C55E"
                        }

                    ]

                }

            )
        )

        fig.update_layout(

            height=320,

            margin=dict(
                l=20,
                r=20,
                t=30,
                b=20
            ),

            paper_bgcolor="rgba(0,0,0,0)",

            font=dict(color="white")

        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        if confidence >= 90:
            st.success("🟢 Excellent Prediction Confidence")
            gauge_color = "#22C55E"  

        elif confidence >= 75:
            st.warning("🟡 Good Prediction Confidence")
            gauge_color = "#FACC15"

        else:
            st.error("🔴 Low Prediction Confidence")
            gauge_color = "#EF4444"

    st.divider()

# =====================================================
# PREDICTION PROBABILITY
# =====================================================

    st.subheader("📊 Disease Prediction Probability")

    df = pd.DataFrame({
    "Disease": class_names,
    "Confidence (%)": prediction[0] * 100
    })

    fig = px.bar(
    df,
    x="Confidence (%)",
    y="Disease",
    orientation="h",
    color="Confidence (%)",
    color_continuous_scale="Viridis",
    text="Confidence (%)"
    )

    fig.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
    )

    fig.update_layout(

        template="plotly_dark",

        paper_bgcolor="#0F172A",
        plot_bgcolor="#1E293B",

        coloraxis_showscale=False,

        font=dict(
         color="white",
         size=16
        ),

        xaxis=dict(
          title="Confidence (%)",
          title_font=dict(color="white", size=18),
          tickfont=dict(color="white")
        ),

        yaxis=dict(
          title="Disease",
          title_font=dict(color="white", size=18),
          tickfont=dict(color="white")
        ),

        margin=dict(l=20, r=20, t=20, b=20),

        height=650
    )

    st.plotly_chart(fig, use_container_width=True)

    st.divider()

# =====================================================
# DISEASE INFORMATION
# =====================================================

    st.header("🌿 Disease Information")

    show_report(info)

    st.divider()

# =====================================================
# CROP RECOMMENDATION
# =====================================================

    st.header("🌾 Crop Recommendation")

    c1, c2, c3 = st.columns(3)

    with c1:
          st.markdown(f"""
          <div class="metric-card">
          <h3>⚠ Severity</h3>
          <h2>{info["Severity"]}</h2>
          </div>
          """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="metric-card">
        <h3>⏳ Recovery Time</h3>
        <h2>{info["Recovery_Time"].replace(" ", "<br>")}</h2>
        </div>
        """, unsafe_allow_html=True)

    with c3:
      st.markdown(f"""
        <div class="metric-card">
        <h3>💰 Estimated Cost</h3>
        <h2>{info["Estimated_Cost"]}</h2>
        </div>
        """, unsafe_allow_html=True)

      st.success(f"🌱 **Fertilizer:** {info['Fertilizer']}")

      st.info(f"🦠 **Pesticide:** {info['Pesticide']}")

      st.warning(f"🥬 **Nutrient Deficiency:** {info['Nutrient_Deficiency']}")

      st.success(f"🏛 **Government Advice:** {info['Government_Advice']}")

      st.divider()

# =====================================================
# PDF REPORT
# =====================================================
    pdf = generate_pdf(
    disease,
    confidence,
    info
    )

    st.write("PDF Path:", pdf)
    st.write("File Exists:", os.path.exists(pdf))
    st.header("📄 Download AgroAI Report")
    
    with open(pdf, "rb") as file:

        st.download_button(
        label="📥 Download PDF Report",
        data=file,
        file_name="AgroAI_Report.pdf",
        mime="application/pdf",
        use_container_width=True
        )

    st.divider()

# =====================================================
# AI RECOMMENDATION
# =====================================================

    st.header("🤖 AI Recommendation")

    recommendation = f"""
    ### 🌿 Disease Detected
    **{disease.replace("_"," ")}**

     ---

    ### 🌱 Recommended Fertilizer
    {info["Fertilizer"]}

    ---

    ### 🦠 Recommended Pesticide
    {info["Pesticide"]}

    ---

    ### 💧 Water Requirement
    {info["Water"]}

    ---

    ### ☀ Weather Condition
    {info["Weather"]}

    ---

    ### 🛡 Prevention Tips
    {info["Prevention"]}

    ---

    ### 🏛 Government Advice
    {info["Government_Advice"]}
    """

    st.markdown(recommendation)

    st.success("✅ Recommendation Generated Successfully")

    st.divider()

# =====================================================
# FOOTER
# =====================================================

    st.markdown("""
    <hr style="margin-top:40px;margin-bottom:20px;">

    <div style="text-align:center;">

    <h3 style="color:#22C55E;">
    🌿 AgroAI Pro
    </h3>

    <p style="font-size:18px;color:#CFCFCF;">
    AI Powered Plant Disease Detection System
    </p>

    <p style="color:#9CA3AF;">
    Made with ❤️ using
    <br>
    TensorFlow • Streamlit • Plotly • Python
    </p>

    <p style="font-size:15px;color:#9CA3AF;">
    © 2026 Ritika Tholia
    </p>

    </div>
    """, unsafe_allow_html=True)

    st.success("🌱 Thank you for using AgroAI Pro!", icon="🌿")
