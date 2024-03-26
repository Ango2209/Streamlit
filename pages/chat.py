import streamlit as st
import requests
import altair as alt
import pandas as pd
import numpy as np
import re
API_URL = "http://13.214.164.179:3000/api/v1/prediction/5f411a49-8fa2-4302-afda-1380dc3ae72f"

# Function to send query to your API
def query_message(payload):
    response = requests.post(API_URL, json=payload)
    return response.json()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input3
        
def render_bar_chart(text):
    skills_pattern = r"Skills:\s*(.+?)\n"
    skills_match = re.search(skills_pattern, text, re.DOTALL)
    
    if skills_match:
       skills = skills_match.group(1).split(', ')
    else:
       skills = []
    skills_object = {"skills": skills}
    print(skills_object)
    df = pd.DataFrame(skills_object)

    if skills_object['skills']:
        print("oks")
        language_counts = df['skills'].value_counts().reset_index()
        language_counts.columns = ['Language', 'Frequency']
        st.markdown('Bar chart')
        chart = alt.Chart(language_counts).mark_bar().encode(
        x="Language",
        y='Frequency',
        color=alt.value('pink') 
        ).properties(
        width=600,
        height=400
        )
        st.altair_chart(chart, use_container_width=True)
    
prompt = st.chat_input("What information you want to find?")
if prompt:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
        
    with st.chat_message("assistant"):
        response = query_message({'question': prompt})
        text = response.get("text", "")
        render_bar_chart(text)
        st.markdown(text)
        st.session_state.messages.append({"role": "assistant", "content": text})
        


