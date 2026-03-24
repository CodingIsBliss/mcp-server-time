# MCP Server – Time ⏰

A **Model Context Protocol (MCP)** server that provides timezone-aware time
tools via the **streamable-http** transport.

Uses only the Python standard library (`zoneinfo`) — no extra API keys or
third-party services required.

Built with [FastMCP](https://github.com/modelcontextprotocol/python-sdk).

## Quick Start

```bash
# Install
pip install -e .

# Run (streamable-http on port 8000)
mcp-server-time
```

The server listens on `http://0.0.0.0:8000/mcp` by default.

## Available Tools

| Tool               | Description                                        |
|--------------------|----------------------------------------------------|
| `get_current_time` | Current date & time in any IANA timezone           |
| `convert_time`     | Convert a datetime between two timezones           |
| `time_difference`  | Offset difference between two timezones            |
| `list_timezones`   | List all IANA timezones, optionally filtered        |

## Environment Variable Overrides

| Variable        | Default              |
|-----------------|----------------------|
| `MCP_TRANSPORT` | `streamable-http`    |
| `MCP_HOST`      | `0.0.0.0`           |
| `MCP_PORT`      | `8000`              |

## License

MIT
