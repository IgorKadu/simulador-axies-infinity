# System Patterns

## System Architecture

The project is divided into two main components: the Axie Infinity Classic simulator and the Axie Infinity Origin simulator. Each simulator has its own data, simulation logic, and frontend.

### Axie Infinity Classic
- **Data:** Raw game data for Classic is stored in `data/classic/raw/`. Parsed data will eventually live in `data/classic/parsed/`.
- **Simulator:** The simulator code is located in `simulators/classic/axie_simulator/`. The main simulation logic is in `simulators/classic/axie_simulator/battle_simulator.py`.
- **Frontend:** The dashboard is located in `simulators/classic/axie_simulator/axie-simulator-dashboard/`.

### Axie Infinity Origin
- **Data:** Raw, unified game data for Origin is stored in `data/origin/raw/unified_data/`. Parsed data will eventually live in `data/origin/parsed/`.
- **Simulator:** The simulator code is located in `simulators/origin/axie_simulator_Origin/`. The main simulation logic is in `simulators/origin/axie_simulator_Origin/battle_simulator.py`.
- **Frontend:** The dashboard is located in `simulators/origin/axie_simulator_Origin/axie-battle-simulator/`.

## Key Technical Decisions

- **Python for Backend:** Python was chosen for its strong data science and scripting capabilities, making it ideal for game simulation and data analysis.
- **Flask for API:** Flask is a lightweight web framework that is sufficient for serving simulation data to the frontend without unnecessary complexity.
- **JavaScript for Frontend:** Standard HTML, CSS, and JavaScript, likely with a framework like Vue.js or React, are used to create interactive and user-friendly dashboards.
- **JSON for Data Interchange:** JSON is used as the primary format for storing parsed game data and for communication between the backend and frontend.

## Design Patterns in Use

- **Model-View-Controller (MVC) Pattern:** The frontend dashboards are structured following MVC principles, separating data (Model), presentation (View), and user input handling (Controller).
- **Data-Driven Design:** The simulators are designed to be data-driven, meaning that game logic and parameters are loaded from external data files, allowing for easy updates as the game changes.
- **Modular Design:** The codebase is organized into modules with specific responsibilities (e.g., data parsing, team generation, battle simulation), promoting code reusability and maintainability.
