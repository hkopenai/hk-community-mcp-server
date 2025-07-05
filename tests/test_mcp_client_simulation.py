"""
Module for testing MCP client simulation.

This module contains unit tests for simulating interactions with an MCP server
using HTTP communication. It tests the functionality of various tools provided
by the MCP server.
"""

import unittest
import subprocess
import json
import sys
import os
import time
import asyncio
import socket
import logging
from datetime import datetime, timedelta
from mcp.client.streamable_http import streamablehttp_client
from mcp import ClientSession

# Configure logging
log_level = os.environ.get("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=getattr(logging, log_level),
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@unittest.skipUnless(
    os.environ.get("RUN_LIVE_TESTS") == "true",
    "Set RUN_LIVE_TESTS=true to run live tests",
)
class TestMCPClientSimulation(unittest.TestCase):
    """
    Test class for MCP client simulation.
    
    This class contains test cases for simulating client interactions with an MCP server
    over HTTP, ensuring that tools and communication function as expected.
    """
    server_process = None
    SERVER_URL = "http://127.0.0.1:8000/mcp/"  # Updated server URL for MCP API

    # Need a fresh mcp server to avoid lock up
    def setUp(self):
        """
        Set up the test environment before each test.
        
        Starts an MCP server subprocess for HTTP communication, ensuring it's listening
        on the specified port before proceeding.
        """
        logger.debug("Starting MCP server subprocess for HTTP communication...")
        # Start the MCP server as a subprocess. It should expose an HTTP endpoint.
        self.server_process = subprocess.Popen(
            [sys.executable, "-m", "hkopenai.hk_community_mcp_server", "--sse"],
            # No stdin/stdout/stderr pipes needed for HTTP communication, but keep for server logs
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        logger.debug(
            "MCP server subprocess started. Giving it a moment to start up and listen on HTTP..."
        )
        # Give the server a moment to start up and listen on the port
        time.sleep(5)  # Increased sleep time for server to fully initialize HTTP server

        # Check if the server is actually listening on the port
        for _ in range(10):
            try:
                with socket.create_connection(("127.0.0.1", 8000), timeout=1):
                    logger.debug("Server is listening on port 8000.")
                    break
            except OSError as e:
                logger.debug(f"Waiting for server to start: {e}")
                time.sleep(1)
        else:
            self.server_process.terminate()
            self.server_process.wait(timeout=5)
            if self.server_process.poll() is None:
                self.server_process.kill()
            raise Exception("Server did not start listening on port 8000 in time.")

        logger.debug(f"Server setup complete.")

    def tearDown(self):
        """
        Clean up after each test.
        
        Terminates the MCP server subprocess and ensures all resources are released.
        """
        # Terminate the server process
        if self.server_process:
            self.server_process.terminate()
            self.server_process.wait(timeout=5)
            if self.server_process.poll() is None:
                logger.debug("Tear down complete.")
                self.server_process.kill()

            # Print any remaining stderr output from the server process
            if self.server_process.stdout:
                self.server_process.stdout.close()
            if self.server_process.stderr:
                stderr_output = self.server_process.stderr.read()
                if stderr_output:
                    logger.debug(f"Server stderr (remaining):\n{stderr_output}")
                else:
                    logger.debug("Server stderr (remaining): (empty)")
                self.server_process.stderr.close()
            logger.info("Tear down complete.")

    async def _call_tool_and_assert(self, tool_name, params):
        """
        Call a tool on the MCP server and assert the response.
        
        Args:
            tool_name (str): The name of the tool to call.
            params (dict): Parameters to pass to the tool.
            
        Returns:
            dict or list: The response data from the tool call.
        """
        async with streamablehttp_client(self.SERVER_URL) as (
            read_stream,
            write_stream,
            _,
        ):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                response = await session.call_tool(tool_name, params)
                logger.info(f"'{tool_name}' tool response: {str(response)[:500]}...")

                json_text = response.content[0].text if response.content else "{}"
                data = json.loads(json_text)
                self.assertIsInstance(
                    data,
                    (dict, list),
                    f"Result for {tool_name} should be a dictionary or list",
                )
                if isinstance(data, dict):
                    self.assertNotIn(
                        "error",
                        data,
                        f"Result for {tool_name} should not contain an error: {data.get('error')}",
                    )
                elif isinstance(data, list) and data and isinstance(data[0], dict):
                    self.assertNotIn(
                        "error",
                        data[0],
                        f"Result for {tool_name} should not contain an error: {data[0].get('error')}",
                    )
                return data

    def test_get_elderly_wait_time_ccs_tool(self):
        """
        Test the 'get_elderly_wait_time_ccs' tool.
        
        Ensures the tool returns valid data for the specified year range.
        """
        logger.debug("Testing 'get_elderly_wait_time_ccs' tool...")
        asyncio.run(
            self._call_tool_and_assert(
                "get_elderly_wait_time_ccs", {"start_year": 2019, "end_year": 2020}
            )
        )
