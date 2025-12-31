import streamlit as st
import google.generativeai as genai
import os

# 1. Page Config
st.set_page_config(page_title="AutoRx Scribe", page_icon="🩺")

# ---------------------------------------------------------
# ✅ CHANGE HERE: API Key Setup (From Secrets)
# జడ్జెస్ కీ ఎంటర్ చేయక్కర్లేదు, ఆటోమేటిక్ గా తీసుకుంటుంది.
# ---------------------------------------------------------
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except FileNotFoundError:
    st.error("API Key not found! Please set it in Streamlit Secrets.")
    st.stop()
# ---------------------------------------------------------

# 3. Main App UI
st.title("🩺 AutoRx Scribe")
st.write("Upload the doctor-patient conversation audio to generate a prescription.")

# 4. Audio Uploader
audio_file = st.file_uploader("Upload Audio (mp3, wav)", type=['mp3', 'wav'])

# ఇక్కడ 'and api_key' అవసరం లేదు, ఎందుకంటే పైన ఆల్రెడీ సెట్ చేశాం.
if audio_file:
    
    st.audio(audio_file, format='audio/mp3')
    
    if st.button("📝 Generate Prescription"):
        with st.spinner("Listening and writing prescription..."):
            try:
                # Upload file to Gemini
                model = genai.GenerativeModel("gemini-1.5-flash") # Model update chesanu (latest stable version)
                
                # The Golden Prompt Logic
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
                # Note: Audio data format for Gemini API requires correct handling
                response = model.generate_content([
                    prompt, 
                    {"mime_type": "audio/mp3", "data": audio_file.getvalue()}
                ])
                
                st.success("Prescription Generated!")
                st.markdown("### 📄 Patient Prescription")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")