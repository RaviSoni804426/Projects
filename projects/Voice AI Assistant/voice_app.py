import streamlit as st
import speech_recognition as sr
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
from gtts import gTTS
import os
import tempfile

# Set page config
st.set_page_config(page_title="Voice AI Assistant", page_icon="🎙️")

st.title("🎙️ Voice AI Assistant")
st.markdown("Interact with a lightweight AI using your voice or text.")

# Load Model
@st.cache_resource
def load_brain():
    model_name = "google/flan-t5-small"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    return tokenizer, model

tokenizer, model = load_brain()

def think(user_input):
    prompt = f"Answer clearly and concisely:\n{user_input}"
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(**inputs, max_new_tokens=100, do_sample=False)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

def speak(text):
    tts = gTTS(text=text, lang="en")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)
        return fp.name

# Mode Selection
mode = st.radio("Choose Input Method:", ["Text", "Voice"])

user_text = ""
if mode == "Text":
    user_text = st.text_input("Type your message here:")
else:
    if st.button("Start Listening"):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            st.info("🎤 Listening...")
            try:
                audio = recognizer.listen(source, timeout=5)
                user_text = recognizer.recognize_google(audio)
                st.success(f"You said: {user_text}")
            except Exception as e:
                st.error("Could not understand audio or microphone error.")

if user_text:
    with st.spinner("AI is thinking..."):
        response = think(user_text)
        st.subheader("AI Response:")
        st.write(response)
        
        audio_path = speak(response)
        st.audio(audio_path)
        # Clean up temp file
        # os.remove(audio_path) # Streamlit might need it to serve
