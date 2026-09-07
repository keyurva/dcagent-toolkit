# Tool: `inspect_indicator_nodes`

## Purpose
Unified metadata and ontology inspection tool that retrieves provenance, date coverage, and populated breakdown dimensions (`StatVarGroup` slices and `Topic` members) for candidate `StatisticalVariable` or `Topic` (`dc/topic/...`) DCIDs resolved by `search_indicators`.

When `place_dcids` is provided, all returned breakdown dimensions and sample slice DCIDs are guaranteed to have observations populated in Data Commons for the specified places.

## Standard Two-Step Discovery & Inspection Workflow
Always use `inspect_indicator_nodes` as **Step 2** immediately after `search_indicators`:

1. **Step 1: NL Concept Resolution (`search_indicators`)**:
   - Decompose the user's natural language request into atomic NL concepts (e.g., for *"tell me about health and demographics of California"*, resolve `"health"` and `"demographics"`).
   - `search_indicators` acts as a concept resolver, returning candidate `Topic` or headline `StatisticalVariable` DCIDs for each concept.
2. **Step 2: Unified Metadata & Ontology Inspection (`inspect_indicator_nodes`)**:
   - Pass the union of candidate DCIDs and `place_dcids` into `inspect_indicator_nodes` in a single batch call.
   - **Replaces `get_variable_metadata`**: Returns seed provenance (`provenances`), temporal coverage (`earliest_date`, `latest_date`), and all populated breakdown dimensions (`dimension`, `available_count`, `sample_slices`).
   - **For Breakdown & Share Queries** (e.g., *"emissions by sector"*, *"population by age"*): Use `sample_slices` (`slice_value -> sv_dcid`) to select the exact slice DCID for `get_observations`.
   - **For General Queries**: Use the returned breakdown dimensions to proactively inform the user of related demographic or sector breakdowns available in Data Commons.
