import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


# ==================================================
# SHOW REPORT IN STREAMLIT
# ==================================================

def show_report(info):

    tab1, tab2, tab3, tab4 = st.tabs([
        "📋 Overview",
        "💊 Treatment",
        "🌱 Farming Advice",
        "📊 Advanced"
    ])

    # ==========================
    # TAB 1
    # ==========================
    with tab1:

        st.subheader("📖 Scientific Description")
        st.info(info["Description"])

        st.subheader("🔍 Symptoms")
        st.warning(info["Symptoms"])

    # ==========================
    # TAB 2
    # ==========================
    with tab2:

        st.subheader("💊 Treatment")
        st.success(info["Treatment"])

        st.subheader("🛡 Prevention")
        st.info(info["Prevention"])

        st.subheader("🌾 Fertilizer")
        st.success(info["Fertilizer"])

        st.subheader("🧪 Pesticide")
        st.success(info["Pesticide"])

    # ==========================
    # TAB 3
    # ==========================
    with tab3:

        st.subheader("🌦 Weather")
        st.info(info["Weather"])

        st.subheader("💧 Water")
        st.info(info["Water"])

        st.subheader("🌱 Soil")
        st.success(info["Soil"])

        st.subheader("☀ Sunlight")
        st.success(info["Sunlight"])

    # ==========================
    # TAB 4
    # ==========================
    with tab4:

        severity = info["Severity"]

        st.subheader("⚠ Disease Severity")

        if severity.lower() == "high":
            st.error(severity)

        elif severity.lower() == "medium":
            st.warning(severity)

        else:
            st.success(severity)

        st.subheader("⏳ Recovery Time")
        st.info(info["Recovery_Time"])

        st.subheader("💰 Estimated Cost")
        st.warning(info["Estimated_Cost"])

        st.subheader("🥬 Nutrient Deficiency")
        st.info(info["Nutrient_Deficiency"])

        st.subheader("🌿 Organic Control")
        st.success(info["Organic_Control"])

        st.subheader("🏛 Government Advice")
        st.info(info["Government_Advice"])


# ==================================================
# GENERATE PDF
# ==================================================

def generate_pdf(disease, confidence, info):

    filename = "AgroAI_Report.pdf"

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph(
            "<b>AgroAI Plant Disease Report</b>",
            styles["Title"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Disease:</b> {disease}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Confidence:</b> {confidence:.2f}%",
            styles["Normal"]
        )
    )

    story.append(Paragraph("<br/>", styles["Normal"]))

    for key, value in info.items():

        story.append(

            Paragraph(

                f"<b>{key.replace('_',' ')}</b> : {value}",

                styles["Normal"]

            )

        )

    doc.build(story)

    return filename