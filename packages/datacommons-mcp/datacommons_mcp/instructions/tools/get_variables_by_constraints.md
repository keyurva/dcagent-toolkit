# Tool: `get_variables_by_constraints`

## Purpose
Queries Spanner directly to resolve exact `StatisticalVariable` DCIDs that match a specified combination of constraint property-value pairs (`constraints`).

## Critical Rule: Never Pass Unconstrained Base Variables
- **NEVER pass unconstrained base variables (variables with no `constraintProperties`, e.g. `Count_Person`) as `seed_dcid` when resolving breakdown queries.**
- Always select `seed_dcid` from the candidate variables in the `constraint_properties` table returned by `search_indicators` (variables that already possess `constraintProperties`).

## Required Parameters
- `seed_dcid` (`str`): A constrained `StatisticalVariable` DCID selected from `constraint_properties` in `search_indicators`.
- `constraints` (`dict[str, list[str]]`): **Strictly required non-empty map** of constraint property names to lists of target constraint value DCIDs discovered from `inspect_indicator_nodes(..., properties=[...])` (e.g. `{"gender": ["Female"], "race": ["BlackOrAfricanAmericanAlone"]}`).
  - **NEVER pass an empty `constraints` dictionary (`{}`)**. Empty constraints will return an empty table immediately.
- `place_dcids` (`list[str] | None`): Optional list of place DCIDs to filter returned variables by observation availability.

## Discovery Workflow
1. **Step 1 (`search_indicators`)**: Search using the full user query including constraints (e.g. `"population by gender age and race"`). Inspect the returned `constraint_properties` table (`headers: ["dcid", "constraint_properties"]`) to identify candidate variables that already have breakdown properties matching your query.
2. **Step 2 (`inspect_indicator_nodes`)**: Call `inspect_indicator_nodes(dcids=[candidate_dcid], place_dcids=[...], properties=["gender", "age", "race"])`. Pass `properties` explicitly to retrieve the valid `constraintValues` (`valueDcid`) for each requested property.
3. **Step 3 (`get_variables_by_constraints`)**: Call `get_variables_by_constraints(seed_dcid=candidate_dcid, constraints={"gender": ["Female"], ...}, place_dcids=[...])` with the exact `valueDcid` strings to obtain the exact variable DCID for `get_observations`.
