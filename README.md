# Hong Kong Community Care Services MCP Server

[![GitHub Repository](https://img.shields.io/badge/GitHub-Repository-blue.svg)](https://github.com/hkopenai/hk-community-mcp-server)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This is an MCP server that provides access to government community and social welfare data through a FastMCP interface.

## Features

### Elderly Community Care Services
- Retrieve data on the number of applicants and average waiting time for subsidized community care services for the elderly in Hong Kong [url](https://data.gov.hk/en-data/dataset/hk-swd-elderly-statistics-on-waiting-list-and-waiting-time-for-ccs)

## Data Source

- Elderly community care services data from Social Welfare Department

## Examples

* Retrieve latest waiting time data subsidized community care services for elderly community care services in Hong Kong

## Setup

1. Clone this repository
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the server:
   ```bash
   python app.py
   ```

### Running Options

- Default stdio mode: `python app.py`
- SSE mode (port 8000): `python app.py --sse`

## Cline Integration

To connect this MCP server to Cline using stdio:

1. Add this configuration to your Cline MCP settings (cline_mcp_settings.json):
```json
{
  "hk-community": {
    "disabled": false,
    "timeout": 3,
    "type": "stdio",
    "command": "uvx",
    "args": [
      "hkopenai.hk-community-mcp-server"
    ]
  }
}
```

## Testing

Tests are available in the `tests/` directory. Run with:
```bash
pytest
```
