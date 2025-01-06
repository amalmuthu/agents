import requests
import streamlit as st
import time

# Function to interact with the LLM API
def get_llm_response(prompt, api_url="https://llm.neorains.com/api/generate", model="llama3.1"):
    """Interact with the GPT-based LLM API for generating content."""
    payload = {
        "temperature": 0.9,
        "stream": False,
        "model": model,
        "prompt": prompt,
    }
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(api_url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json().get("response", "No response found in the API output.")
        else:
            return f"API Error {response.status_code}: {response.text}"
    except Exception as e:
        return f"An error occurred: {e}"

# Base Agent Class
class Agent:
    def __init__(self, name):
        self.name = name

    def execute(self, shared_state):
        raise NotImplementedError("Agents must implement the execute method.")

# Preboarding Agent
class PreboardingAgent(Agent):
    def execute(self, shared_state):
        if shared_state["status"] == "Preboarding":
            welcome_email_prompt = f"Generate a professional welcome email for {shared_state['employee']['name']} starting on {shared_state['employee']['start_date']}."
            it_email_prompt = f"Generate a professional IT setup email for {shared_state['employee']['name']}."

            # Get responses from LLM
            welcome_email = get_llm_response(welcome_email_prompt)
            it_email = get_llm_response(it_email_prompt)

            # Store responses in shared state
            shared_state["preboarding"]["welcome_email"] = welcome_email
            shared_state["preboarding"]["it_email"] = it_email

            return "Preboarding emails generated. Please send them to proceed."

# First-Day Agent
class FirstDayAgent(Agent):
    def execute(self, shared_state):
        if shared_state["status"] == "First Day Ready":
            checklist_prompt = (
                f"Generate a checklist for {shared_state['employee']['name']}'s first day, "
                "including team introductions, workspace setup, and tool access verification."
            )

            # Get response from LLM
            checklist = get_llm_response(checklist_prompt)

            # Store the checklist in shared state
            shared_state["first_day"]["checklist"] = checklist

            return "First day checklist generated. Please ensure tasks are completed."

# Training Agent
class TrainingAgent(Agent):
    def execute(self, shared_state):
        if shared_state["status"] == "Training Ready":
            training_plan_prompt = (
                f"Create a training plan for {shared_state['employee']['name']}, "
                f"working as a {shared_state['employee']['role']}. Include orientation, role-specific training, and compliance training."
            )

            # Get response from LLM
            training_plan = get_llm_response(training_plan_prompt)

            # Store the training plan in shared state
            shared_state["training"]["plan"] = training_plan

            return "Training plan created. Please proceed with the training sessions."

# Check-in Agent
class CheckinAgent(Agent):
    def execute(self, shared_state):
        if shared_state["status"] == "Check-in Ready":
            check_in_prompt = (
                f"Create a check-in plan for {shared_state['employee']['name']} "
                "that includes weekly check-ins, monthly performance reviews, and feedback mechanisms."
            )

            # Get response from LLM
            check_in_plan = get_llm_response(check_in_prompt)

            # Store the check-in plan in shared state
            shared_state["check_in"]["reminders"] = check_in_plan

            return "Check-in reminders generated. Please ensure reviews are scheduled."

# Shared State Management
def initialize_shared_state():
    return {
        "status": "Preboarding",
        "employee": {
            "name": "",
            "start_date": "",
            "role": ""
        },
        "preboarding": {"welcome_email_sent": False, "it_email_sent": False},
        "first_day": {},
        "training": {},
        "check_in": {}
    }

# Orchestrator Class
class Orchestrator:
    def __init__(self):
        self.agents = []
        self.shared_state = initialize_shared_state()

    def add_agent(self, agent):
        self.agents.append(agent)

    def run_agent(self, agent_name):
        for agent in self.agents:
            if agent.name == agent_name:
                return agent.execute(self.shared_state)
        return "Agent not found."

# Streamlit Interface
def display_progress(shared_state):
    st.write("### Onboarding Progress")
    for key, value in shared_state.items():
        if isinstance(value, dict):
            st.write(f"**{key.capitalize()}:**")
            for subkey, subvalue in value.items():
                st.write(f"- {subkey}: {subvalue}")
        else:
            st.write(f"**{key.capitalize()}:** {value}")

def display_agent_output(agent_name, shared_state):
    st.write(f"### {agent_name} Output")

    if agent_name == "Preboarding Agent":
        welcome_email = st.text_area("Welcome Email", shared_state["preboarding"].get("welcome_email", ""), height=100)
        if st.button("Send Welcome Email"):
            shared_state["preboarding"]["welcome_email_sent"] = True
            st.success("Welcome email sent successfully.")

        it_email = st.text_area("IT Setup Email", shared_state["preboarding"].get("it_email", ""), height=100)
        if st.button("Send IT Setup Email"):
            shared_state["preboarding"]["it_email_sent"] = True
            st.success("IT setup email sent successfully.")

    elif agent_name == "First Day Agent":
        st.text_area("First Day Checklist", shared_state["first_day"].get("checklist", ""), height=200)
        if st.button("Mark First Day Tasks as Complete"):
            shared_state["status"] = "Training Ready"
            st.success("First day tasks marked as complete.")

    elif agent_name == "Training Agent":
        st.text_area("Training Plan", shared_state["training"].get("plan", ""), height=200)
        if st.button("Mark Training as Complete"):
            shared_state["status"] = "Check-in Ready"
            st.success("Training tasks marked as complete.")

    elif agent_name == "Check-in Agent":
        st.text_area("Check-in Plan", shared_state["check_in"].get("reminders", ""), height=200)
        if st.button("Mark Check-in as Complete"):
            shared_state["status"] = "Complete"
            st.success("Check-in tasks marked as complete.")

def main():
    st.title("Agent Swarm Onboarding System")

    # Sidebar for employee details
    st.sidebar.header("Employee Details")
    name = st.sidebar.text_input("Employee Name")
    start_date = st.sidebar.date_input("Start Date")
    role = st.sidebar.text_input("Role")

    if name and start_date and role:
        # Store employee details in shared state
        orchestrator = Orchestrator()
        orchestrator.shared_state["employee"]["name"] = name
        orchestrator.shared_state["employee"]["start_date"] = str(start_date)
        orchestrator.shared_state["employee"]["role"] = role

        # Add agents to orchestrator
        orchestrator.add_agent(PreboardingAgent("Preboarding Agent"))
        orchestrator.add_agent(FirstDayAgent("First Day Agent"))
        orchestrator.add_agent(TrainingAgent("Training Agent"))
        orchestrator.add_agent(CheckinAgent("Check-in Agent"))

        # Display current progress
        display_progress(orchestrator.shared_state)

        # Select agent to execute
        st.write("### Select an Agent to Run")
        agent_options = [agent.name for agent in orchestrator.agents]
        selected_agent = st.radio("Choose an Agent:", agent_options)

        if st.button("Run Selected Agent"):
            with st.spinner(f"Running {selected_agent}..."):
                result = orchestrator.run_agent(selected_agent)
                time.sleep(2)  # Simulate processing time
                st.success(result)

        # Display agent output
        display_agent_output(selected_agent, orchestrator.shared_state)

    else:
        st.sidebar.warning("Please fill in all the employee details to proceed.")

if __name__ == "__main__":
    main()
