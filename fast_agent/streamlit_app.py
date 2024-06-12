import streamlit as st

st.image("images/fastagent.png")

st.sidebar.header('Model')
ollama_model = st.sidebar.radio(label="Select Model", options=["Ollama 🆓", "GPT-4o 💷"])

# Define the available tools
tools = ["SerperSearchTool", "FileTool", "DirectoryTool", "ScrapeWebsiteTool", "PDFSearchTool", "TXTSearchTool","CSVSearchTool","DOCXSearchTool", "YoutubeVideoSearchTool", "YoutubeChannelSearchTool"]

# Title of the app
st.title("Multi-Select Tool with Arguments")

# Multi-select tool in the sidebar
selected_tools = st.sidebar.multiselect("Select the tools you want to configure:", tools)

# Dictionary to hold the arguments for each selected tool
tool_arguments = {}

# Loop through the selected tools and create a text_input for each in the sidebar
for tool in selected_tools:
    if tool != 'SerperSearchTool':
        argument = st.sidebar.text_input(f"Enter arguments for {tool}:")
        tool_arguments[tool] = argument

# Display the tool arguments
st.write("Tool Arguments:", tool_arguments)

