# Tool: `inspect_indicator_nodes`

## Purpose
Unified metadata and ontology inspection tool that retrieves provenance, date coverage, and targeted breakdown dimensions (`constraintValues`) for candidate `StatisticalVariable` DCIDs resolved by `search_indicators`.

## Critical Rule: Never Pass Unconstrained Base Variables for Breakdowns
- **NEVER pass unconstrained base variables (variables with no `constraintProperties` in the `constraint_properties` table, e.g. `Count_Person`) into `inspect_indicator_nodes` when resolving breakdown queries.**
- Always select candidate DCIDs from the `constraint_properties` table returned by `search_indicators` (i.e. variables that already possess `constraintProperties` matching the user's requested breakdown dimensions).

## Parameters & Required Contract
- `dcids` (`list[str]`): List of candidate `StatisticalVariable` DCIDs selected from `search_indicators` (e.g. constrained variables from `constraint_properties`).
- `place_dcids` (`list[str] | None`): Place DCIDs to scope provenance and observation availability.
- `properties` (`list[str] | None`): **REQUIRED when inspecting breakdown constraint values.**
  - **If `properties` is omitted or empty (`None` / `[]`)**: Returns **node metadata only** (`name`, `provenances`, `earliestDate`, `latestDate`, `rootSvg`) with **zero breakdown scans**.
  - **If `properties` is provided (e.g. `properties=["gender", "age", "race"]`)**: Returns only breakdown dimensions and valid `constraintValues` (`valueDcid`) matching those requested `properties`.

## Three-Stage Constraint Discovery Workflow
1. **Step 1 (`search_indicators`)**: Search with the full user query including constraints (e.g. `"population by gender age and race"`). Check the returned `constraint_properties` table (`headers: ["dcid", "constraint_properties"]`) to identify candidate variables that already have breakdown properties matching your query.
2. **Step 2 (`inspect_indicator_nodes`)**: Pass `dcids=[candidate_dcid]` (selected from `constraint_properties`), `place_dcids=[...]`, and **`properties=["gender", "age", "race"]`**. This returns the exact valid `valueDcid` options for each property.
3. **Step 3 (`get_variables_by_constraints`)**: Pass `seed_dcid=candidate_dcid`, `constraints={"gender": ["Female"], ...}` (non-empty), and `place_dcids` to resolve the exact variable DCID for `get_observations`.
