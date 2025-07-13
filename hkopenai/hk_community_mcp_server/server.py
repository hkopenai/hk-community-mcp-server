"""
Module for configuring and running the HK Community MCP Server.

This module provides functionality to create and start the MCP server, which offers
various tools for accessing data related to the Hong Kong community.
"""

from fastmcp import FastMCP

from hkopenai.hk_community_mcp_server import tool_elderly_wait_time_ccs


def create_mcp_server():
    """Create and configure the MCP server"""
    mcp = FastMCP(name="HK OpenAI community Server")

    tool_elderly_wait_time_ccs.register(mcp)

    return mcp


def main(host: str, port: int, sse: bool):
    """
    Main function to run the MCP Server.

    Args:
        args: Command line arguments passed to the function.
    """
    server = create_mcp_server()

    if sse:
        server.run(transport="streamable-http", host=host, port=port)
        print(f"MCP Server running in SSE mode on port {args.port}, bound to {args.host}")
    else:
        server.run()
        print("MCP Server running in stdio mode")


if __name__ == "__main__":
    main()
