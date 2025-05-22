# GPT-Marketer MCP Server

This project provides an MCP (Model Context Protocol) server for marketing automation and email generation
## Configuration

Add the following configuration for cursor:

```json
{
  "mcpServers": {
    "gpt-marketer-mcp": {
      "url": "http://localhost:8000/sse",
      "env":{
        "PYTHONPATH": "",
        "ANTHROPIC_API_KEY": "",
        "TAVILY_API_KEY": ""
      },
      "environment":{
        "name": "gpt-marketer-mcp",
        "type": "venv",
        "path": "/.venv"
      }
    }
  }
}
```

- `url`: The SSE endpoint for the MCP server.
- `env`: Environment variables required for the server to function. Set your API keys here.
- `environment`: Python virtual environment configuration.

---

## How to Use in Cursor

1. **Add the MCP Server**
   - Open Cursor and go to the MCP integration settings.
   - Add a new MCP server with the following details:
     - **Name**: `gpt-marketer-mcp`
     - **URL**: `http://localhost:8000/sse`
     - **Environment Variables**: Set your `ANTHROPIC_API_KEY` and `TAVILY_API_KEY`.
     - **Python Environment**: Point to your virtual environment path (e.g., `/.venv`).

2. **Connect and Use**
   - Once added, connect to the server from Cursor.
   - You can now use the tools and capabilities provided by the GPT-Marketer MCP server directly within Cursor

---

## How to Run Using `client.py`

1. **Install Dependencies**
   - Ensure you have Python 3.8+ and a virtual environment set up.
   - Install dependencies using [uv](https://docs.astral.sh/uv/):
     ```bash
     uv pip install -r requirements.txt
     ```
   - Or, if you have a `pyproject.toml` file, you can use:
     ```bash
     uv pip install
     ```
   - For project-based dependency management and environment setup:
     ```bash
     uv sync
     ```

2. **Set Environment Variables**
   - Create a `.env` file in the project root:
     ```env
     ANTHROPIC_API_KEY=your-anthropic-key
     TAVILY_API_KEY=your-tavily-key
     ```

3. **Start the MCP Server**
   - Run the server (if not already running):
     ```bash
     uv run .\mcp_server\server.py
     ```

4. **Run the Client**
   - In a new terminal, run:
     ```bash
     uv run .\mcp_server\client.py
     ```
   - The client will connect to the MCP server, load available tools, and allow you to generate email content or perform other marketing tasks.

---

## About MCP

Model Context Protocol (MCP) is an open protocol for connecting AI applications to data sources and tools. MCP servers expose tools and resources, while MCP clients (like this project) connect to those servers to enable powerful AI-driven workflows.

For more information, see the [MCP documentation](https://modelcontextprotocol.io/introduction).
