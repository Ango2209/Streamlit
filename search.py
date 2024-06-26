import streamlit as st
import requests
import altair as alt
import pandas as pd
import numpy as np
import re
st.sidebar.image("https://th.bing.com/th/id/R.937852738cb3f37450550bb2c9fc5be1?rik=G9fCXu4%2fIgJE9g&riu=http%3a%2f%2fww1.prweb.com%2fprfiles%2f2016%2f11%2f13%2f14044818%2fHitachi-inspire-the-next-vector-logo.png&ehk=uucVd6nl7xwv%2f1DqYtu88%2bwv3K1wTfLyW23HayAHXOc%3d&risl=&pid=ImgRaw&r=0", width=150)

st.sidebar.subheader('Skills')

skills= st.sidebar.multiselect(
    "Filter by Programming Languages",
    ["Java", "JavaScript", "AWS","HTML/CSS","Python","Data Analysis","Project Management","CRM","Customer Service","AI","Angular.js","React.js","UNIX","Database","Django","Communication","Microsoft Project"]
)

st.sidebar.subheader('Level')
level = st.sidebar.selectbox('Filter by Level', ("All Level",'Entry',"Fresher", "Senior",'Project Manager',"Junior","Business Analyst","Full Stack","AI","Director"))

API_URL = "http://13.214.164.179:3000/api/v1/prediction/5f411a49-8fa2-4302-afda-1380dc3ae72f"
# Plotting the bar chart

# Function to send query to your API
def query_message(payload):
    response = requests.post(API_URL, json=payload)
    return response.json()


st.title("ResumeQueryGenius")
prompt=""


levelPrompt = f"{level} position" if level != "All Level" else ""
skillsPrompt = ", ".join(skills) + "" if skills else ""

if st.sidebar.button("Search"):
    prompt = (
    "Please provide resumes matching the following criteria:\n")
    if skillsPrompt and levelPrompt:
        prompt += f"- Desired Skills: {skillsPrompt} at {levelPrompt}.\n"
    elif skillsPrompt:
        prompt += f"- Desired Skills: {skillsPrompt}.\n"
    elif levelPrompt:
        prompt += f"- Desired Level: {levelPrompt}.\n"
    else:
        prompt += "- No specific skills or level specified.\n"
    prompt += (
    "For each candidate, ensure they possess the required skills or position.\n"
    "If a candidate does not meet the criteria, please exclude them from consideration."
    "For each candidate:\n"
    "- Specify the candidate's name, personal contact details, work experience, and skills.\n"
    "- Include their work experience, specifying the total years based on provided history (assuming the current year is 2024).\n"
    "Generate a candidate profile in the following format:\n\n"
    " Candidate: [Candidate's Name] \n"
    "- Contact: [Candidate's Email], [Candidate's Phone Number], [Candidate's Location]\n"
    "- Work Experience:\n"
        " Please list all work experiences in the following format for each:\n"
        " - [Company Name], [Job Title], [Location] | [Years of Experience] years\n"
        "[Additional Work Experience if applicable]\n"
    "- Total Year of Experience: [Total Years of Experience] years\n" 
    "- Skills: [Please provide a comprehensive list of all skills possessed by the candidate, separated by commas.]\n"
    "- Example:\n"
    "- Name: Coleman Guthrie\n"
    "- Contact: cole.guthrie@email.com, (123) 456-7890, San Francisco, CA\n"
    "- Work Experience: Genovice, IT Project Manager, San Francisco, CA | 5 years\n"
    "- Federal Reserve Bank of Boston, IT Project Manager, San Francisco, CA | 5 years\n"
    "- Skills: Server Maintenance, SQL, APIs, CRM, Microsoft 365, Programming Languages: C++, Java, Python, Project Management, Data Analysis\n"
    )




def render_bar_chart(text):
    skills_pattern = r"Skills:\s*(.+?)(?:Candidate|$)"
    skills_match = re.findall(skills_pattern, text, re.DOTALL)
    skills_list = []

    for skills_block in skills_match:
       skills_list.extend(re.findall(r"(\w+(?:\s+\w+)*)", skills_block))
    skills_object = {"skills": skills_list}

    print(skills_object)

    df = pd.DataFrame(skills_object)
    if skills_object['skills']:
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

if prompt:
    with st.spinner("## Loading..."):
        output = query_message({'question': prompt})
        text = output.get("text", "")
        if text:
            render_bar_chart(text)
            st.write(text)
        else:
            st.write("No results found.")
else:
   st.write("## Query something..")


