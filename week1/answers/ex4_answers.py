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
MCP gives you a language-agnostic, transport-agnostic contract over stdio.
Any client — the LangGraph agent today, a Rasa action tomorrow, a CLI tool
next week — connects to the same server without knowing how the tools are
implemented. When the venue database changes, you update one file and every
client picks it up on the next call. With hardcoded tools you must update
each caller separately; with MCP the server is the single source of truth
and tool discovery is dynamic. That boundary also means the server can be
versioned, restarted, or swapped for a different implementation without
touching client code at all.
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
The LangGraph ReAct loop is the right agent for research: in Query 1 I
watched it call search_venues, receive two candidates, then independently
decide to call get_venue_details for the best one — without being told to.
That step-by-step reasoning over tool results is exactly what a free-form
research task requires, and a rule-based system could not have decided which
venue to detail-fetch on its own.

Rasa CALM is the right agent for the confirmation call: it follows a
declared flow (confirm_booking, ask for deposit, escalate if over limit)
where every step is auditable and the outcome is deterministic. Swapping
them feels wrong because a LangGraph agent has no guaranteed path through
a booking flow — it could skip the deposit check or invent an escalation
condition — while Rasa on a research task would break at the first question
it has no declared step to answer, as I observed in Exercise 3's out-of-scope
response where the CALM agent could not improvise beyond its flows.
"""
