"""
Module for configuring and running the HK Community MCP Server.

This module provides functionality to create and start the MCP server, which offers
various tools for accessing data related to the Hong Kong community.
"""

import argparse
from fastmcp import FastMCP
from hkopenai.hk_community_mcp_server import tool_elderly_wait_time_ccs
from typing import Dict, List, Annotated, Optional
from pydantic import Field


def create_mcp_server():
    """Create and configure the MCP server"""
    mcp = FastMCP(name="HK OpenAI community Server")

    @mcp.tool(
        description="Retrieve data on the number of applicants and average waiting time for subsidised community care services for the elderly in Hong Kong."
    )
    def get_elderly_wait_time_ccs(start_year: int, end_year: int) -> List[Dict]:
        return tool_elderly_wait_time_ccs.fetch_elderly_wait_time_data(
            start_year, end_year
        )

    return mcp


def main():
    """
    Main function to start the MCP Server.
    
    Parses command line arguments to determine the mode of operation (SSE or stdio)
    and starts the server accordingly.
    """
    parser = argparse.ArgumentParser(description="HKO MCP Server")
    parser.add_argument(
        "-s", "--sse", action="store_true", help="Run in SSE mode instead of stdio"
    )
    parser.add_argument(
        "--host", type=str, default="127.0.0.1", help="Host to bind the server to"
    )
    args = parser.parse_args()

    server = create_mcp_server()

    if args.sse:
        server.run(transport="streamable-http", host=args.host)
        print(f"MCP Server running in SSE mode on port 8000, bound to {args.host}")
    else:
        server.run()
        print("MCP Server running in stdio mode")


if __name__ == "__main__":
    main()
