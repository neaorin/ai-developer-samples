# Exercitiu 03: Streamlit 
# Modificați această aplicație Streamlit pentru a apela implementarea chat-ului dvs. folosind Azure OpenAI SDK sau REST API și pentru a răspunde corect la întrebarea utilizatorului.
# Rulati aceasta aplicatie folosind comanda: streamlit run 03-exercise-streamlit.py
# Apoi poate fi acesata la adresa: http://localhost:8501

import streamlit as st
st.set_page_config(page_title="🦜🔗 Demo Streamlit App")
st.title('🦜🔗 Demo Streamlit App')

def generate_response(input_text):
  response = "Habar n-am! 🤷‍♂️"
  st.info(response)

with st.form('my_form'):
  text = st.text_area('Întrebare:', 'Care este capitala României?')
  submitted = st.form_submit_button('Trimite')
  if submitted:
    generate_response(text)
