import streamlit as st 
from langgraph_sqlite_db import retrive_threads,workflow,save_title,get_title,Chat_model
from langchain_core.messages import HumanMessage,AIMessage

import uuid

# Generate a unique thread ID for each conversation
def generate_thread_id():
    thread_id = uuid.uuid4()  # Generate a unique thread ID using UUID
    return str(thread_id)

def reset_conversation():
    thread_id = generate_thread_id()  # Generate a new thread ID for the new conversation
    
    session_state["thread_id"] = thread_id  # Generate a new thread ID for the new conversation
    add_thread(thread_id)  # Add the new thread ID to the list of chat threads
    session_state["message_history"] = []  # Clear the conversation history

def add_thread(thread_id):
    if thread_id not in session_state["chat_threads"]:
        session_state["chat_threads"].append(thread_id)  # Add the new thread ID to the list of chat threads
        
def load_conversation(thread_id):
    state = workflow.get_state(config={'configurable': {'thread_id': thread_id}})

    # Check if messages key exists in state values, return empty list if not
    return state.values.get('message', [])


# **************************** Session Setup ****************************

session_state = st.session_state #to store the conversation history it is type of dictionary
if "message_history" not in session_state:
    session_state["message_history"] = [] #initialize the message history as an empty list
    
if "thread_id" not in session_state:
    session_state["thread_id"] = generate_thread_id()
               # Generate a unique thread ID for the conversation # Print the thread ID to the console for debugging

if "chat_threads" not in session_state:
    session_state["chat_threads"] = retrive_threads() # Initialize a dictionary to store chat threads
      # Add the initial thread ID to the list of chat threads

add_thread(session_state["thread_id"])   

    
# **************************** Sidebar Setup ****************************

st.sidebar.title("My Chatbot")

if st.sidebar.button("New Conversation"):
    reset_conversation()  # Reset the conversation when the button is clicked

st.sidebar.header("My Conversations")

for thread in session_state["chat_threads"][::-1]:
    title = get_title(thread)
    
    if st.sidebar.button(title):
        session_state['thread_id'] = thread
        messages = load_conversation(thread)
        

        temp_messages = []

        for msg in messages:
            if isinstance(msg, HumanMessage):
                role='user'
            else:
                role='assistant'
            temp_messages.append({'role': role, 'content': msg.content , "avatar": "user.png" if role=="user" else "customer.png"}) # Add avatar to messages based on role

        st.session_state['message_history'] = temp_messages

for message in session_state['message_history']:
    with st.chat_message(message['role'],avatar=message.get("avatar")): #add avatar if exists in message dictionary
        st.text(message['content'])


user_input= st.chat_input("Type your message here")


if user_input:
    if len(session_state["message_history"]) == 0:
        title = Chat_model.invoke( f"Generate a conversation title in 4 words,make sure title do not any kind of punctuation marks like double quotes and such marks:\n{user_input}").content # Generate a title based on the first user message

        save_title(
            session_state["thread_id"],
            title
        )
        
    session_state["message_history"].append({"role": "user", "content": user_input, "avatar": "user.png"}) # Add avatar to user message
    with st.chat_message("user", avatar="user.png"):
        st.markdown(user_input)
   
    
    # response=workflow.invoke({"message":[HumanMessage(content=user_input)]},config={"configurable":{"thread_id":2}})
    
    # assistant_reply=response["message"][-1].content
    
    
    with st.chat_message("assistant", avatar="customer.png"):
        ai_message=st.write_stream(
        message_chunk.content for message_chunk,metadeta in workflow.stream(
            {"message":[HumanMessage(content=user_input)]},
            config={"configurable":{"thread_id": session_state["thread_id"]}},
            stream_mode="messages"
        )
        )
    session_state["message_history"].append({"role": "assistant", "content": ai_message, "avatar": "customer.png"}) # Add avatar to assistant message
    
    # Add user message to conversation history
    
    

    
    