# Exercise 4 — Insights & Issues

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
