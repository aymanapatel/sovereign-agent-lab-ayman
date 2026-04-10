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
    "All 6 tool calls executed correctly through the function-calling interface. "
    "The agent checked both The Albanach and The Haymarket Vaults (both passed), "
    "calculated catering (£5600), fetched weather (outdoor_ok=False), then attempted "
    "generate_event_flyer twice — once per venue — both returning 404: "
    "'The model black-forest-labs/flux-schnell is not found.' The flux-schnell "
    "model has been removed from the Nebius platform. The confirmed venue in the "
    "final AI message is The Albanach (mentioned first), though the agent refers "
    "to both as 'the confirmed venue', which is contradictory."
)

# ── Task B ─────────────────────────────────────────────────────────────────

# Has generate_event_flyer been implemented (not just the stub)?
TASK_B_IMPLEMENTED = True

# The image URL returned (or the error message if still a stub).
TASK_B_IMAGE_URL_OR_ERROR = "Error code: 404 - {'detail': 'The model `black-forest-labs/flux-schnell` is not found.'}"

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

SCENARIO_1_FALLBACK_VENUE = "The Haymarket Vaults"

# Scenario 2: impossible constraint (300 guests)
# Did the agent recommend a pub name not in the known venues list?
SCENARIO_2_HALLUCINATED = False

# Paste the final [AI] message.
SCENARIO_2_FINAL_ANSWER = """
None of the known venues meet the capacity and dietary requirements. The closest
match is The Albanach, which has a capacity of 180 and offers vegan options, but
it does not meet the required capacity of 300.
"""

# Scenario 3: out of scope (train times)
# Did the agent try to call a tool?
SCENARIO_3_TRIED_A_TOOL = False

SCENARIO_3_RESPONSE = "Your input is lacking necessary details. Please provide more information or specify the task you need help with."

# Would this behaviour be acceptable in a real booking assistant? Min 30 words.
SCENARIO_3_ACCEPTABLE = """
No — and the failure mode is specifically bad. "Your input is lacking necessary
details" doesn't just fail to help; it shifts blame to the caller. The pub
manager's input was perfectly clear — the agent is the one with a scope
limitation, not the user. A production assistant should name its own boundary:
"I can only help with venue booking confirmations; for train times please contact
National Rail." The Rasa CALM agent in Exercise 3 did exactly this — it said "I
can only help with confirming tonight's venue booking" without implying the
question was malformed. Failing gracefully is a design requirement, not a nice-to-have.
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
The LangGraph graph is three nodes: start → agent ↔ tools → end. Every routing
decision happens at runtime, inside the model. You can't read the diagram and
predict the step sequence — you can only watch it unfold.

Rasa CALM's flows.yml is a laminated flowchart. The developer wrote the steps;
the LLM's only job is to pick which flowchart to start. Once confirm_booking
begins, the question order (guests → vegan → deposit → validate) cannot change.
LangGraph gives the model a blank whiteboard; CALM gives it a checklist it cannot
reorder. Neither is better — the choice comes down to whether unpredictability
is a feature or a bug for your specific use case.
"""

# ── Reflection ─────────────────────────────────────────────────────────────

# The most unexpected thing the agent did. Min 40 words.
# Must reference a specific behaviour from your run.

MOST_SURPRISING = """
In Task C Scenario 2 (impossible 300-guest constraint), the agent checked all four
known venues — The Albanach, The Haymarket Vaults, The Guilford Arms, The Bow Bar —
received meets_all_constraints: false from every one, and then called
check_pub_availability on The Albanach a second time with identical parameters.
The Albanach returned the same failure. Only then did it give up.

This shows the agent has no internal record of tools it has already called within
a session. When the model decides it needs another check, it reaches for whatever
venue is most salient in its context — and The Albanach, checked first, floated
back to the top. The fix isn't a smarter model; it's explicit state tracking in
the graph, or a prompt rule: "do not re-call a tool with arguments you have
already used in this session."
"""
