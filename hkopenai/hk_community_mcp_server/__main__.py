"""
Module for launching the HK Community MCP Server.

This module serves as the entry point for starting the MCP server, which provides
various tools and resources for the Hong Kong community.
"""

from hkopenai_common.cli_utils import cli_main
from .server import server

if __name__ == "__main__":
    cli_main(server, "HK Community MCP Server")
