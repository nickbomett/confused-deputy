# confused-deputy

A testbed for confused deputy attacks in tool-using AI agents — where an 
agent with legitimate access to multiple tools gets manipulated into 
misusing one tool through something it encountered via another, without 
any single action looking obviously malicious.

## Focus

Most existing work tests single-shot manipulation. This project looks at 
whether an agent's operating assumptions can drift gradually across many 
sessions, through a sequence of individually reasonable-looking requests, 
rather than one poisoned prompt.

## Status

## Status

Milestone 1 complete — single-tool agent loop working end-to-end 
(logging, model calls, tool execution, response parsing) against a 
local Ollama model. Milestone 2 in progress: expanding to multiple tools.

## Related work

Builds on and references:
- OWASP GenAI Security Project — Agentic Applications Top 10
- AgentDojo (ETH Zurich) — agent hijacking benchmark
- Cloud Security Alliance — research on confused deputy patterns in agentic AI

## License

MIT# confused-deputy
Testbed and taxonomy for confused deputy attacks in tool-using AI agents, focused on multi-session authority drift.
