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

st.sidebar.subheader('Year of Experiences')
experienced = st.sidebar.selectbox('Filter by Year Of Experienced', ('1', '2',"3",'4',"5","6","Above All"))

API_URL = "http://13.214.164.179:3000/api/v1/prediction/5f411a49-8fa2-4302-afda-1380dc3ae72f"
# Plotting the bar chart

# Function to send query to your API
def query_message(payload):
    response = requests.post(API_URL, json=payload)
    return response.json()


st.title("ResumeQueryGenius")
prompt=""


if level == "All Level":
    levelPrompt = ""
else:
    levelPrompt=f"at {level} position"
    

if skills == []:
    skillsPrompt = ""
else:
    skillsPrompt=f"{skills} skills"

if st.sidebar.button("Search"):
    prompt=f"Provide all resumes matching {skillsPrompt} {levelPrompt}. Generate detailed information for each resume(Please specify a name of that resume).For skills, list them on a single row beside the skills title.Specify the total years of experience based on the work experience history provided in the resume"
    st.write(prompt)


def render_bar_chart(text):
    skills_pattern = r"Skills:\s*(.+?)\n\n"
    # Extract skills using regular expression
    skills_match = re.findall(skills_pattern, text)
    # Process the matched skills
    skills_list = []
    for skills_block in skills_match:
        skills_list.extend(re.findall(r"(\w+)", skills_block))
    # Create the object with extracted skills
    skills_object = {"skills": skills_list}
    # Display the object containing skills
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
    output = query_message({'question': prompt})
    text = output.get("text", "")
    render_bar_chart(text)

    st.write(text)  






