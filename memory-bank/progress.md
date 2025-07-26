# Progress

## What Works

- The project has a new, clean, and maintainable structure with a clear separation of concerns:
  - All raw game data is centralized in the `data/` directory.
  - All application code is centralized in the `simulators/` directory.
- The core goals and product vision are documented in `projectbrief.md` and `productContext.md`.
- The technical architecture is documented in `systemPatterns.md`.

## What's Left to Build

- **Data Pipeline:** A robust data parsing pipeline needs to be created to transform the files from `data/raw/` into a structured, machine-readable format (like JSON) in a `data/parsed/` directory.
- **Simulator Refactoring:** The simulator code needs to be updated to read from the new structured data source (`data/parsed/`).
- **API Endpoints:** The Flask API needs to be fully implemented or verified to serve data to the frontend.
- **Frontend Dashboards:** The UI needs to be connected to the backend API and fully developed.
- **Comprehensive Testing:** The entire data pipeline and simulation process needs to be tested.

## Current Status

- **Structural Refactoring Complete.** The foundational file structure has been successfully reorganized. The raw data has been cleaned up and consolidated. The project is now ready for the next phase: implementing the data parsing pipeline.

## Known Issues

- The exact versions of the raw game data are unknown and may be outdated. This needs to be verified.

## Evolution of Project Decisions

- **Project Restructuring:** A key decision was made to halt new feature development in favor of a significant refactoring effort. This was done to address issues of poor data structure and a disorganized codebase, setting a stronger foundation for future work. The new structure separates data (`data/`) from application code (`simulators/`).
