"""
Module for testing the MCP server creation.

This module contains unit tests for the server creation functionality of the MCP server,
ensuring that the server is set up correctly with the appropriate tools.
"""

import unittest
from unittest.mock import patch, Mock
from hkopenai.hk_community_mcp_server.server import create_mcp_server


class TestApp(unittest.TestCase):
    """
    Test class for MCP server application.
    
    This class contains test cases for verifying the creation and configuration
    of the MCP server, including tool registration.
    """
    @patch("hkopenai.hk_community_mcp_server.server.FastMCP")
    @patch("hkopenai.hk_community_mcp_server.tool_elderly_wait_time_ccs.register")
    def test_create_mcp_server(self, mock_register, mock_fastmcp):
        """
        Test the creation of the MCP server.
        
        Args:
            mock_tool_elderly_wait_time_ccs: Mock object for the elderly wait time tool.
            mock_fastmcp: Mock object for the FastMCP class.
            
        Verifies that the server is created correctly and that tools are registered
        as expected.
        """
        # Setup mocks
        mock_server = Mock()
        mock_fastmcp.return_value = mock_server

        # Test server creation
        create_mcp_server()

        # Verify server creation
        mock_fastmcp.assert_called_once()
        mock_register.assert_called_once_with(mock_server)
        mock_tool_elderly_wait_time_ccs.fetch_elderly_wait_time_data.assert_called_once_with(
            2020, 2021
        )


if __name__ == "__main__":
    unittest.main()
