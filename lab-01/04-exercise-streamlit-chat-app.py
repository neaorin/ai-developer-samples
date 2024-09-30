# Exercitiu 04: Streamlit - aplicație de chat
# Modificați această aplicație Streamlit într-o aplicație de chat care apelează implementarea chat-ului dvs. folosind Azure OpenAI SDK sau REST API și răspunde corect la întrebările utilizatorului.

# Documentatie: https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps

# Rulati aceasta aplicatie folosind comanda: streamlit run 04-exercise-streamlit-chat-app.py
# Apoi poate fi acesata la adresa: http://localhost:8501

import streamlit as st
st.set_page_config(page_title="🦜🔗 Demo Streamlit Chat App")
st.title('🦜🔗 Demo Streamlit Chat App')

def generate_response(input_text):
  response = "Habar n-am! 🤷‍♂️"
  st.info(response)

with st.form('my_form'):
  text = st.text_area('Întrebare:', 'Care este capitala României?')
  submitted = st.form_submit_button('Trimite')
  if submitted:
    generate_response(text)
