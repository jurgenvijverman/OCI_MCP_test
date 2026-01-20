

# OCI MCP Server & AI Agent

## Prerequisites

- Python 3.10+
- [Poetry](https://python-poetry.org/docs/#installation)
- Oracle Cloud account and `~/.oci/config` set up
- OpenAI API key

## Installation

Clone the repository and install dependencies:

```sh
git clone https://github.com/jurgenvijverman/OCI_MCP_test.git
cd OCI_MCP_test
poetry install
```

## Configuration

### Server (.env)
Create a `.env` file in `oci_mcp_server/` with your compartment OCID:

```
OCI_COMPARTMENT_OCID=ocid1.compartment.oc1..your_compartment_ocid
```

### Agent (.env)
Create a `.env` file in `ai_agent/` with your OpenAI API key:

```
OPENAI_API_KEY=your_openai_api_key_here
```

## Running the OCI MCP Server

1. Ensure your OCI config is set up (default: `~/.oci/config`).
2. Ensure `oci_mcp_server/.env` contains your compartment OCID.
3. Start the server:

```sh
poetry run uvicorn oci_mcp_server.server:app --reload
```

The server will be available at http://localhost:8000

## Running the AI Agent

1. Ensure `ai_agent/.env` contains your OpenAI API key.
2. Run the agent interactively:

```sh
poetry run python ai_agent/agent.py
```

Type your questions and press Enter. Press Ctrl+C to exit.

## Security

- `.env` files and `.venv` folder are excluded from git via `.gitignore`.
- Never commit your API keys or secrets to version control.

## Project Structure

- `oci_mcp_server/` — FastAPI server exposing OCI network config via REST
- `ai_agent/` — AI agent that interacts with the server and OpenAI

## License

MIT or your chosen license.
