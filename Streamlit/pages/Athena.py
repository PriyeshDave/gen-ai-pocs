import streamlit as st
from PIL import Image
import os
from langchain import PromptTemplate, LLMChain
# set the streamlit page theme as light
st.set_page_config(layout="wide", page_title="Athena", page_icon="../Colleague-OnBoarding/assets/images/favicon.png", initial_sidebar_state="expanded")

# Removing the watermark at the bottom
st.markdown('<style> #MainMenu {visibility: hidden;} footer {visibility: hidden;}</style>', unsafe_allow_html=True)

with open("./UI/Use Case Descriptions/athena.txt") as f:
    athena_text = f.read()
    athena_text = athena_text.strip()
    f.close()
# Import required libraries
from dotenv import load_dotenv
from itertools import zip_longest

import streamlit as st
from streamlit_chat import message
from langchain.chains import RetrievalQA
from langchain.chains import RetrievalQA
import pinecone
import os
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings

from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)

# Load environment variables
load_dotenv()
os.environ['PINECONE_API_KEY'] =''
os.environ['PINECONE_INDEX_NAME'] ='slackpine'
os.environ['PINECONE_ENV'] ='gcp-starter'
os.environ['OPENAI_API_KEY']=''
os.environ['CTRANSFORMERS_MODEL'] =''
os.environ['LANGCHAIN_TRACING_V2']='true'
os.environ['LANGCHAIN_ENDPOINT']='https://api.smith.langchain.com'
os.environ['LANGCHAIN_API_KEY']=''
os.environ['LANGCHAIN_PROJECT']='slackllm'


# Set streamlit page configuration
#st.set_page_config(page_title="ChatBot Starter")
#st.title("SlackBot Starter")
with open("./UI/Use Case Descriptions/data_copilot.txt") as f:
    data_athena_intro_text = f.read()
    data_athena_intro_text = data_athena_intro_text.strip()
    f.close()
st.markdown("<h1 style='text-align: center; color: black;'> Tacit  Knowledge SlackBot </h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: black;'> Your Untapped asset knowledge management QA Bot </h2>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: black;'>{data_athena_intro_text}</p>", unsafe_allow_html=True)

# Initialize session state variables
if 'generated' not in st.session_state:
    st.session_state['generated'] = []  # Store AI generated responses

if 'past' not in st.session_state:
    st.session_state['past'] = []  # Store past user inputs

if 'entered_prompt' not in st.session_state:
    st.session_state['entered_prompt'] = ""  # Store the latest user input

# Initialize the ChatOpenAI model
chat = ChatOpenAI(
    temperature=0.5,
    model_name="gpt-3.5-turbo"
)

model_name = 'text-embedding-ada-002'

embed = OpenAIEmbeddings(
            model=model_name,
            openai_api_key=os.environ['OPENAI_API_KEY']
        )  
index_name = 'slackpine'
pinecone.init(
    api_key=os.getenv("PINECONE_API_KEY"),  # find at app.pinecone.io
    environment=os.getenv("PINECONE_ENV"),  # next to api key in console
)
text_field = "text"

# switch back to normal index for langchain
index = pinecone.Index(index_name)

vectorstore = Pinecone(
    index, embed.embed_query, text_field
)
qa_chain = RetrievalQA.from_chain_type(
    chat,
    retriever=vectorstore.as_retriever(),
    chain_type="stuff",
    return_source_documents=True,
)
    
template = """Question: {question}
Answer: Let's think step by step."""

prompt = PromptTemplate(
    template=template,
    input_variables= ["question"]
)




def build_message_list():
    """
    Build a list of messages including system, human and AI messages.
    """
    # Start zipped_messages with the SystemMessage
    zipped_messages = [SystemMessage(
        content="You are a helpful AI assistant talking with a human. If you do not know an answer, just say 'I don't know', do not make up an answer.")]

    # Zip together the past and generated messages
    for human_msg, ai_msg in zip_longest(st.session_state['past'], st.session_state['generated']):
        if human_msg is not None:
            zipped_messages.append(HumanMessage(
                content=human_msg))  # Add user messages
        if ai_msg is not None:
            zipped_messages.append(
                AIMessage(content=ai_msg))  # Add AI messages

    return zipped_messages


def generate_response():
    """
    Generate AI response using the ChatOpenAI model.
    """
    # Build the list of messages
    zipped_messages = build_message_list()
    
    # Generate response using the chat model
    # ai_response = qa_chain.run(st.session_state.entered_prompt)#chat(zipped_messages)
    llm_chain_local = LLMChain(prompt=prompt, llm=chat)
    ai_response=llm_chain_local(st.session_state.entered_prompt)
    print(ai_response)
    return ai_response['text']


# Define function to submit user input
def submit():
    # Set entered_prompt to the current value of prompt_input
    st.session_state.entered_prompt = st.session_state.prompt_input
    # Clear prompt_input
    st.session_state.prompt_input = ""

# Create a text input for user
st.text_input('Slack Channel: ', key='prompt_input', on_change=submit)

if st.session_state.entered_prompt != "":
    
    # Get user query
    user_query = st.session_state.entered_prompt

    # Append user query to past queries
    st.session_state.past.append(user_query)
    
    # Generate response
    output = generate_response()

    # Append AI response to generated responses
    st.session_state.generated.append(output)

# Display the chat history
if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        # Display AI response
        message(st.session_state["generated"][i], key=str(i))
        # Display user message
        message(st.session_state['past'][i],
                is_user=True, key=str(i) + '_user')


# Add credit




st.markdown(f"<p style='text-align: center; color: black;'>{athena_text}</p>", unsafe_allow_html=True)
#st.balloons()