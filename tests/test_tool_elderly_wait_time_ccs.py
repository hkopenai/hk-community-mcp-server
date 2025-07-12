'''
Module for testing the elderly wait time CCS tool.

This module contains unit tests for fetching and filtering elderly wait time data.
'''

import unittest
from unittest.mock import patch, MagicMock

from hkopenai.hk_community_mcp_server.tool_elderly_wait_time_ccs import _get_elderly_community_care_services
from hkopenai.hk_community_mcp_server.tool_elderly_wait_time_ccs import register


class TestElderlyWaitTimeCCS(unittest.TestCase):
    '''
    Test class for verifying elderly wait time CCS functionality.

    This class contains test cases to ensure the data fetching and filtering
    for elderly wait time CCS work as expected.
    '''

    def test_get_elderly_community_care_services(self):
        '''
        Test the retrieval and filtering of elderly community care services data.

        This test verifies that the function correctly filters data by year range,
        returns empty results for non-matching years, and handles partial year matches.
        '''
        mock_csv_data = (
            b"\xff\xfe"  # UTF-16 LE BOM
            b"A\x00s\x00 \x00a\x00t\x00 \x00d\x00a\x00t\x00e\x00\tS\x00u\x00b\x00s\x00i\x00d\x00i\x00s\x00e\x00d\x00 \x00C\x00C\x00S\x00 \x00-\x00 \x00C\x00C\x00S\x00P\x00 \x00(\\N\x00o\x00.\x00 \x00o\x00f\x00 \x00a\x00p\x00p\x00l\x00i\x00c\x00a\x00n\x00t\x00s\x00)\x00\tS\x00u\x00b\x00s\x00i\x00d\x00i\x00s\x00e\x00d\x00 \x00C\x00C\x00S\x00 \x00-\x00 \x00C\x00C\x00S\x00P\x00 \x00(\\A\x00v\x00e\x00r\x00a\x00g\x00e\x00 \x00w\x00a\x00i\x00t\x00i\x00n\x00g\x00 \x00t\x00i\x00m\x00e\x00 \x00i\x00n\x00 \x00m\x00o\x00n\x00t\x00h\x00s\x00)\x00\r\x00\n\x00" # Header
            b"3\x001\x00-\x001\x002\x00-\x001\x009\x00\t1\x000\x000\x00\t1\x002\x00\r\x00\n\x00"
        )

        with patch("requests.get") as mock_requests_get:
            mock_response = MagicMock()
            mock_response.content = mock_csv_data
            mock_response.raise_for_status.return_value = None
            mock_requests_get.return_value = mock_response

            # Test filtering by year range
            result = _get_elderly_community_care_services(2019, 2019)
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]["date"], "31-12-19")

            # Test empty result for non-matching years
            result = _get_elderly_community_care_services(2022, 2023)
            self.assertEqual(len(result), 0)

            # Test partial year match
            mock_csv_data_partial = (
                b"\xff\xfe"  # UTF-16 LE BOM
                b"A\x00s\x00 \x00a\x00t\x00 \x00d\x00a\x00t\x00e\x00\tS\x00u\x00b\x00s\x00i\x00d\x00i\x00s\x00e\x00d\x00 \x00C\x00C\x00S\x00 \x00-\x00 \x00C\x00C\x00S\x00P\x00 \x00(\x00N\x00o\x00.\x00 \x00o\x00f\x00 \x00a\x00p\x00p\x00l\x00i\x00c\x00a\x00n\x00t\x00s\x00)\x00\tS\x00u\x00b\x00s\x00i\x00d\x00i\x00s\x00e\x00d\x00 \x00C\x00C\x00S\x00 \x00-\x00 \x00C\x00C\x00S\x00P\x00 \x00(\x00A\x00v\x00e\x00r\x00a\x00g\x00e\x00 \x00w\x00a\x00i\x00t\x00i\x00n\x00g\x00 \x00t\x00i\x00m\x00e\x00 \x00i\x00n\x00 \x00m\x00o\x00n\x00t\x00h\x00s\x00)\x00\r\x00\n\x00" # Header
                b"3\x001\x00-\x001\x002\x00-\x001\x009\x00\t1\x000\x000\x00\t1\x002\x00\r\x00\n\x00"
                b"3\x001\x00-\x001\x002\x00-\x002\x000\x00\t1\x001\x000\x00\t1\x003\x00\r\x00\n\x00"
            )
            mock_response.content = mock_csv_data_partial
            mock_requests_get.return_value = mock_response
            result = _get_elderly_community_care_services(2019, 2020)
            self.assertEqual(len(result), 2)

    def test_register_tool(self):
        '''
        Test the registration of the get_elderly_community_care_services tool.

        This test verifies that the register function correctly registers the tool
        with the FastMCP server and that the registered tool calls the underlying
        _get_elderly_community_care_services function.
        '''
        mock_mcp = MagicMock()

        # Call the register function
        register(mock_mcp)

        # Verify that mcp.tool was called with the correct description
        mock_mcp.tool.assert_called_once_with(
            description="Retrieve data on the number of applicants and average waiting time for subsidised community care services for the elderly in Hong Kong."
        )

        # Get the mock that represents the decorator returned by mcp.tool
        mock_decorator = mock_mcp.tool.return_value

        # Verify that the mock decorator was called once (i.e., the function was decorated)
        mock_decorator.assert_called_once()

        # The decorated function is the first argument of the first call to the mock_decorator
        decorated_function = mock_decorator.call_args[0][0]

        # Verify the name of the decorated function
        self.assertEqual(decorated_function.__name__, "get_elderly_community_care_services")

        # Call the decorated function and verify it calls _get_elderly_community_care_services
        with patch(
            "hkopenai.hk_community_mcp_server.tool_elderly_wait_time_ccs._get_elderly_community_care_services"
        ) as mock_get_elderly_community_care_services:
            decorated_function(start_year=2018, end_year=2019)
            mock_get_elderly_community_care_services.assert_called_once_with(2018, 2019)