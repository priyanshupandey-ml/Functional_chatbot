# 🤖 Advanced ChatGPT-Like Chatbot using LangGraph

## 📌 Project Overview

This project is an advanced AI chatbot built using **LangGraph**, **LangChain**, **Streamlit**, and **SQLite**. The goal of this project was to understand how production-level conversational AI systems such as ChatGPT manage conversations, persist chat history, resume old sessions, and maintain user-specific threads.

Through this project, I learned the complete workflow of designing and implementing graph-based AI applications using LangGraph.

---

# 🚀 Features

* ChatGPT-like user interface using Streamlit
* Conversation persistence using SQLite
* Resume previous chats anytime
* Thread-based conversation management
* Dynamic chat title generation
* Session state management in Streamlit
* Graph-based workflow using LangGraph
* Node and State architecture
* Database connection management
* Message history storage and retrieval
* Scalable architecture for future AI agents

---

# 📚 Concepts Learned

## 1. LangGraph Fundamentals

LangGraph allows building AI applications as graphs.

### Components Learned:

### State

A State acts as shared memory between nodes.

```python
class State(TypedDict):
    messages: Annotated[list, add_messages]
```

The state stores conversation history and passes data between nodes.

---

### Nodes

Nodes are individual functions that perform tasks.

Example:

```python
def chatbot_node(state):
    response = llm.invoke(state["messages"])
    return {"messages": [response]}
```

Each node receives the current state and returns updates to the state.

---

### Edges

Edges define how execution flows between nodes.

```python
graph.add_edge(START, "chatbot")
graph.add_edge("chatbot", END)
```

---

### Graph Compilation

After creating nodes and edges, the graph is compiled.

```python
workflow = graph.compile(
    checkpointer=checkpointer
)
```

Compilation converts the graph into an executable workflow.

---

# 2. Persistence in LangGraph

One of the most important concepts learned was Persistence.

Persistence allows conversations to survive application restarts.

Without persistence:

* Chat history disappears after refresh.
* Old conversations cannot be resumed.

With persistence:

* Chats are automatically saved.
* Users can continue previous conversations.
* Message history remains available.

---

# 3. Checkpointers

A Checkpointer stores graph state after every execution.

Example:

```python
workflow = graph.compile(
    checkpointer=checkpointer
)
```

The checkpointer acts like memory storage for the graph.

---

# 4. Thread Management

Threads are unique identifiers representing individual conversations.

Example:

```python
thread_id = str(uuid.uuid4())
```

Each thread maintains its own conversation history.

Benefits:

* Multiple conversations per user.
* Easy chat retrieval.
* ChatGPT-like experience.

---

# 5. Resuming Old Chats

Learned how to retrieve previously saved threads from the database and continue the conversation.

Workflow:

1. Select an existing thread.
2. Load stored messages.
3. Restore chat history.
4. Continue chatting from the last message.

This replicates ChatGPT's conversation restoration feature.

---

# 6. SQLite Database Integration

SQLite was used for storing:

* Thread IDs
* Chat titles
* Messages
* Metadata

---

### Database Operations Learned

#### Create Tables

```sql
CREATE TABLE chats (
    id INTEGER PRIMARY KEY,
    thread_id TEXT,
    title TEXT
);
```

#### Insert Data

```sql
INSERT INTO chats VALUES (...);
```

#### Read Data

```sql
SELECT * FROM chats;
```

#### Delete Data

```sql
DELETE FROM chats;
```

---

# 7. Database Connection Management

A major lesson learned was proper database connection handling.

### Common Issue

```python
sqlite3.ProgrammingError:
Cannot operate on a closed database
```

### Solution

Maintain a single active connection and close it only when required.

Example:

```python
conn = sqlite3.connect("chatbot.db")
cur = conn.cursor()
```

Proper connection management prevents application crashes.

---

# 8. Streamlit Session State

Session State allows storing variables across reruns.

Example:

```python
if "messages" not in st.session_state:
    st.session_state.messages = []
```

Uses:

* Store conversation history
* Track selected thread
* Maintain UI state
* Preserve user interactions

---

# 9. Building ChatGPT-like Interface

Implemented:

### Chat Messages

```python
with st.chat_message("user"):
    st.write(prompt)
```

```python
with st.chat_message("assistant"):
    st.write(response)
```

---

### Chat Input

```python
prompt = st.chat_input("Ask Anything")
```

---

### Sidebar Navigation

Used Streamlit sidebar for:

* Viewing previous conversations
* Selecting threads
* Starting new chats

---

# 10. Dynamic Chat Titles

Implemented automatic chat title generation based on the first user message.

Example:

```python
"How to Learn LangGraph?"
```

becomes

```text
How to Learn LangGraph?
```

inside the sidebar.

Benefits:

* Easier navigation.
* Better conversation organization.

---

# 11. Message History Management

Learned how to:

* Save messages
* Retrieve messages
* Display previous chats
* Synchronize UI with database

This creates a seamless conversational experience.

---

# 12. LangChain Integration

Used LangChain to:

* Handle LLM communication
* Structure messages
* Manage Human and AI messages

Example:

```python
HumanMessage(content="Hello")
AIMessage(content="Hi!")
```

---

# 13. Project Architecture

```text
User
 │
 ▼
Streamlit UI
 │
 ▼
Session State
 │
 ▼
LangGraph Workflow
 │
 ▼
State
 │
 ▼
Nodes
 │
 ▼
LLM
 │
 ▼
Checkpoint Saver
 │
 ▼
SQLite Database
```

---

# 🎯 Key Outcomes

Through this project, I learned:

✅ LangGraph Fundamentals

✅ States

✅ Nodes

✅ Edges

✅ Graph Compilation

✅ Persistence

✅ Checkpointers

✅ Thread Management

✅ SQLite Integration

✅ Database Connection Handling

✅ Streamlit Session State

✅ Chat History Management

✅ Dynamic Chat Titles

✅ ChatGPT-like UI Design

✅ Conversation Restoration

✅ LangChain Message Handling

---

# 🛠 Tech Stack

* Python
* LangGraph
* LangChain
* Streamlit
* SQLite
* Hugging Face Models
* SQL

---

# 📈 Future Enhancements

* PostgreSQL Integration
* User Authentication
* Multi-user Support
* Vector Database (ChromaDB/Qdrant)
* RAG Implementation
* Agentic AI Workflows
* Voice Assistant Integration
* File Upload and Analysis
* Long-Term Memory

---

# 👨‍💻 Author

**Priyanshu Pandey**

B.Tech CSE Student | BS Data Science (IIT Madras)

Passionate about AI, Machine Learning, Data Engineering, Cybersecurity, and Building Intelligent Systems.
