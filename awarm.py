import streamlit as st
import requests

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

# Employee Class
class Employee:
    def __init__(self, name, email, department, role):
        self.name = name
        self.email = email
        self.department = department
        self.role = role

# Main App Class
class OnboardingApp:
    def __init__(self):
        if "employees" not in st.session_state:
            st.session_state.employees = []

    def add_employee(self, name, email, department, role):
        new_employee = Employee(name, email, department, role)
        st.session_state.employees.append(new_employee)

    def get_employee(self, name):
        return next((emp for emp in st.session_state.employees if emp.name == name), None)

# Agent Functions
def run_preboarding_agent(department, role):
    """Preboarding Agent: Generate Welcome and IT Setup Emails."""
    # Welcome Email
    welcome_prompt = f"""Write a professional welcome email for a new hire.
    Department: {department}
    Role: {role}"""
    welcome_email = get_llm_response(welcome_prompt)

    # IT Setup Email
    it_setup_prompt = f"""Write an IT setup email for a new hire.
    Department: {department}
    Role: {role}"""
    it_email = get_llm_response(it_setup_prompt)

    return {"welcome_email": welcome_email, "it_setup_email": it_email}

def run_first_day_agent(department, role):
    """First Day Agent: Generate a First Day Checklist."""
    first_day_prompt = f"""Write a first day checklist for a new hire.
    Department: {department}
    Role: {role}"""
    return get_llm_response(first_day_prompt)

def run_training_agent(department, role):
    """Training Agent: Generate a Training Plan."""
    training_prompt = f"""Write a training plan for a new hire.
    Department: {department}
    Role: {role}"""
    return get_llm_response(training_prompt)

def run_checkin_agent(department, role):
    """Check-in Agent: Generate a Check-in Plan."""
    checkin_prompt = f"""Write a check-in plan for a new hire.
    Department: {department}
    Role: {role}"""
    return get_llm_response(checkin_prompt)

# Streamlit App Interface
def main():
    st.title("Onboarding System with AWARM Agents")
    app = OnboardingApp()

    # Sidebar: Add Employee
    st.sidebar.header("Add Employee")
    name = st.sidebar.text_input("Name")
    email = st.sidebar.text_input("Email")
    department = st.sidebar.selectbox("Department", ["Engineering", "HR", "Marketing", "Sales"])
    role = st.sidebar.text_input("Role")

    if st.sidebar.button("Add Employee"):
        if name and email and department and role:
            app.add_employee(name, email, department, role)
            st.sidebar.success("Employee added successfully!")

    # Main: Display Agents
    if st.session_state.employees:
        selected_employee = st.selectbox("Select Employee", [emp.name for emp in st.session_state.employees])
        employee = app.get_employee(selected_employee)

        if employee:
            st.header(f"Agents for {employee.name}")

            # Agent Buttons
            agent = st.radio("Select Agent", ["Preboarding Agent", "First Day Agent", "Training Agent", "Check-in Agent"])

            if agent == "Preboarding Agent":
                if st.button("Generate Welcome Email"):
                    emails = run_preboarding_agent(employee.department, employee.role)
                    welcome_email = st.text_area("Welcome Email", value=emails["welcome_email"])
                    if st.button("Send Welcome Email"):
                        st.success("Welcome email sent successfully!")

                if st.button("Generate IT Setup Email"):
                    emails = run_preboarding_agent(employee.department, employee.role)
                    it_email = st.text_area("IT Setup Email", value=emails["it_setup_email"])
                    if st.button("Send IT Setup Email"):
                        st.success("IT setup email sent to IT support successfully!")

            elif agent == "First Day Agent":
                if st.button("Generate First Day Checklist"):
                    checklist = run_first_day_agent(employee.department, employee.role)
                    st.text_area("First Day Checklist", value=checklist)
                    if st.button("Mark Checklist Sent"):
                        st.success("First day checklist sent successfully!")

            elif agent == "Training Agent":
                if st.button("Generate Training Plan"):
                    plan = run_training_agent(employee.department, employee.role)
                    st.text_area("Training Plan", value=plan)
                    if st.button("Mark Training Plan Sent"):
                        st.success("Training plan sent successfully!")

            elif agent == "Check-in Agent":
                if st.button("Generate Check-in Plan"):
                    plan = run_checkin_agent(employee.department, employee.role)
                    st.text_area("Check-in Plan", value=plan)
                    if st.button("Mark Check-in Plan Sent"):
                        st.success("Check-in plan sent successfully!")

if __name__ == "__main__":
    main()
