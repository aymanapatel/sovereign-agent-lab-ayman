"""
Exercise 1 — Answers
====================
Fill this in after running exercise1_context.py.
Run `python grade.py ex1` to check for obvious issues before submitting.
"""

# ── Part A ─────────────────────────────────────────────────────────────────

# The exact answer the model gave for each condition.
# Copy-paste from your terminal output (the → "..." part).

PART_A_PLAIN_ANSWER    = "The Haymarket Vaults"
PART_A_XML_ANSWER      = "The Albanach"
PART_A_SANDWICH_ANSWER = "The Albanach"

# Was each answer correct? True or False.
# Correct = contains "Haymarket" or "Albanach" (both satisfy all constraints).

PART_A_PLAIN_CORRECT    = True
PART_A_XML_CORRECT      = True
PART_A_SANDWICH_CORRECT = True

# Explain what you observed. Minimum 30 words.

PART_A_EXPLANATION = """
All three conditions were correct, but the format influenced which valid venue the model chose.
PLAIN format returned "The Haymarket Vaults" (appearing later in the list), while XML and SANDWICH
both returned "The Albanach" (the first entry). This suggests that structured XML formatting
amplifies primacy bias — the model anchors on the first well-formed record it encounters and stops
searching once constraints are satisfied, rather than evaluating all options exhaustively.
"""

# ── Part B ─────────────────────────────────────────────────────────────────

PART_B_PLAIN_ANSWER    = "The Haymarket Vaults"
PART_B_XML_ANSWER      = "The Albanach"
PART_B_SANDWICH_ANSWER = "The Albanach"

PART_B_PLAIN_CORRECT    = True
PART_B_XML_CORRECT      = True
PART_B_SANDWICH_CORRECT = True

# Did adding near-miss distractors change any results? True or False.
PART_B_CHANGED_RESULTS = False

# Which distractor was more likely to cause a wrong answer, and why?
# Minimum 20 words.
PART_B_HARDEST_DISTRACTOR = """
The Holyrood Arms is the more dangerous distractor because it satisfies two of three constraints
(capacity=160 and vegan=yes) and only fails on status=full. A model that evaluates constraints
partially or in sequence — checking capacity then vegan but stopping before status — would pick
it over the correct Haymarket Vaults. The New Town Vault fails vegan immediately, making it easier
to eliminate. The 70B model handled both correctly, but weaker models are more likely to
short-circuit on The Holyrood Arms specifically.
"""

# ── Part C ─────────────────────────────────────────────────────────────────

# Did the exercise run Part C (small model)?
# Check outputs/ex1_results.json → "part_c_was_run"
PART_C_WAS_RUN = True

PART_C_PLAIN_ANSWER    = "The Haymarket Vaults"
PART_C_XML_ANSWER      = "The Haymarket Vaults"
PART_C_SANDWICH_ANSWER = "The Haymarket Vaults"

# Explain what Part C showed, or why it wasn't needed. Minimum 30 words.
PART_C_EXPLANATION = """
Part C ran because both Part A and Part B were all-correct on the 70B model, meaning no structural
effect was visible yet. The 8B model (Meta-Llama-3.1-8B-Instruct) also answered correctly in all
three conditions, but interestingly it consistently chose "The Haymarket Vaults" across all formats
rather than "The Albanach". This is the opposite of the 70B pattern — the smaller model appears
less susceptible to primacy bias in XML-structured input, suggesting it parses XML tags less
fluently and evaluates entries more sequentially without anchoring on the first match.
"""

# ── Core lesson ────────────────────────────────────────────────────────────

# Complete this sentence. Minimum 40 words.
# "Context formatting matters most when..."

CORE_LESSON = """
Context formatting matters most when the signal-to-noise ratio is low: when near-miss distractors
closely resemble the correct answer, when the model must evaluate multiple constraints simultaneously
rather than matching a single keyword, and when using smaller or weaker models with limited
multi-step reasoning capacity. On clean datasets with a strong frontier model the effect can vanish
entirely — every format works. But add adversarial distractors, bury the answer mid-context, or
drop to a smaller model and the structural scaffold (XML tags, repeated query reminders at top and
bottom) becomes the difference between the model finding the needle and picking the wrong piece of hay.
"""