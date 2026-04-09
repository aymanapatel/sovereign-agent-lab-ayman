"""
Exercise 2 — Answers
====================
Fill this in after running exercise2_langgraph.py.
Run `python grade.py ex2` to check for obvious issues.
"""

# ── Task A ─────────────────────────────────────────────────────────────────

# List of tool names called during Task A, in order of first appearance.
# Note: the model returned all five calls as a single JSON text string rather
# than using the structured function-calling interface — the tools were
# described but not executed. Names are inferred from the model's text response.
# Root cause and fix documented in Insights.md.

TASK_A_TOOLS_CALLED = [
    "check_pub_availability",
    "check_pub_availability",
    "calculate_catering_cost",
    "get_edinburgh_weather",
    "generate_event_flyer",
]

# Which venue did the agent confirm? Must be one of:
# "The Albanach", "The Haymarket Vaults", or "none"
TASK_A_CONFIRMED_VENUE = "The Albanach"

# Total catering cost the agent calculated. Float, e.g. 5600.0
# Write 0.0 if the agent didn't calculate it.
TASK_A_CATERING_COST_GBP = 5600.0

# Did the weather tool return outdoor_ok = True or False?
TASK_A_OUTDOOR_OK = False

TASK_A_NOTES = (
    "The Llama-3.3-70B model batched all five tool calls into one JSON text "
    "block instead of using the structured function-calling interface. No tools "
    "actually executed — the model described what it would call rather than "
    "calling it. Tool names and confirmed venue (The Albanach, with the flyer "
    "prompt in the response) are inferred directly from the model's text output. "
    "Fixed in research_agent.py by adding a system prompt that instructs the "
    "model to call tools one at a time through the proper function-calling "
    "interface. outdoor_ok=False is based on the weather result observed in "
    "Task C Scenario 1 which ran concurrently."
)

# ── Task B ─────────────────────────────────────────────────────────────────

# Has generate_event_flyer been implemented (not just the stub)?
TASK_B_IMPLEMENTED = True

# The image URL returned (or the error message if still a stub).
TASK_B_IMAGE_URL_OR_ERROR = "https://pictures-storage.storage.eu-north1.nebius.cloud/text2img-f3eb885c-bb20-4b36-8b92-8de33a4972ed_00001_.webp"

# The prompt sent to the image model. Copy from terminal output.
TASK_B_PROMPT_USED = "Professional event flyer for Edinburgh AI Meetup, tech professionals, modern venue at The Haymarket Vaults, Edinburgh. 160 guests tonight. Warm lighting, Scottish architecture background, clean modern typography."

# ── Task C ─────────────────────────────────────────────────────────────────

# Scenario 1: first choice unavailable
# Quote the specific message where the agent changed course. Min 20 words.
SCENARIO_1_PIVOT_MOMENT = """
After receiving the Bow Bar tool result — capacity 80, status full,
meets_all_constraints false — the agent immediately issued a second
check_pub_availability call for The Haymarket Vaults without any user
instruction to do so. The pivot was automatic and happened on the very
next tool call, triggered solely by meets_all_constraints: false in the
JSON response.
"""

SCENARIO_1_FALLBACK_VENUE = "The Albanach"

# Scenario 2: impossible constraint (300 guests)
# Did the agent recommend a pub name not in the known venues list?
SCENARIO_2_HALLUCINATED = False

# Paste the final [AI] message.
SCENARIO_2_FINAL_ANSWER = """
None of the known venues meet the capacity and dietary requirements. The Albanach,
The Haymarket Vaults, and The Guilford Arms have a capacity of 180, 160, and 200
respectively, which is less than the required capacity of 300. The Bow Bar has a
capacity of 80, which is also less than the required capacity, and it is currently
full. Therefore, none of the known venues can accommodate 300 people with vegan options.
"""

# Scenario 3: out of scope (train times)
# Did the agent try to call a tool?
SCENARIO_3_TRIED_A_TOOL = False

SCENARIO_3_RESPONSE = "Your input is lacking necessary details. Please provide more information or specify the task you need help with."

# Would this behaviour be acceptable in a real booking assistant? Min 30 words.
SCENARIO_3_ACCEPTABLE = """
No. The response "Your input is lacking necessary details" is misleading — the
user's input was perfectly clear; the agent simply has no tool for train
schedules. A production booking assistant should instead say something like
"I can only help with booking confirmations; for train times please contact
National Rail." The current response would confuse a pub manager calling to
confirm a booking and might make them think they phrased something incorrectly,
rather than understanding this agent is scoped to venue bookings only.
"""

# ── Task D ─────────────────────────────────────────────────────────────────

# Paste the Mermaid output from `python exercise2_langgraph.py task_d` here.
TASK_D_MERMAID_OUTPUT = """
---
config:
  flowchart:
    curve: linear
---
graph TD;
\t__start__([<p>__start__</p>]):::first
\tagent(agent)
\ttools(tools)
\t__end__([<p>__end__</p>]):::last
\t__start__ --> agent;
\tagent -.-> __end__;
\tagent -.-> tools;
\ttools --> agent;
\tclassDef default fill:#f2f0ff,line-height:1.2
\tclassDef first fill-opacity:0
\tclassDef last fill:#bfb6fc
"""

# Compare the LangGraph graph to exercise3_rasa/data/rules.yml. Min 30 words.
TASK_D_COMPARISON = """
The LangGraph Mermaid graph shows just three nodes — start, agent, tools, end —
with a single loop: agent calls tools, tools return to agent, agent either loops
or exits. Every routing decision is made at runtime by the model.

Rasa CALM's flows.yml is the opposite: every task (confirm_booking,
handle_out_of_scope) is written out as an explicit ordered list of steps. The LLM
decides which flow to start but cannot deviate from the declared step sequence.
LangGraph gives the model complete freedom; Rasa CALM gives it one decision
(which flow?) and then hands control to deterministic execution.
"""

# ── Reflection ─────────────────────────────────────────────────────────────

# The most unexpected thing the agent did. Min 40 words.
# Must reference a specific behaviour from your run.

MOST_SURPRISING = """
In Task C Scenario 1, after finding The Haymarket Vaults met all constraints
(capacity 160, vegan true, status available, meets_all_constraints true), the agent
did not stop. It continued checking The Guilford Arms and The Albanach — venues it
was not asked to check — and ultimately chose The Albanach as the confirmed venue
even though The Haymarket Vaults was already adequate. This exhaustive, greedy
search behaviour was unexpected: a human assistant would stop at the first qualifying
venue, but the agent kept exploring as if it were optimising for the best option
rather than simply satisfying the requirement.
"""
