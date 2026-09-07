CRITICAL: Before calling this tool for the first time in a session, you MUST read the playbook resource by calling your platform's standard MCP resource-reading capability for the URI 'skill://data-commons-researcher/SKILL.md'.

Search the Data Commons Knowledge Graph for topics and statistical variables (indicators) matching a natural language query. Returns candidate indicator DCIDs, names, and data availability mappings. Can be optionally scoped to a list of target places to verify data presence.

After receiving candidate DCIDs from this tool, ALWAYS call `inspect_indicator_nodes` with the candidate DCIDs and target place DCID before guessing sub-variables or making repeated search calls.

