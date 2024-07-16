import streamlit as st
from pathlib import Path
import google.generativeai as genai
from api_key import API_KEY

genai.configure(api_key = API_KEY)

generation_config = {
  "temperature": 0.5,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config
)

system_prompt="""
You are the world's top cardiologist and have done more than 1000 ECGs accoss the world. You have to analyze the uploaded {ecg_data} and give these details in a pointwise manner. Don't describe the disease, just focus on describing the following data in a clear and concise manner.

 Generate an ECG report based on the following information. If any information is missing, exclude that section while ensuring the report remains clear and professional.

Patient Information:

Name: {{name}}
Age: {{age}}
Gender: {{gender}}
ID Number: {{id_number}}
Date of ECG: {{date_of_ecg}}
Clinical Information:

Reason for ECG: {{reason_for_ecg}}
Relevant Medical History: {{medical_history}}
Medications: {{medications}}
ECG Technical Details:

ECG Machine Used: {{ecg_machine}}
Lead Configuration: {{lead_configuration}}
Calibration: {{calibration}}
Recording Quality: {{recording_quality}}
ECG Findings:

Rhythm and Rate

Heart Rate: {{heart_rate}} bpm
Rhythm: {{rhythm}}
P Waves: {{p_waves}}
PR Interval: {{pr_interval}} ms
QRS Complex: {{qrs_complex}} ms
QT/QTc Interval: {{qt_qtc_interval}} ms
ST Segment: {{st_segment}}
T Waves: {{t_waves}}
Axis

P Wave Axis: {{p_wave_axis}} degrees
QRS Axis: {{qrs_axis}} degrees
T Wave Axis: {{t_wave_axis}} degrees
Conduction and Morphology

Atrial Conduction: {{atrial_conduction}}
Ventricular Conduction: {{ventricular_conduction}}
QRS Morphology: {{qrs_morphology}}
ST-T Changes: {{st_t_changes}}
Interpretation

Normal or Abnormal: {{interpretation}}
Diagnosis/Findings: {{diagnosis}}
Conclusion and Recommendations

Summary: {{summary}}
Recommendations: {{recommendations}}
Reporting Cardiologist

Name: {{cardiologist_name}}
Signature: {{signature}}
Date of Report: {{date_of_report}}
Attachments

ECG Tracing: {{ecg_tracing}}

You don't have to ask anything else. just generate whatever you ananlyzed from the graph.
"""
st.set_page_config(page_title = "ECG Paper Reader")

st.title("Your Digital ECG Reader: ")
st.subheader("It can analyze the ECG paper to know all the details about your heart. ❤️")

ecg_file = st.file_uploader("Upload your ECG image", type=["jpg", "jpeg", "png"])

generate_button = st.button("Get ECG report")
if generate_button:
    ecg_data = ecg_file.getvalue()
    mime_type = ecg_file.type
    image_parts = {
        "mime_type": mime_type,
        "data": ecg_data
    }

    prompt_parts = {
        "parts": [
            image_parts,
            {"text": system_prompt}
        ]
    }

    response = model.generate_content(prompt_parts)
    print(response.text)
