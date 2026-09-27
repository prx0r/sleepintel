# JEV-MCP PROOF (live 2026-09-26 — npx @jkudish/jev-mcp, OpenRouter key)

Server: init ok, 11 tools. Proven shapes (exact args or 422):
- jev_noul {propositions: [str]} ✓
- jev_decide {decision, evidence, priorities, candidates:[{id, description}]}
  → ship 0.79 on Satie evening ✓
- jev_classify {items:[{id, text}], classes:[{id, description}]} ✓
- jev_rerank {query, candidates:[{id, text}]} → ranked list ✓
Policy: our scripts/jev.py stays primary (pinned model, audit log);
MCP tools for interactive/agent sessions. Corrections loop (classify.py
--corrections) feeds cases.jsonl → calibration.
