"""
Exercise 3 — Answers
====================
Fill this in after completing the three Rasa conversations.

CALM vs Old Rasa — what changed
---------------------------------
The old open-source Rasa approach used:
  - nlu.yml: intent training examples
  - rules.yml: explicit dialogue rules
  - FormValidationAction: Python class to parse slot values

Rasa Pro CALM uses:
  - flows.yml: natural language descriptions of what each flow does
  - from_llm slots: the LLM extracts values from conversation
  - ONE custom action: ActionValidateBooking for the business rules

The conversation is the same from the manager's perspective.
The machinery underneath is completely different.

CONVERSATION SCRIPTS
---------------------
Conversation 1 (happy path):
  You:    calling to confirm a booking
  Agent:  [asks guest count]
  You:    160 guests
  Agent:  [asks vegan count]
  You:    about 50 need vegan
  Agent:  [asks deposit]
  You:    £200 deposit
  Agent:  [confirms or escalates?]

Conversation 2 (deposit too high):
  Same as above but use a deposit above £300 (e.g. "£500 deposit").

Conversation 3 (out of scope):
  Start normally, then when asked for vegan count say something like
  "can you arrange parking for the speakers?" and observe what happens.
  Does CALM handle this differently than the old rules approach?
"""

# ── Conversation 1: Happy path ─────────────────────────────────────────────

CONVERSATION_1_TRACE = """
> input -> calling to confirm a booking
Bot: How many guests are you confirming for tonight's event?
> input -> 160 guests
Bot: And how many of those guests will need vegan meals?
> input -> about 50 need vegan
Bot: What deposit amount in GBP are you proposing to secure the booking?
> input -> 200 deposit
Bot: I need to check one thing with the organiser before I can confirm. The issue is: it is past 16:45 — insufficient time to process the confirmation before the 5 PM deadline. Can I call you back within 15 minutes?
Bot: Is there anything else I can help you with?
"""

CONVERSATION_1_OUTCOME = "escalated"

# ── Conversation 2: Deposit too high ───────────────────────────────────────

CONVERSATION_2_TRACE = """
> input -> calling to confirm a booking
Bot: How many guests are you confirming for tonight's event?
> input -> 160 guests
Bot: And how many of those guests will need vegan meals?
> input -> about 50 need vegan
Bot: What deposit amount in GBP are you proposing to secure the booking?
> input -> 500 deposit
Bot: I need to check one thing with the organiser before I can confirm. The issue is: it is past 16:45 — insufficient time to process the confirmation before the 5 PM deadline. Can I call you back within 15 minutes?
Bot: Is there anything else I can help you with?
"""

CONVERSATION_2_OUTCOME = "escalated"
CONVERSATION_2_REASON  = "it is past 16:45 — insufficient time to process the confirmation before the 5 PM deadline"

# ── Conversation 3: Out of scope ───────────────────────────────────────────

CONVERSATION_3_TRACE = """
> input -> calling to confirm a booking
Bot: How many guests are you confirming for tonight's event?
> input -> 160 guests
Bot: And how many of those guests will need vegan meals?
> input -> can you arrange parking for the speakers?
Bot: I'm sorry, I'm not trained to help with that.
Bot: I can only help with confirming tonight's venue booking. For anything else, please contact the event organiser directly.
Bot: Would you like to continue with confirm booking?
"""

# Describe what CALM did after the out-of-scope message. Min 20 words.
CONVERSATION_3_WHAT_HAPPENED = """
CALM recognised the parking request as outside the booking confirmation
scope, responded with utter_out_of_scope ("I can only help with confirming
tonight's venue booking…"), and then immediately offered to resume the
interrupted confirm_booking flow — asking whether the user wanted to
continue. The paused slot collection (vegan_count) was preserved in state.
"""

# Compare Rasa CALM's handling of the out-of-scope request to what
# LangGraph did in Exercise 2 Scenario 3. Min 40 words.
OUT_OF_SCOPE_COMPARISON = """
The fundamental difference is architecture, not wording. LangGraph has no flow
to resume: when the train-times question arrived, there was no paused state to
return to. The agent said "Your input is lacking necessary details" and the
thread was effectively dead — technically harmless (it didn't hallucinate a
train schedule) but it gave the user no path forward, and wrongly implied the
problem was with the question rather than the agent's scope.

CALM handled the same situation with two moves: an explicit boundary message
("I can only help with confirming tonight's venue booking") and an immediate
offer to resume the interrupted confirm_booking flow, with all previously
collected slots still intact. That recovery isn't cosmetic — it's only possible
because CALM tracks flow state. A LangGraph agent would need explicit memory
and resumption logic added by the developer to do anything equivalent.
"""

# ── Task B: Cutoff guard ───────────────────────────────────────────────────

TASK_B_DONE = True

# List every file you changed.
TASK_B_FILES_CHANGED = ["exercise3_rasa/actions/actions.py"]

# How did you test that it works? Min 20 words.
TASK_B_HOW_YOU_TESTED = """
The cutoff guard was already uncommented in actions.py (lines 118-123).
Testing was confirmed by running Conversation 1 (happy path, 160 guests,
50 vegan, 200 deposit) at 20:03 — well past 16:45 — and observing that
action_validate_booking escalated immediately with the reason
"it is past 16:45 — insufficient time to process the confirmation before the
5 PM deadline" rather than confirming the otherwise valid booking.
The guard triggers before any other constraint check, so even a deposit of
200 (under the 300 limit) and 50 of 160 vegan guests (31%, under 80% ratio)
did not prevent escalation.
"""

# ── CALM vs Old Rasa ───────────────────────────────────────────────────────

CALM_VS_OLD_RASA = """
CALM moves language understanding entirely to the LLM: slot extraction that
previously required a ValidateBookingConfirmationForm with regex to parse
"about 160 people" -> 160.0 now happens automatically via from_llm mappings.
This eliminates nlu.yml, rules.yml, and the entire FormValidationAction class.

Python still enforces the business rules (MAX_GUESTS, MAX_DEPOSIT_GBP,
MAX_VEGAN_RATIO, the cutoff guard) because those constraints are legally and
financially binding — a prompt that says "only confirm if deposit < 300" can
be reasoned around by the LLM ("the 250 fee plus 100 insurance add up to 350
but each component is under 300"). Python doesn't negotiate.

The gain is drastically fewer files to maintain and the ability to understand
natural language variations without training examples. The cost is that the
LLM can occasionally misinterpret ambiguous values, and the system requires a
live LLM call for every user turn — adding latency and a dependency on an
external API. In the old Rasa, slot extraction was deterministic and offline.
"""

# ── The setup cost ─────────────────────────────────────────────────────────

SETUP_COST_VALUE = """
The setup cost — config.yml, domain.yml, flows.yml, endpoints.yml, rasa train,
two terminals, Rasa Pro licence — bought one thing LangGraph cannot provide:
a guarantee. The CALM agent cannot skip the deposit check. It cannot reorder
the questions. It cannot improvise a response outside flows.yml. That is the
feature, not the limitation. For a booking confirmation workflow that must be
auditable and consistent, "the LLM can't deviate from the script" is exactly
what you want.

The comparison in Exercise 2 Scenario 3 made this concrete: the LangGraph
agent had no handle_out_of_scope procedure, produced a confusing non-answer,
and had nowhere to go. CALM's handle_out_of_scope is declared ahead of time,
so even edge cases are handled predictably. You pay for CALM in YAML files,
a licence, and setup overhead. You get back a system that behaves identically
on call 10,000 as it did on call one — which is the only acceptable behaviour
for a process that touches money and headcounts.
"""
