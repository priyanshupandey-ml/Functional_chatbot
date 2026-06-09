from langgraph.graph import StateGraph,START,END
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage,HumanMessage
from typing import Annotated,TypedDict
from langchain_huggingface import ChatHuggingFace,HuggingFaceEndpoint
from dotenv import load_dotenv
from langgraph.checkpoint.sqlite import SqliteSaver
import os
import sqlite3

#to add peristence so that bot remmebrs the cnversation history
load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-3.1-8B-Instruct",
    task="text-generation",
    # huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN")
)
Chat_model= ChatHuggingFace(llm=llm)

class ChatState(TypedDict):
    message: Annotated[list[BaseMessage], add_messages]
    
def chat_node(state:ChatState)->ChatState:
    #Here you can add your logic to process the messages and generate a response
    messages=state["message"]
    
    
    response=Chat_model.invoke(messages)
    
    return {"message":response}


conn=sqlite3.connect(database="chatbot_data.db" , check_same_thread=False)
checkpointer=SqliteSaver(conn=conn)
cur=conn.cursor()
cur.execute("DELETE FROM checkpoints")
conn.commit()

def save_title(thread_id, title):
    conn = sqlite3.connect("chatbot_data.db")
    cur = conn.cursor()

    cur.execute("""
        INSERT OR REPLACE INTO conversations
        (thread_id, title)
        VALUES (?, ?)
    """, (thread_id, title))

    conn.commit()
    conn.close()

def get_title(thread_id):
    conn = sqlite3.connect("chatbot_data.db")
    cur = conn.cursor()

    cur.execute(
        "SELECT title FROM conversations WHERE thread_id=?",
        (thread_id,)
    )

    row = cur.fetchone()

    conn.close()

    if row:
        return row[0]
    
    return "New Chat"

graph=StateGraph(ChatState)
    

graph.add_node("chat_node",chat_node)

#Defne nodes of graph 

#Define edges of graph
graph.add_edge(START,"chat_node")
graph.add_edge("chat_node",END)

config={"configurable":{"thread_id":1}}
workflow=graph.compile(checkpointer=checkpointer)

def retrive_threads():
    get_all_threads=set()
    for thread in checkpointer.list(None):
        get_all_threads.add(thread.config['configurable']['thread_id'])
        print(thread)
    return list(get_all_threads)

