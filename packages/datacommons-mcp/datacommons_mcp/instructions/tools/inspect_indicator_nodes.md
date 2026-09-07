# Tool: `inspect_indicator_nodes`

## Purpose
Traverses the Data Commons indicator ontology (`StatVarGroup` hierarchy and `Topic` memberships) starting from one or more candidate `StatisticalVariable` or `Topic` (`dc/topic/...`) DCIDs returned by `search_indicators`.

When `place_dcid` is provided, all returned breakdown dimensions and sample slice DCIDs are guaranteed to have observations populated in Data Commons for that place.

## Standard Two-Step Indicator Discovery Workflow
Always use `inspect_indicator_nodes` as **Step 2** immediately after `search_indicators`:

1. **Step 1 (`search_indicators`)**: Pass the user's natural language query to find top candidate headline `StatisticalVariable` or `Topic` DCIDs.
2. **Step 2 (`inspect_indicator_nodes`)**: Pass those candidate DCIDs and `place_dcid` into `inspect_indicator_nodes`:
   - **For Breakdown & Share Queries** (e.g., *"emissions by sector"*, *"population by age"*): Use the returned `dimension` and `sample_slices` (`slice_value -> sv_dcid`) to select the exact slice DCID for `get_observations` without guessing or running repeated searches.
   - **For General Queries** (e.g., *"tell me about greenhouse gas emissions in California"*): Use the returned dimensions list to proactively inform the user of related demographic or sector breakdowns available in Data Commons.
