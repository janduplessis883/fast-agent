from crewai import Crew
from trip_agents import TripAgents
from trip_tasks import TripTasks
import streamlit as st
import datetime

st.set_page_config(page_icon="✈️", layout="wide")




class TripCrew:

    def __init__(self, origin, cities, date_range, interests):
        self.cities = cities
        self.origin = origin
        self.interests = interests
        self.date_range = date_range
        self.output_placeholder = st.empty()

    def run(self):
        agents = TripAgents()
        tasks = TripTasks()

        city_selector_agent = agents.city_selection_agent()
        local_expert_agent = agents.local_expert()
        travel_concierge_agent = agents.travel_concierge()

        identify_task = tasks.identify_task(
            city_selector_agent,
            self.origin,
            self.cities,
            self.interests,
            self.date_range
        )

        gather_task = tasks.gather_task(
            local_expert_agent,
            self.origin,
            self.interests,
            self.date_range
        )

        plan_task = tasks.plan_task(
            travel_concierge_agent,
            self.origin,
            self.interests,
            self.date_range
        )

        crew = Crew(
            agents=[
                city_selector_agent, local_expert_agent, travel_concierge_agent
            ],
            tasks=[identify_task, gather_task, plan_task],
            verbose=True
        )

        result = crew.kickoff()
        self.output_placeholder.markdown(result)

        return result


if __name__ == "__main__":
    

    st.image('images/fastagent.png')

    import datetime
    import os
    
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

    # Sidebar section for tool selection and arguments
    st.sidebar.subheader("Tools")
    tools = ["SerperSearchTool", "FileTool", "DirectoryTool", "ScrapeWebsiteTool", "PDFSearchTool", "TXTSearchTool", "CSVSearchTool", "DOCXSearchTool", "YoutubeVideoSearchTool", "YoutubeChannelSearchTool"]
    selected_tools = st.sidebar.multiselect("Select the tools you want to configure:", tools)
    tool_arguments = {}

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

    today = datetime.datetime.now().date()
    next_year = today.year + 1
    jan_16_next_year = datetime.date(next_year, 1, 10)

    with st.sidebar:
        st.header("👇 Enter your trip details")
        with st.form("my_form"):
            location = st.text_input(
                "Where are you currently located?", placeholder="San Mateo, CA")
            cities = st.text_input(
                "City and country are you interested in vacationing at?", placeholder="Bali, Indonesia")
            date_range = st.date_input(
                "Date range you are interested in traveling?",
                min_value=today,
                value=(today, jan_16_next_year + datetime.timedelta(days=6)),
                format="MM/DD/YYYY",
            )
            interests = st.text_area("High level interests and hobbies or extra details about your trip?",
                                     placeholder="2 adults who love swimming, dancing, hiking, and eating")

            submitted = st.form_submit_button("Submit")

        st.divider()

        # Credits to joaomdmoura/CrewAI for the code: https://github.com/joaomdmoura/crewAI
        st.sidebar.markdown(
            """
        Credits to [**@joaomdmoura**](https://twitter.com/joaomdmoura) 
        for creating **crewAI** 🚀
        """,
            unsafe_allow_html=True
        )

        st.sidebar.info("Click the logo to visit GitHub repo", icon="👇")
        st.sidebar.markdown(
            """
        <a href="https://github.com/joaomdmoura/crewAI" target="_blank">
            <img src="https://raw.githubusercontent.com/joaomdmoura/crewAI/main/docs/crewai_logo.png" alt="CrewAI Logo" style="width:100px;"/>
        </a>
        """,
            unsafe_allow_html=True
        )


if submitted:
    with st.status("🤖 **Agents at work...**", state="running", expanded=True) as status:
        with st.container(height=500, border=False):
            trip_crew = TripCrew(location, cities, date_range, interests)
            result = trip_crew.run()
        status.update(label="✅ Trip Plan Ready!",
                      state="complete", expanded=False)

    st.subheader("Here is your Trip Plan", anchor=False, divider="rainbow")
    st.markdown(result)
