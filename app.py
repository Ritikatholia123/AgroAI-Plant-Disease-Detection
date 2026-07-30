import pandas as pd
import streamlit as st
from tensorflow.keras.models import load_model
from PIL import Image
from disease_data import disease_info, class_names
from utils import predict_disease
from report import show_report, generate_pdf

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="🌿 AgroAI",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# LOAD CSS
# ==========================================

try:
    with open("style.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )
except:
    pass

# ==========================================
# LOAD MODEL
# ==========================================

MODEL_PATH = "model/plant_disease_model.keras"

try:
    model = load_model(MODEL_PATH)

except Exception as e:

    st.error(f"Model Loading Error\n\n{e}")

    st.stop()

# ==========================================
# HEADER
# ==========================================

st.title("🌿 AgroAI")

st.markdown("""
## 🤖 AI Powered Plant Disease Detection

Upload a leaf image and AgroAI will detect the disease automatically.

### Features

✅ Disease Detection

✅ Treatment

✅ Prevention

✅ Fertilizer Recommendation

✅ Pesticide Recommendation

✅ Weather Advice

✅ Organic Control

✅ Government Advice

✅ PDF Report
""")

st.divider()

# ==========================================
# IMAGE UPLOAD
# ==========================================

uploaded_file = st.file_uploader(
    "📷 Upload Plant Leaf Image",
    type=["jpg", "jpeg", "png"]
)
# ==========================================
# PREDICTION
# ==========================================

if uploaded_file is not None:

    image = Image.open(uploaded_file).convert("RGB")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.image(
            image,
            caption="Uploaded Leaf",
            use_container_width=True
        )

    # Predict Disease
    disease, confidence, prediction = predict_disease(
        model,
        image,
        class_names
    )
    st.subheader("📊 Prediction Probability")

    df = pd.DataFrame({
    "Disease": class_names,
    "Confidence": prediction[0] * 100
    })

    st.bar_chart(
    df.set_index("Disease")
)

    # Get Disease Information
    info = disease_info[disease]

    with col2:

        st.success("Prediction Completed Successfully")

        st.header(f"🌿 {disease}")

        st.metric(
            "Confidence",
            f"{confidence:.2f}%"
        )

        st.progress(confidence / 100)

    st.divider()

    # Show Disease Report
    show_report(info)

    # Generate PDF
    pdf = generate_pdf(
        disease,
        confidence,
        info
    )

    with open(pdf, "rb") as file:

        st.download_button(
            label="📄 Download PDF Report",
            data=file,
            file_name="AgroAI_Report.pdf",
            mime="application/pdf"
        )

