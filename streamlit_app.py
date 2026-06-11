import streamlit as st
from datetime import datetime
import base64

# ---------------- PAGE ----------------
st.set_page_config(page_title="INR Calculator", layout="centered")

st.title("🧪 INR Calculator")
st.markdown("Enter patient details to generate report.")

# ---------------- INPUT ----------------
patient_id = st.text_input("Patient ID (Minimum 6 digits)")
patient_value = st.number_input("Patient Value", min_value=0.0, step=0.1)
control_value = st.number_input("Control Value", min_value=0.0, step=0.1)

ISI = 1.2

# ---------------- VALIDATION ----------------
valid_id = patient_id.isdigit() and len(patient_id) >= 6

if patient_id and not valid_id:
    st.error("Patient ID must be at least 6 digits and numeric.")

# ---------------- PRINT HTML PAGE ----------------
def open_print_page(pid, patient, control, ratio, index, inr):
    now = datetime.now().strftime("%d-%m-%Y %H:%M")

    html = f"""
    <html>
    <head>
        <title>INR Laboratory Report</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 40px;
                color: #000;
            }}
            .container {{
                max-width: 700px;
                margin: auto;
                border: 1px solid #000;
                padding: 20px;
            }}
            h1 {{
                text-align: center;
                font-size: 26px;
                margin-bottom: 20px;
            }}
            .row {{
                font-size: 18px;
                margin: 10px 0;
            }}
            .footer {{
                margin-top: 30px;
                text-align: center;
                font-size: 14px;
            }}
            @media print {{
                button {{
                    display: none;
                }}
            }}
            button {{
                margin-top: 20px;
                padding: 10px;
                width: 100%;
                font-size: 16px;
                cursor: pointer;
            }}
        </style>
    </head>

    <body>

    <div class="container">

        <h1>INR Laboratory Report</h1>

        <div class="row"><b>Date:</b> {now}</div>
        <div class="row"><b>Patient ID:</b> {pid}</div>
        <div class="row"><b>Patient Value:</b> {patient}</div>
        <div class="row"><b>Control Value:</b> {control}</div>
        <div class="row"><b>Ratio:</b> {ratio:.2f}</div>
        <div class="row"><b>Index:</b> {index:.2f}</div>
        <div class="row"><b>INR:</b> {inr:.2f}</div>

        <button onclick="window.print()">🖨️ Print / Save as PDF</button>

        <div class="footer">
            Developed by Bipropod Das Shubro
        </div>

    </div>

    </body>
    </html>
    """

    b64 = base64.b64encode(html.encode()).decode()

    url = f"data:text/html;base64,{b64}"

    st.markdown(
        f'<a href="{url}" target="_blank">📄 Open Print Report</a>',
        unsafe_allow_html=True
    )

# ---------------- CALCULATION ----------------
if valid_id and patient_value > 0 and control_value > 0:

    ratio = patient_value / control_value
    index = (control_value * 100) / patient_value
    inr = ratio ** ISI

    st.markdown("### 📊 Results")

    col1, col2, col3 = st.columns(3)
    col1.metric("Ratio", f"{ratio:.2f}")
    col2.metric("Index", f"{index:.2f}")
    col3.metric("INR", f"{inr:.2f}")

    # PRINT PAGE BUTTON
    open_print_page(patient_id, patient_value, control_value, ratio, index, inr)

elif patient_value == 0 or control_value == 0:
    st.info("Enter values to calculate.")

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown("Developed by **Bipropod Das Shubro**")
