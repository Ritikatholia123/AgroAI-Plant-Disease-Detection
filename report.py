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

        st.markdown(f"""
        <div class="info-card">
        <h4>📖 Scientific Description</h4>
        <p>{info["Description"]}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="info-card">
        <h4>🔍 Symptoms</h4>
        <p>{info["Symptoms"]}</p>
        </div>
        """, unsafe_allow_html=True)

    # ==========================
    # TAB 2
    # ==========================
    with tab2:

       st.markdown(f"""
       <div class="info-card">
       <h4>💊 Treatment</h4>
       <p>{info["Treatment"]}</p>
       </div>
       """, unsafe_allow_html=True)

       st.markdown(f"""
       <div class="info-card">
       <h4>🛡 Prevention</h4>
       <p>{info["Prevention"]}</p>
       </div>
       """, unsafe_allow_html=True)

       st.markdown(f"""
       <div class="info-card">
       <h4>🌾 Fertilizer</h4>
       <p>{info["Fertilizer"]}</p>
       </div>
       """, unsafe_allow_html=True)

       st.markdown(f"""
       <div class="info-card">
       <h4>🧪 Pesticide</h4>
       <p>{info["Pesticide"]}</p>
       </div>
       """, unsafe_allow_html=True)

    # ==========================
    # TAB 3
    # ==========================
    with tab3:

        st.markdown(f"""
        <div class="info-card">
        <h4>🌦 Weather</h4>
        <p>{info["Weather"]}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="info-card">
        <h4>💧 Water</h4>
        <p>{info["Water"]}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="info-card">
        <h4>🌱 Soil</h4>
        <p>{info["Soil"]}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="info-card">
        <h4>☀ Sunlight</h4>
        <p>{info["Sunlight"]}</p>
        </div>
        """, unsafe_allow_html=True)
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

        st.markdown(f"""
        <div class="info-card">
        <h4>⏳ Recovery Time</h4>
        <p>{info["Recovery_Time"]}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="info-card">
        <h4>💰 Estimated Cost</h4>
        <p>{info["Estimated_Cost"]}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="info-card">
        <h4>🥬 Nutrient Deficiency</h4>
        <p>{info["Nutrient_Deficiency"]}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="info-card">
        <h4>🌿 Organic Control</h4>
        <p>{info["Organic_Control"]}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="info-card">
        <h4>🏛 Government Advice</h4>
        <p>{info["Government_Advice"]}</p>
        </div>
        """, unsafe_allow_html=True)


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