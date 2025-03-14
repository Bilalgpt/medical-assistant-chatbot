import streamlit as st
from pathlib import Path
from langchain.agents import create_sql_agent
from langchain.sql_database import SQLDatabase
from langchain.agents.agent_types import AgentType
from langchain.callbacks import StreamlitCallbackHandler
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from sqlalchemy import create_engine
import sqlite3
import os
from langchain_groq import ChatGroq
import plotly.express as px
import pandas as pd

# Initialize medical database if needed
def initialize_database_if_needed():
    if not os.path.exists("medical.db"):
        st.sidebar.warning("Medical database not found. Initializing with sample data...")
        import medical_database
        medical_database.initialize_medical_database()
        st.sidebar.success("Database initialized!")

# Page configuration
st.set_page_config(
    page_title="MediChat: AI Medical Database Assistant",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar styling and branding
st.sidebar.image("https://img.icons8.com/color/96/000000/health-checkup.png", width=80)
st.sidebar.title("MediChat")
st.sidebar.caption("Your AI Medical Database Assistant")

# Main page styling
st.title("🏥 MediChat: AI Medical Database Assistant")
st.markdown("""
This intelligent assistant can help you query and analyze medical records, 
patient information, prescriptions, and more using natural language.
""")

# Database selection options
LOCALDB = "USE_LOCALDB"
MYSQL = "USE_MYSQL"
radio_opt = ["Use Medical SQLite Database", "Connect to external Medical Database"]
selected_opt = st.sidebar.radio(label="Database Connection", options=radio_opt)

# Database connection configuration
if radio_opt.index(selected_opt) == 1:
    db_uri = MYSQL
    with st.sidebar.expander("MySQL Connection Details"):
        mysql_host = st.text_input("MySQL Host")
        mysql_user = st.text_input("MySQL User")
        mysql_password = st.text_input("MySQL Password", type="password")
        mysql_db = st.text_input("Database Name")
else:
    db_uri = LOCALDB
    initialize_database_if_needed()

# Model selection and API key input
st.sidebar.divider()
st.sidebar.subheader("AI Model Configuration")
model_options = ["Llama3-8b-8192", "Gemma2-9b-It", "Mixtral-8x7b-32768"]
selected_model = st.sidebar.selectbox("Select AI Model", model_options)
api_key = st.sidebar.text_input(label="Groq API Key", type="password")

# Display examples for users to try
st.sidebar.divider()
st.sidebar.subheader("Example Questions")
example_questions = [
    "How many patients have hypertension?",
    "List all medications prescribed for depression",
    "What are the most common diagnoses?",
    "Which doctor has seen the most patients?",
    "Show me all patients with type 2 diabetes"
]
for q in example_questions:
    if st.sidebar.button(q, key=q):
        st.session_state.messages.append({"role": "user", "content": q})
        st.experimental_rerun()

# Check for required inputs
if not db_uri:
    st.info("Please select a database connection option")
if not api_key:
    st.info("Please enter your Groq API key to continue")
    st.stop()

# Initialize LLM
llm = ChatGroq(groq_api_key=api_key, model_name=selected_model, streaming=True)

# Database configuration function
@st.cache_resource(ttl="2h")
def configure_db(db_uri, mysql_host=None, mysql_user=None, mysql_password=None, mysql_db=None):
    if db_uri == LOCALDB:
        dbfilepath = Path("medical.db").absolute()
        creator = lambda: sqlite3.connect(f"file:{dbfilepath}?mode=ro", uri=True)
        return SQLDatabase(create_engine("sqlite:///", creator=creator))
    elif db_uri == MYSQL:
        if not (mysql_host and mysql_user and mysql_password and mysql_db):
            st.error("Please provide all MySQL connection details.")
            st.stop()
        return SQLDatabase(create_engine(f"mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}"))

# Create database connection
if db_uri == MYSQL:
    db = configure_db(db_uri, mysql_host, mysql_user, mysql_password, mysql_db)
else:
    db = configure_db(db_uri)

# Create SQL agent
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
agent = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION
)

# Add options to view database schema
if st.sidebar.checkbox("Show Database Schema"):
    st.sidebar.code(db.get_table_info())

# Display database overview in dashboard
if "messages" not in st.session_state:
    # Create initial dashboard
    st.subheader("Database Overview")
    col1, col2, col3 = st.columns(3)
    
    try:
        # Count statistics
        patient_count = pd.read_sql("SELECT COUNT(*) as count FROM patients", db.engine).iloc[0]['count']
        record_count = pd.read_sql("SELECT COUNT(*) as count FROM medical_records", db.engine).iloc[0]['count']
        prescription_count = pd.read_sql("SELECT COUNT(*) as count FROM prescriptions", db.engine).iloc[0]['count']
        
        col1.metric("Total Patients", patient_count)
        col2.metric("Medical Records", record_count)
        col3.metric("Prescriptions", prescription_count)
        
        # Demographics chart
        with st.expander("Patient Demographics", expanded=True):
            col1, col2 = st.columns(2)
            
            # Gender distribution
            gender_data = pd.read_sql("SELECT gender, COUNT(*) as count FROM patients GROUP BY gender", db.engine)
            fig1 = px.pie(gender_data, values='count', names='gender', title='Gender Distribution')
            col1.plotly_chart(fig1, use_container_width=True)
            
            # Blood type distribution
            blood_data = pd.read_sql("SELECT blood_type, COUNT(*) as count FROM patients GROUP BY blood_type", db.engine)
            fig2 = px.bar(blood_data, x='blood_type', y='count', title='Blood Type Distribution')
            col2.plotly_chart(fig2, use_container_width=True)
        
        # Initialize chat messages
        st.session_state["messages"] = [{"role": "assistant", "content": "Hello! I'm your Medical Database Assistant. How can I help you analyze the medical records today?"}]
    except Exception as e:
        st.error(f"Error loading dashboard: {e}")
        st.session_state["messages"] = [{"role": "assistant", "content": "Hello! I'm your Medical Database Assistant. How can I help you analyze the medical records today?"}]

# Clear chat button
if st.sidebar.button("Clear Chat History"):
    st.session_state["messages"] = [{"role": "assistant", "content": "Chat history cleared. How can I help you analyze the medical records today?"}]
    st.experimental_rerun()

# Display chat history
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# User input
user_query = st.chat_input(placeholder="Ask anything about the medical database (e.g., 'Show me all patients with hypertension')")

# Process user input
if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    st.chat_message("user").write(user_query)
    
    with st.chat_message("assistant"):
        streamlit_callback = StreamlitCallbackHandler(st.container())
        
        try:
            response = agent.run(user_query, callbacks=[streamlit_callback])
            
            # Check if the response contains data that could be visualized
            if "SELECT" in user_query.upper() and ("count" in user_query.lower() or "group by" in user_query.lower()):
                try:
                    # Extract SQL query from agent's thoughts
                    thought_lines = streamlit_callback.thought.split('\n')
                    sql_query = None
                    for line in thought_lines:
                        if "SELECT" in line.upper() and "FROM" in line.upper():
                            sql_query = line.strip()
                            break
                    
                    if sql_query:
                        # Execute the query to get data for visualization
                        result_df = pd.read_sql(sql_query, db.engine)
                        
                        # Determine appropriate visualization
                        if result_df.shape[1] == 2 and result_df.shape[0] < 15:
                            # For 2-column results that look like category-value pairs
                            if result_df.dtypes.iloc[1] in ['int64', 'float64']:
                                cols = result_df.columns
                                fig = px.bar(result_df, x=cols[0], y=cols[1], 
                                             title=f"Visualization of {cols[0]} vs {cols[1]}")
                                st.plotly_chart(fig, use_container_width=True)
                except Exception as viz_error:
                    # Silently fail visualization attempts - they're just enhancements
                    pass
            
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.write(response)
        except Exception as e:
            error_msg = f"Sorry, I encountered an error: {str(e)}"
            st.session_state.messages.append({"role": "assistant", "content": error_msg})
            st.write(error_msg)
