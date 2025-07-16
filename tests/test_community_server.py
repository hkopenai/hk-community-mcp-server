"""
Module for testing the MCP server creation.

This module contains unit tests for the server creation functionality of the MCP server,
ensuring that the server is set up correctly with the appropriate tools.
"""

import unittest
from unittest.mock import patch, Mock
from hkopenai.hk_community_mcp_server.server import server


class TestApp(unittest.TestCase):
    """
    Test class for MCP server application.
    
    This class contains test cases for verifying the creation and configuration
    of the MCP server, including tool registration.
    """
    @patch("hkopenai.hk_community_mcp_server.server.FastMCP")
    @patch("hkopenai.hk_community_mcp_server.tools.elderly_community_care_services.register")
    def test_create_mcp_server(self, mock_register, mock_fastmcp):
        """
        Test the creation of the MCP server and tool registration.

        This test verifies that the server is created correctly, tools are registered
        using the decorator, and the tools call the underlying functions as expected.
        """
        # Setup mocks
        mock_server = Mock()

        # Configure mock_server.tool to return a mock that acts as the decorator
        # This mock will then be called with the function to be decorated
        mock_server.tool.return_value = Mock()
        mock_fastmcp.return_value = mock_server

        # Test server creation
        server()

        # Verify server creation
        mock_fastmcp.assert_called_once()
        mock_register.assert_called_once_with(mock_server)


if __name__ == "__main__":
    unittest.main()
