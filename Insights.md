# Insights & Issues — Week 1 Exercises

---

# Exercise 3 — Rasa Pro CALM

## Issues Encountered

### 1. `'ascii' codec can't encode character '\u2713'` — Rasa + LiteLLM encoding bug
**Problem:** When Rasa's `CompactLLMCommandGenerator` called the Nebius LLM via LiteLLM using `provider: self-hosted`, every request failed with `InternalServerError: Hosted_vllmException - 'ascii' codec can't encode character '\u2713' in position 21`. The same error appeared for the `openai` provider on embeddings. Direct LiteLLM calls to the same endpoint worked fine.

**Root cause:** The first Rasa server startup was launched from the wrong working directory (not `exercise3_rasa/`) before environment variables were fully exported, causing the server to fail to resolve `${NEBIUS_KEY}` from `endpoints.yml`. Once the server was restarted from `exercise3_rasa/` with properly exported `NEBIUS_KEY` and `RASA_PRO_LICENSE`, all calls succeeded.

**Fix:** Export environment variables before running `uv run rasa run`, and always start the server from the `exercise3_rasa/` directory.

---

### 2. Two terminals required — action server + Rasa server must both run
**Problem:** The exercise requires two separate processes: `rasa run actions` (port 5055) handles custom Python logic; `rasa run --enable-api` (port 5005) handles the conversation. If the action server is not running when `action_validate_booking` is triggered, the conversation silently errors.

**Fix:** Start both processes before sending any messages. Check `curl http://localhost:5055/health` and `curl http://localhost:5005/status` before running conversations.

---

### 3. Task B cutoff guard was already uncommented
**Problem:** The exercise description says to uncomment four lines in `actions.py`. The lines were already uncommented in the committed file (Task B was completed before this run). However, the model is trained once and cached — `actions.py` changes are picked up by the action server on restart without retraining.

**Observation:** Because it was 20:03 (past 16:45), the cutoff guard triggered on every conversation including the "happy path" Conversation 1. `CONVERSATION_1_OUTCOME` = "escalated" (valid per grade.py, which accepts "confirmed" or "escalated").

---

### 4. `FormValidationAction` in a docstring triggers grade warning
**Problem:** The `actions.py` docstring explains the old Rasa approach and mentions `FormValidationAction` by name. The grade.py check does a string-match on the source file, triggering a `⚠️` warning.

**Status:** Warning only — no failure. The string appears in a comment, not as functional code. Left as-is since it's part of the exercise's educational documentation.

---

## Key Learnings

### CALM's deterministic flow contract
The slot collection order (guest_count → vegan_count → deposit_amount_gbp → action_validate_booking) is guaranteed by `flows.yml`. The LLM cannot reorder or skip steps. This is the key property that makes CALM suitable for auditable booking confirmations — not a limitation but a deliberate design choice.

### Python enforces business rules; LLM handles language
In Conversation 1, the deposit (£200) and vegan ratio (50/160 = 31%) both passed the guards. The conversation escalated solely because of the time-based cutoff guard in Python. The LLM correctly extracted the slot values; Python correctly applied the constraint. Neither component did the other's job.

### Out-of-scope deflection with flow resumption
When the user asked about parking in Conversation 3, CALM triggered `handle_out_of_scope`, displayed `utter_out_of_scope`, and then offered to resume `confirm_booking`. The paused flow's slot state was preserved. LangGraph in Exercise 2 had no equivalent — its out-of-scope response was a confusing "your input lacks details" that gave no indication of the agent's actual scope.

### REST API for automated testing
The `--enable-api` flag exposes a `POST /webhooks/rest/webhook` endpoint that accepts `{"sender": "...", "message": "..."}`. This allows scripted conversation testing without interactive `rasa shell`. Using unique `sender` IDs isolates conversation state.

---

## Run Log Files (`week1/outputs/txt/ex3/`)

| File | Description |
|---|---|
| `01_conv1_happy.txt` | Happy path: 160 guests, 50 vegan, £200 deposit — escalated by time cutoff |
| `02_conv2_deposit_high.txt` | Deposit too high: £500 — escalated by time cutoff |
| `03_conv3_out_of_scope.txt` | Parking request during vegan_count collection — deflected then offered to resume |

---

# Exercise 4 — MCP Client

## Issues Encountered

### 1. `asyncio.run()` inside a running event loop
**Problem:** `_make_mcp_caller` called `asyncio.run(_inner())` synchronously from within the LangGraph agent's tool execution path. Since `main()` is itself an async function (run via `asyncio.run(main())`), the outer event loop was already active. Calling `asyncio.run()` inside a running loop raises `RuntimeError: This event loop is already running`.

**Fix:** Wrap each MCP call in a `concurrent.futures.ThreadPoolExecutor`. The worker thread has no running event loop, so `asyncio.run()` works cleanly there.

---

### 2. StructuredTool had no parameter schema
**Problem:** `StructuredTool.from_function` was called with `func=_make_mcp_caller(...)` — a function whose only signature is `**kwargs`. LangChain infers the tool schema from the function signature; `**kwargs` produces an empty schema. With no schema, the LLM doesn't know what arguments to pass, so it serialised the intended call as a raw JSON text string instead of invoking the function-calling interface.

**Fix:** Added `_build_args_schema()` which converts the MCP tool's `inputSchema` (a JSON Schema dict) into a typed Pydantic model using `pydantic.create_model`. The model is passed as `args_schema=` to `StructuredTool.from_function`.

---

### 3. `extract_trace` missed LangChain's `tool_calls` attribute
**Problem:** The original `extract_trace` only checked for `content` blocks of type `"tool_use"` (Anthropic API format). LangChain's `ChatOpenAI` backend puts tool invocations on `AIMessage.tool_calls` — a list attribute, not a content block. As a result, all tool calls were invisible in the trace and the agent appeared to do nothing.

**Fix:** Added a primary check `if hasattr(m, "tool_calls") and m.tool_calls` (mirroring the pattern in `research_agent.py`), with the old content-block check kept as a fallback.

---

### 4. No system prompt → model wrote JSON text instead of calling tools
**Problem:** Without a system prompt, Llama-3.3-70B-Instruct on the Nebius endpoint tends to batch all intended tool calls into a single JSON text block when the task is multi-step. The agent returned `{"type": "function", "name": "search_venues", ...}` as plain AI content instead of invoking the tool.

**Fix:** Added the same `_SYSTEM_PROMPT` used in `research_agent.py`: instruct the model to call tools one at a time through the function-calling interface, never as text.

---

## Key Learnings

### MCP's real value
The experiment proved it directly: changing `"status": "available"` → `"full"` for The Albanach in `mcp_venue_server.py` immediately changed the agent's search results on the next run. `exercise4_mcp_client.py` was not touched. This is the MCP contract: the server is the single source of truth; all clients pick up changes through discovery rather than code edits.

### Schema is not optional
Without a schema, structured tool calling silently degrades to text generation. The LLM does its best — it writes out what it would call — but the tools never execute. This is hard to debug because the model output looks plausible. Always pass `args_schema` when wrapping external tools as LangChain `StructuredTool`s.

### Async bridge pattern
Mixing a synchronous LangChain/LangGraph agent with an async MCP client requires an explicit thread boundary. The cleanest approach is a `ThreadPoolExecutor` around each `asyncio.run()` call in the tool bridge. This keeps the MCP async code isolated in a fresh thread and the LangGraph sync loop unaffected.

### Agent specialisation confirmed
Query 2 (300 guests) demonstrated the agent calling `search_venues` three times with the same parameters after getting an empty result — the model retried instead of accepting the answer. This over-checking behaviour is benign here but underscores that a free-form ReAct loop is not suited for deterministic workflows where each step must happen exactly once. Rasa CALM is the right tool for that pattern.

---

## Run Log Files (`week1/outputs/txt/ex4/`)

| File | Description |
|---|---|
| `01_normal_run.txt` | Full trace — both queries with Albanach available |
| `02_experiment_albanach_full.txt` | Same queries after setting Albanach status to `full`; Albanach disappears from Query 1 results |
