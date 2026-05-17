import streamlit as st
from agent import get_travel_agent_executor

st.set_page_config(page_title="AI Travel Planner", page_icon="✈️")

st.title("✈️ Agentic AI-Based Travel Assistant")
st.markdown("Automate custom travel itineraries with localized datasets, real-time weather info, and LangChain agents.")

st.subheader("Plan Your Journey")
user_prompt = st.text_area(
    "Where would you like to go?", 
    "Plan a 3-Day Trip to Goa from Delhi. Find cheap flights, good hotels, and tell me what the weather will be like."
)

if st.button("Generate Optimized Itinerary"):
    if user_prompt:
        with st.spinner("Executing Tool-Calling Agent workflows..."):
            try:
                # Calls the executor safely without OpenAI billing requirements
                agent_executor = get_travel_agent_executor()
                response = agent_executor.invoke({"input": user_prompt})
                
                # Render beautiful, clean text output
                st.info(response['output'])
                
            except Exception as e:
                st.error(f"Execution Error encountered: {str(e)}")