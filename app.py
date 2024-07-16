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
You are the world's top cardiologist and have done more than 1000 ECGs accoss the world. You have to analyze the uploaded {ecg_data} and give these details in a pointwise manner. Don't describe the disease, just focus on describing the following data in a clear and concise manner:

1. Patient Information
- Name:
- Age:
- Gender:
- ID Number:
- Date of ECG:

2. Clinical Information
- Reason for ECG: (e.g., routine check, chest pain, pre-surgical evaluation)
- Relevant Medical History:(e.g., hypertension, diabetes, previous myocardial infarction)
- Medications: ( presently using) 

3. ECG Technical Details
- ECG Machine Used: (Model and Manufacturer)
- Lead Configuration:(e.g., 12-lead ECG)
- Calibration: (e.g., 10 mm/mV, 25 mm/s)
- Recording Quality:(e.g., adequate, artifacts present)

4. ECG Findings
Rhythm and Rate
- Heart Rate: (beats per minute)
- Rhythm: (e.g., sinus rhythm, atrial fibrillation)
- P Waves:(present, morphology)
- PR Interval: (duration in milliseconds)
- QRS Complex: (duration in milliseconds)
- QT/QTc Interval:(duration in milliseconds)
- ST Segment:(elevation, depression, normal)
- T Waves: (inversion, peaked, flattened)

Axis
- P Wave Axis:
- QRS Axis:
- T Wave Axis:

Conduction and Morphology
- Atrial Conduction: (e.g., atrial enlargement)
- Ventricular Conduction:(e.g., bundle branch block)
- QRS Morphology:(e.g., normal, pathological Q waves)
- ST-T Changes: (e.g., ischemic changes, repolarization abnormalities)

5. Interpretation
- Normal or Abnormal:
- Diagnosis/Findings:(e.g., myocardial infarction, left ventricular hypertrophy)
- Comparison with Previous ECG: (if available)

6. Conclusion and Recommendations
- Summary: (Concise interpretation of findings)
- Recommendations:(e.g., further testing, follow-up, treatment changes)

7. Reporting Cardiologist
- Name: Dr. Deepti
- Signature:
- Date of Report:

8. Attachments
- ECG Tracing: (Image of the ECG printout)

Ignore the 7th and 1st any information if it's not visible in the ecg paper. don't show them in your response at all. 
I want the response to be well formed in the manner that's specified. No extra information.

If the image is not of ecg or is blurry (not visible), then simply say that "Please upload a valid image of ECG paper, make sure that it is clear. Try again!".


"""
st.set_page_config(page_title = "ECG Paper Reader")

st.title("Your Digital ECG Reader: ")
st.subheader("It can analyze the ECG paper to know all the details about your heart. ❤️")

ecg_file = st.file_uploader("Upload your ECG image", type=["jpg", "jpeg", "png"])

generate_button = st.button("Get ECG report")
if generate_button:
    ecg_data = ecg_file.getvalue()
    mime_type = ecg_file.type
    image_parts= [
        {
            "mime-type" : mime_type,
            "data" : ecg_data
        },
    ]

    prompt_parts = [
        
        image_parts[0],
        system_prompt
    ]

    response = model.generate_content(prompt_parts)
    print(response.text)
