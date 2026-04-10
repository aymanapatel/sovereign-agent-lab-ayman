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
All three formats gave a correct answer, but they didn't agree on which one. PLAIN returned
"The Haymarket Vaults" — the second eligible venue — while XML and SANDWICH both landed on
"The Albanach", which appears first. The mechanism matters: XML tags create hard boundaries
between records, so the model processes each <venue> block as a discrete unit. When the first
record passes all constraints, it commits and stops. PLAIN text flows together without those
boundaries, so the model keeps scanning and ends up further into the list. Formatting changed
not just readability but search depth — and with it, which correct answer came out.
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
Part C ran because both Part A and Part B were all-correct on the 70B model — no structural
differentiation visible yet. The 8B model (Meta-Llama-3.1-8B-Instruct) also got every answer
right, but with an inverted pattern: it consistently picked "The Haymarket Vaults" regardless
of format, where the 70B model swung toward "The Albanach" under XML. My best explanation is
that the 70B model reads XML structure as signal and anchors on the first well-formed record;
the 8B model either ignores XML cues or scans more linearly and ends up further into the list.
The more interesting takeaway: format sensitivity is not simply worse as models get smaller —
it's different. A weaker model can be less affected by structural priming for reasons entirely
unrelated to capability.
"""

# ── Core lesson ────────────────────────────────────────────────────────────

# Complete this sentence. Minimum 40 words.
# "Context formatting matters most when..."

CORE_LESSON = """
Context formatting matters most when the signal-to-noise ratio is low — when near-miss distractors
closely resemble the correct answer, when the model must check multiple constraints rather than
match a single keyword, and when you are working with smaller models that have limited multi-step
reasoning. On clean data with a strong model, the effect vanishes: every format works and the task
is easy regardless. But add adversarial distractors, bury the answer mid-context, or drop to a
weaker model, and the structural scaffold — XML tags, repeated query reminders at top and bottom —
becomes the difference between finding the needle and pulling out the wrong piece of hay. The lesson
is not "always use XML." It is: know when formatting is doing real cognitive work for the model.
"""