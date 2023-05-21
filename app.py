import os
import streamlit as st
from streamlit_chat import message
from gpt_index import GPTSimpleVectorIndex, SimpleDirectoryReader


@st.cache_resource
def create_index(file: str) -> GPTSimpleVectorIndex:
    documents = SimpleDirectoryReader(input_files=[f'docs/{file}.txt']).load_data()
    index = GPTSimpleVectorIndex(documents)
    index.save_to_disk('index.json')
    return index


@st.cache_data
def query_index(user_input: str, post: str) -> str:
    return index.query(user_input).response.strip()


def clear_chat():
    st.session_state['generated'] = []
    st.session_state['past'] = []


st.set_page_config(page_title='Vitl GPT demo', page_icon=':robot:')
st.title('Vitl GPT demo')

if 'generated' not in st.session_state or 'past' not in st.session_state:
    clear_chat()

post = st.radio(
    'Select a blog post:',
    [
        'A love letter to DNA',
        'The many factors that affect our mental health',
        'What\'s in our Male Multivitamin and why'
    ],
    on_change=clear_chat
)

index = create_index(post)

user_input = st.text_input('Write a message:', 'Hello, what can I talk to you about?', key='input')

if user_input:
    output = query_index(user_input, post=post)
    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)

if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state['generated'][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
