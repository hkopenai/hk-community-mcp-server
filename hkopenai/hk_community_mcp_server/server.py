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
        return tool_elderly_wait_time_ccs.fetch_elderly_wait_time_data(start_year, end_year)

    return mcp
def main():
    parser = argparse.ArgumentParser(description='HKO MCP Server')
    parser.add_argument('-s', '--sse', action='store_true',
                       help='Run in SSE mode instead of stdio')
    args = parser.parse_args()

    server = create_mcp_server()
    
    if args.sse:
        server.run(transport="streamable-http")
        print("HKO MCP Server running in SSE mode on port 8000")
    else:
        server.run()
        print("HKO MCP Server running in stdio mode")

if __name__ == "__main__":
    main()
