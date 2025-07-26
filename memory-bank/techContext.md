# Tech Context

## Technologies Used

- **Backend:**
  - Python 3.x
  - Flask
- **Frontend:**
  - HTML5
  - CSS3
  - JavaScript (ES6+)
  - Potentially a JS framework like Vue.js or React (to be confirmed by inspecting frontend code)
- **Data:**
  - JSON
  - Plain text files (.txt)

## Development Setup

- A Python environment with `Flask` and other dependencies listed in `requirements.txt` files is needed to run the backend simulators and APIs.
- A modern web browser is sufficient to run the frontend dashboards.
- A code editor like VSCode is recommended for development.

## Technical Constraints

- The simulators must be kept up-to-date with the latest game patches and balance changes from Sky Mavis.
- The simulation logic needs to be as accurate as possible to provide meaningful results.
- The frontend must be responsive and work well on different screen sizes.

## Dependencies

- The Python backend has dependencies that can be installed from the `requirements.txt` file in `simulators/origin/axie_simulator_Origin/`.
- The frontend projects have JavaScript dependencies listed in their `package.json` files, which can be installed using a package manager like `npm` or `pnpm`.

## Tool Usage Patterns

- **Data Parsing:** Python scripts are used to parse raw game data from text files into structured JSON format.
- **Simulation:** The core simulation logic is executed in Python.
- **Web Server:** Flask is used to create a simple local server to expose simulation results via a REST API.
- **Frontend Development:** Frontend assets are likely bundled and served using a tool like Vite, as suggested by the presence of `vite.config.js`.
