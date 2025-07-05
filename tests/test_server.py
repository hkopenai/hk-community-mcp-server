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
    @patch("hkopenai.hk_community_mcp_server.server.tool_elderly_wait_time_ccs")
    def test_create_mcp_server(self, mock_tool_elderly_wait_time_ccs, mock_fastmcp):
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

        # Configure mock_server.tool to return a mock that acts as the decorator
        # This mock will then be called with the function to be decorated
        mock_server.tool.return_value = Mock()
        mock_fastmcp.return_value = mock_server

        # Test server creation
        server = create_mcp_server()

        # Verify server creation
        mock_fastmcp.assert_called_once()
        self.assertEqual(server, mock_server)

        # Verify that the tool decorator was called for each tool function
        self.assertEqual(mock_server.tool.call_count, 1)

        # Get all decorated functions
        decorated_funcs = {
            call.args[0].__name__: call.args[0]
            for call in mock_server.tool.return_value.call_args_list
        }
        self.assertEqual(len(decorated_funcs), 1)

        # Call each decorated function and verify that the correct underlying function is called

        decorated_funcs["get_elderly_wait_time_ccs"](start_year=2020, end_year=2021)
        mock_tool_elderly_wait_time_ccs.fetch_elderly_wait_time_data.assert_called_once_with(
            2020, 2021
        )


if __name__ == "__main__":
    unittest.main()
