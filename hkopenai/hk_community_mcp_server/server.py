"""
Module for configuring and running the HK Community MCP Server.

This module provides functionality to create and start the MCP server, which offers
various tools for accessing data related to the Hong Kong community.
"""

from fastmcp import FastMCP

from hkopenai.hk_community_mcp_server.tools import elderly_community_care_services


def server():
    """Create and configure the MCP server"""
    mcp = FastMCP(name="HK OpenAI community Server")

    elderly_community_care_services.register(mcp)

    return mcp