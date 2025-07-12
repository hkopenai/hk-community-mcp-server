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

    tool_elderly_wait_time_ccs.register(mcp)

    return mcp


def main(args):
    """
    Main function to run the MCP Server.

    Args:
        args: Command line arguments passed to the function.
    """
    server = create_mcp_server()

    if args.sse:
        server.run(transport="streamable-http", host=args.host, port=args.port)
        print(f"MCP Server running in SSE mode on port {args.port}, bound to {args.host}")
    else:
        server.run()
        print("MCP Server running in stdio mode")


if __name__ == "__main__":
    main()
