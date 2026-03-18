import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from io import BytesIO
from datetime import datetime

# ---------------- UI STYLE ----------------
st.set_page_config(page_title="INR Calculator", layout="centered")

st.title("🧪 INR Calculator")
st.markdown("Enter patient details to generate a professional report.")

# ---------------- INPUT ----------------
patient_id = st.text_input("Patient ID (Minimum 6 digits)")
patient_value = st.number_input("Patient Value", min_value=0.0, step=0.1)
control_value = st.number_input("Control Value", min_value=0.0, step=0.1)

ISI = 1.2

# ---------------- PDF FUNCTION ----------------
def generate_pdf(pid, patient, control, ratio, index, inr):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer)

    # Custom styles with larger font
    title_style = ParagraphStyle(name='Title', fontSize=22, leading=26, alignment=TA_CENTER)
    normal_style = ParagraphStyle(name='Normal', fontSize=16, leading=22)

    elements = []

    # Title
    elements.append(Paragraph("INR Laboratory Report", title_style))
    elements.append(Spacer(1, 20))

    # Date
    now = datetime.now().strftime("%d-%m-%Y %H:%M")
    elements.append(Paragraph(f"Date: {now}", normal_style))
    elements.append(Spacer(1, 15))

    # Patient Info
    elements.append(Paragraph(f"Patient ID: {pid}", normal_style))
    elements.append(Spacer(1, 15))

    # Results
    elements.append(Paragraph(f"Patient Value: {patient}", normal_style))
    elements.append(Paragraph(f"Control Value: {control}", normal_style))
    elements.append(Paragraph(f"Ratio: {ratio:.3f}", normal_style))
    elements.append(Paragraph(f"Index: {index:.2f}", normal_style))
    elements.append(Paragraph(f"INR: {inr:.3f}", normal_style))

    doc.build(elements)
    buffer.seek(0)
    return buffer

# ---------------- VALIDATION ----------------
valid_id = patient_id.isdigit() and len(patient_id) >= 6

if patient_id and not valid_id:
    st.error("Patient ID must be at least 6 digits and numeric.")

# ---------------- CALCULATION ----------------
if valid_id and patient_value > 0 and control_value > 0:

    ratio = patient_value / control_value
    index = (control_value * 100) / patient_value
    inr = ratio ** ISI

    st.markdown("### 📊 Results")
    col1, col2, col3 = st.columns(3)
    col1.metric("Ratio", f"{ratio:.3f}")
    col2.metric("Index", f"{index:.2f}")
    col3.metric("INR", f"{inr:.3f}")

    # Generate PDF
    pdf = generate_pdf(patient_id, patient_value, control_value, ratio, index, inr)

    st.download_button(
        "📄 Download Report",
        data=pdf,
        file_name=f"INR_Report_{patient_id}.pdf",
        mime="application/pdf",
        type="primary"
    )

    # Print Button
    st.markdown("""
        <br>
        <button onclick="window.print()" style="width:100%;padding:10px;font-size:16px;">
        🖨️ Print Report
        </button>
    """, unsafe_allow_html=True)

elif patient_value == 0 or control_value == 0:
    st.info("Enter values to calculate.")

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown("Developed by **Bipropod Das Shubro**")
