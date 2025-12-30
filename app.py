import streamlit as st
import google.generativeai as genai
import os

# 1. Page Config
st.set_page_config(page_title="AutoRx Scribe", page_icon="🩺")

# 2. Sidebar for API Key (Security)
with st.sidebar:
    st.title("⚙️ Configuration")
    api_key = st.text_input("Enter Google Gemini API Key", type="password")
    st.info("Get your key from: aistudio.google.com")

# 3. Main App UI
st.title("🩺 AutoRx Scribe")
st.write("Upload the doctor-patient conversation audio to generate a prescription.")

# 4. Audio Uploader
audio_file = st.file_uploader("Upload Audio (mp3, wav)", type=['mp3', 'wav'])

if audio_file and api_key:
    genai.configure(api_key=api_key)
    
    st.audio(audio_file, format='audio/mp3')
    
    if st.button("📝 Generate Prescription"):
        with st.spinner("Listening and writing prescription..."):
            try:
                # Upload file to Gemini
                model = genai.GenerativeModel("gemini-flash-latest")
                
                # The Golden Prompt Logic (In Code)
                prompt = """
                You are a medical scribe. Listen to this audio conversation between a doctor and patient.
                Extract the following details and format them clearly:
                1. Patient Symptoms
                2. Diagnosis
                3. Medicines (Name, Dosage, Frequency)
                4. Special Advice
                
                Format the output as a clean Medical Prescription.
                """
                
                # Process audio directly
                response = model.generate_content([prompt, 
                    {"mime_type": "audio/mp3", "data": audio_file.getvalue()}
                ])
                
                st.success("Prescription Generated!")
                st.markdown("### 📄 Patient Prescription")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

elif not api_key:
    st.warning("Please enter your API Key in the sidebar to start.")