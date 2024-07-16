# Imports
import streamlit as st
from openai import OpenAI
import time

def generate_story(prompt, client):
  design_response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": """Based on the story given, you will design a detailed image prompt for the cover image of this story. The image prompt should include the theme of the story with relevent color suitable for adults.
      The output should be within 100 chracters. """},
      {"role": "user", "content": f'{prompt}'}],
      max_tokens = 400,
      temperature = 1.3
  )

  design_prompt = design_response.choices[0].message.content
  return design_prompt

def image_generator(design_response):
  cover_response = client.images.generate(
    model='dall-e-2',
    prompt = f"{design_response}",
    size="256x256",
    quality = 'standard',
    n = 1
  )

  image_url = cover_response.data[0].url
  return image_url
  
# Statics
api_key = st.secrets['OPENSI_API_KEY']
client = OpenAI(api_key=api_key)

st.title("OpenSI Story Generator")

with st.form("Form"):
  st.write("This is for user to key in information.")
  msg = st.text_input(label="Some keyword to generate story", key="keyword")

  submitted = st.form_submit_button('Submit')

  if not submitted:
    with st.spinner('Wait for it...'):
      while msg == "":
          time.sleep(0.5)
  
  if submitted:
  
    # generate story
    story_ai = generate_story(msg, client)
    st.write(story_ai)

    # generate url
    story_url = image_generator(story_ai)
    st.write(story_url)
    
    # st.image(requests.get(story_url).content)
    if story_url is not None:
      st.image(story_url)
  
    st.success('Done!')
    

