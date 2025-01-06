the difference between AWARM and SWARM agents:
AWARM (Asynchronous Working Agents):

Agents work independently
Each agent has its own task
Don't necessarily coordinate with others
More autonomous behavior
Example: Different robots in a factory doing separate tasks

CopyAWARM Pattern:
Agent 1 --> Task A
Agent 2 --> Task B  (Independent tasks)
Agent 3 --> Task C
SWARM:

Agents work collectively
Share common goal
Coordinate with each other
Like bees in a hive
Example: Multiple drones flying in formation

CopySWARM Pattern:
Agent 1 ↘
Agent 2 → Common Goal (Working together)
Agent 3 ↗
Main Differences:

Coordination:

AWARM: Little to no coordination
SWARM: High coordination


Goals:

AWARM: Individual goals
SWARM: Shared goals


Communication:

AWARM: Minimal communication
SWARM: Constant communication


Task Distribution:

AWARM: Fixed individual tasks
SWARM: Dynamic task sharing

SWARM.py 
LLM Integration: Uses a custom LLaMA model API to generate content
Agent System: Multiple specialized agents handling different onboarding phases
Streamlit UI: Web interface for the onboarding process


Main Agents:

PreboardingAgent: Generates welcome and IT setup emails
FirstDayAgent: Creates first-day checklists
TrainingAgent: Develops training plans
CheckinAgent: Manages check-in schedules and feedback


Orchestration:

Orchestrator class manages all agents
Shared state system tracks onboarding progress
Sequential workflow from preboarding to check-ins


User Interface Features:

Employee details input (name, start date, role)
Progress tracking dashboard
Agent selection and execution
Display of generated content
Interactive buttons for task completion


Process Flow:
CopyEmployee Details Entry
↓
Preboarding (Welcome + IT Emails)
↓
First Day Checklist
↓
Training Plan
↓
Check-in Schedule

AWARM.py 
This code implements awarm concept implementing HR onboarding system.
