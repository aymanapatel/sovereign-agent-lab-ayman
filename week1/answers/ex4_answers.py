"""
Exercise 4 — Answers
====================
Fill this in after running exercise4_mcp_client.py.
"""

# ── Basic results ──────────────────────────────────────────────────────────

# Tool names as shown in "Discovered N tools" output.
TOOLS_DISCOVERED = ["search_venues", "get_venue_details"]

QUERY_1_VENUE_NAME    = "The Haymarket Vaults"
QUERY_1_VENUE_ADDRESS = "1 Dalry Road, Edinburgh"
QUERY_2_FINAL_ANSWER  = "There are no venues available that can accommodate 300 people and offer vegan options."

# ── The experiment ─────────────────────────────────────────────────────────
# Required: modify venue_server.py, rerun, revert.

EX4_EXPERIMENT_DONE = True

# What changed, and which files did or didn't need updating? Min 30 words.
EX4_EXPERIMENT_RESULT = """
After changing The Albanach's status from 'available' to 'full' in
mcp_venue_server.py and re-running, Query 1 returned only one match
(The Haymarket Vaults) instead of two. The agent's final answer remained
the same venue — The Haymarket Vaults at 1 Dalry Road — because it was
still available and met the constraints. Query 2 was unaffected since no
venue reached 300-person capacity regardless. Only mcp_venue_server.py
needed to change; exercise4_mcp_client.py, the agent, and the LangGraph
loop were untouched. This is the MCP contract in action: data lives in one
place; all clients see the update automatically at the next tool call.
"""

# ── MCP vs hardcoded ───────────────────────────────────────────────────────

LINES_OF_TOOL_CODE_EX2 = 10   # imports + TOOLS list in research_agent.py
LINES_OF_TOOL_CODE_EX4 = 39   # _build_args_schema + _make_mcp_caller + discover_tools

# What does MCP buy you beyond "the tools are in a separate file"? Min 30 words.
MCP_VALUE_PROPOSITION = """
The experiment showed it directly: changing The Albanach's status to "full" in
mcp_venue_server.py immediately changed the agent's search results on the next
run. exercise4_mcp_client.py was untouched. One file changed, one source of
truth, zero client updates.

With hardcoded tools you repeat that change everywhere the tool is referenced —
the LangGraph agent, any Rasa action that needs the same data, any CLI tool
you build later. MCP moves the update to the server. The client discovers
available tools at connection time, so it picks up new or modified tools
automatically. The server boundary also means you can version, restart, or
swap the implementation entirely without touching a single caller — as long
as the schema stays compatible, the contract holds.
"""

# ── Week 5 architecture ────────────────────────────────────────────────────
# Describe your full sovereign agent at Week 5 scale.
# At least 5 bullet points. Each bullet must be a complete sentence
# naming a component and explaining why that component does that job.

WEEK_5_ARCHITECTURE = """
- The MCP venue server acts as the single source of truth for all tool
  calls, so any agent or action framework connects to it without needing
  to know how venue data is stored or filtered.
- A LangGraph ReAct agent using Llama-3.3-70B-Instruct handles open-ended
  research queries because the model loop — tool call, observe, decide —
  works well for tasks where the number and order of steps is unknown in advance.
- A DeepSeek R1 planner node (added in Week 3) decomposes multi-step briefs
  into a structured task list before the executor agent begins, reducing
  wasted tool calls and improving reliability on complex bookings.
- A vector store loaded at session start (Week 4 CLAUDE.md memory) gives the
  agent access to past booking decisions and known constraints without
  re-running expensive web searches from scratch every session.
- An observability layer with LangSmith traces and cost counters (Week 5)
  provides the audit trail required to justify autonomous bookings to
  stakeholders and catches regressions before they reach production.
"""

# ── The guiding question ───────────────────────────────────────────────────
# Which agent for the research? Which for the call? Why does swapping feel wrong?
# Must reference specific things you observed in your runs. Min 60 words.

GUIDING_QUESTION_ANSWER = """
In Query 1 I watched the LangGraph agent call search_venues, get two
candidates back, then independently decide to call get_venue_details for
the best one — without any instruction to do so. That unprompted follow-up
is the thing a ReAct loop is good at: reasoning over a tool result and
choosing the next step without a script. A rule-based system can't do that;
it would need the developer to pre-declare "after search, always fetch details."

Rasa CALM is right for the confirmation call precisely because it cannot
improvise. The flow runs (guests → vegan → deposit → validate) and nothing
can reorder or skip it. Swapping them feels wrong in both directions:
a LangGraph agent could skip the deposit check if the conversation led it
somewhere unexpected; a CALM agent given a free-form research task would
hit the first unanswered question and stall — exactly what happened in
Exercise 3 Conversation 3 when the parking question arrived. Each architecture
has a constraint that is simultaneously its biggest weakness and its biggest
strength, depending entirely on what you're building.
"""
