import streamlit as st
import os

st.image("images/fastagent.png")
# - Manage API keys - load from TOML file and decalre as enviromental variables ----------------------------------------
# Title of the app
st.sidebar.title("CrewAI Agents Front End")
st.sidebar.subheader("The Model")
# Radio button to select the model
selected_model = st.sidebar.radio(
    "Select the model to run the crew:",
    ("💷 OpenAI-GPT-4o", "🆓 Ollama-llama3-q8", "🆓 GROQ-llama70b", "💷 Anthropic-Claude")
)

# Function to set environment variables
def set_environment_variables(api_key, api_base, model_name):
    os.environ["OPENAI_API_KEY"] = api_key
    os.environ["OPENAI_API_BASE"] = api_base
    os.environ["OPENAI_MODEL_NAME"] = model_name
    os.environ["MODEL"] = model_name

# Load and set environment variables based on selected model
try:
    if selected_model == "💷 OpenAI-GPT-4o":
        api_key = st.secrets["model_secrets"]["OPENAI_API_KEY"]
        api_base = st.secrets["model_secrets"]["OPENAI_API_BASE"]
        model_name = st.secrets["model_secrets"]["OPENAI_MODEL_NAME"]
        set_environment_variables(api_key, api_base, model_name)
        st.sidebar.warning("Default Model: 💷 OpenAI-GPT-4o")

    elif selected_model == "🆓 Ollama-llama3-q8":
        api_key = st.secrets["model_secrets"]["OLLAMA_API_KEY"]
        api_base = st.secrets["model_secrets"]["OLLAMA_API_BASE"]
        model_name = st.secrets["model_secrets"]["OLLAMA_MODEL_NAME"]
        set_environment_variables(api_key, api_base, model_name)
        st.sidebar.success("Model: 🆓 Ollama-llama3-q8")

    elif selected_model == "🆓 GROQ-llama70b":
        st.sidebar.success("Model: 🆓 GROQ-llama70b")

    elif selected_model == "💷 Anthropic-Claude":
        st.sidebar.warning("Model: 💷 Anthropic-Claude")

    else:
        st.sidebar.warning("No model selected.")

except KeyError as e:
    st.sidebar.error(f"Missing secret: {e}")


st.toast(f"OPENAI_API_KEY: {os.getenv('OPENAI_API_KEY')}")
st.toast(f"OPENAI_API_BASE: {os.getenv('OPENAI_API_BASE')}")
st.toast(f"OPENAI_MODEL_NAME: {os.getenv('OPENAI_MODEL_NAME')}")
st.toast(f"MODEL: {os.getenv('MODEL')}")




st.sidebar.subheader("Tools")
# Define the available tools
tools = ["SerperSearchTool", "FileTool", "DirectoryTool", "ScrapeWebsiteTool", "PDFSearchTool", "TXTSearchTool","CSVSearchTool","DOCXSearchTool", "YoutubeVideoSearchTool", "YoutubeChannelSearchTool"]

# Multi-select tool in the sidebar
selected_tools = st.sidebar.multiselect("Select the tools you want to configure:", tools)

# Dictionary to hold the arguments for each selected tool
tool_arguments = {}

# Loop through the selected tools and create a text_input for each in the sidebar
for tool in selected_tools:
    if tool != 'SerperSearchTool':
        argument = st.sidebar.text_input(f"Enter arguments for **{tool}**:")
        tool_arguments[tool] = argument


with st.expander("Tool Arguments:"):
    st.write(tool_arguments)

with st.expander("AGENTS:"):
    st.write("Researcher_Agent")
    
with st.expander("TASKS:"):
    st.write("Research_Task")
    
    
    
    
    