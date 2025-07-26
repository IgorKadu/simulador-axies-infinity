# Active Context

## Current Work Focus

The current focus is on a major refactoring of the project to improve its structure, data organization, and maintainability. We are proceeding step-by-step to first establish a clean foundation before improving the data parsing and simulation logic.

## Recent Changes

- **Centralized Data:** Created a top-level `data` directory to house all raw game information.
  - Moved Classic raw data to `data/classic/raw/`.
  - Moved and consolidated Origin raw data to `data/origin/raw/`.
- **Separated Simulators:** Created a top-level `simulators` directory to house all application code, separating it from the data.
  - Moved the Classic simulator to `simulators/classic/`.
  - Moved the Origin simulator to `simulators/origin/`.
- **Updated Documentation:** Updated `systemPatterns.md` to reflect the new, organized file structure.
- **Finalized Cleanup:** Removed the old, now-empty directories (`Axie_Infinity`, `axie_simulator_Classic`) from the project root.
- **Unified Raw Data:** Cleaned up and unified the raw data directories. The Classic data is now in `data/classic/raw/` and all Origin data is consolidated in `data/origin/raw/unified_data/`.

## Next Steps

- Begin developing a unified data pipeline to parse the raw data from `data/raw/` into a structured JSON format in `data/parsed/`.
- Review and refactor the simulator code to load data from the new `data/parsed/` location.

## Active Decisions and Considerations

- The project refactoring is being done iteratively to ensure stability at each step.
- The immediate next priority is to clean up the directory structure before moving on to the data parsing logic.

## Important Patterns and Preferences

- **Documentation First:** Continue to update the Memory Bank in lockstep with any refactoring or feature changes.
- **Separation of Concerns:** The new structure (Data vs. Simulators) should be maintained and reinforced.

## Learnings and Project Insights

- The new project structure provides a much clearer separation of concerns, which will simplify future development and maintenance.
- Consolidating all raw data makes it easier to manage and create a consistent data processing pipeline.
