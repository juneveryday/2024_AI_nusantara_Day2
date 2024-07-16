import streamlit as st
from openai import OpenAI

api_key = st.secrets['OPENAI_SECRET']
client = OpenAI(api_key = api_key)

def create_story(prompt):
  completion = client.chat.completions.create(
    model = 'gpt-3.5-turbo',
    messages = [{"role": "system","content": "You are the best seller story writer. You will take users prompt and generate a 1000 characters short story for adults age 20~30."},
                {"role": "user","content": f'{prompt}'}],
    max_tokens = 190,
    temperature = 0.8
)

  story = completion.choices[0].message.content
  return story

def refine_story(story):
  completion = client.chat.completions.create(
    model = 'gpt-3.5-turbo',
    messages = [{"role": "system","content": """ Based on the story given, you will design image prompt for the cover of this story. The image prompt should include the theme of the story with relevant color, suitable for 20~30 ppl."""},
                {"role": "user","content": f'{story}'}],
    max_tokens = 60,
    temperature = 0.8
)

  image_prompt = completion.choices[0].message.content
  return image_prompt

def create_image(story):

  cover_response = client.images.generate(
      model = 'dall-e-2',
      prompt = f"{story}",
      size = '256x256',
      n = 1,
      quality = 'standard'
  )
  
  image_url = cover_response.data[0].url
  return image_url
  

prompt = 'Write a story about a computer science student, struggling in monash who eventually became the richest guy in the world. Make sure the wtory has funny elements.'

st.set_page_config(page_title="Story and Image Generator", page_icon=":sparkles:", layout="centered")

st.title("✨ Story and Image Generator ✨")
st.markdown("Welcome! Enter some key words to generate a unique short story and a corresponding image.")

with st.form(key="my_form"):
    st.subheader("User Input")
    st.write("This is for you to input information for story generation:")
    msg = st.text_input(label='Enter some keywords to generate a story')
    submitted = st.form_submit_button(label='Submit')

    if submitted:
        if msg:
            with st.spinner("Generating your story..."):
                story = create_story(msg)
                refined_story = refine_story(story)

            st.subheader("Generated Story")
            st.write(refined_story)

            with st.spinner("Generating an image for your story..."):
                image_url = create_image(refined_story)
                st.image(image_url, caption='Generated Image', use_column_width=True)
        else:
            st.write("Please enter some keywords to generate a story.")

st.markdown("---")
st.markdown("Created with ❤️ using OpenAI and Streamlit")

# Styling with CSS
st.markdown("""
    <style>
        .main {
            padding: 20px;
            border-radius: 10px;
        }
        .stButton button {
            background-color: #4CAF50;
            color: white;
            border-radius: 5px;
            padding: 10px;
        }
        .stTextInput input {
            padding: 10px;
            border-radius: 5px;
        }
    </style>
    """, unsafe_allow_html=True)