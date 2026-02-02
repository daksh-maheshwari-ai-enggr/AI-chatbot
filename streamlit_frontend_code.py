import streamlit as st
from langgraph_backend_code import backend
from langchain_core.messages import HumanMessage
import uuid

def gen_thread_id():
    thread_id=uuid.uuid4()
    return thread_id

def new_thread_id():
    new_id=gen_thread_id()
    st.session_state['thread_id']=new_id
    chat_threads(st.session_state['thread_id'])
    st.session_state['msg_history']=[]

def chat_threads(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

def load_conversation(thread_id):
    return backend.get_state(config={"configurable":{'thread_id':thread_id}}).values['messages']


if 'msg_history' not in st.session_state:
    st.session_state['msg_history']=[]

if 'thread_id' not in st.session_state:
    st.session_state['thread_id']=gen_thread_id()  

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads']=[]

chat_threads(st.session_state['thread_id'])    


st.sidebar.title("Todo-Bot")

if st.sidebar.button("New Chat"):
    new_thread_id()

st.sidebar.header("My Chat")

st.title("Todo Bot")      

for thread_id in st.session_state['chat_threads']:
    st.sidebar.button(str(thread_id))    

  

for message in st.session_state['msg_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])


prompt=st.chat_input("Type here")

if prompt:

    st.session_state['msg_history'].append({'role':'user','content':prompt})

    with st.chat_message("user"):
        st.text(prompt)

    config1={"configurable":{'thread_id':st.session_state['thread_id']}}  
    result=backend.invoke({'msgs':[HumanMessage(content=prompt)]},config=config1)
    new_result=result['msgs'][-1].content

    st.session_state['msg_history'].append({'role':'assistant','content':new_result})    
    with st.chat_message("assistant"):
        st.text(new_result)


