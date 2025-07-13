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
            "As at date\tSubsidised CCS - CCSP (No. of applicants)\tSubsidised CCS - CCSP (Average waiting time in months)\n"
            "31-12-19\t1000\t12\n"
        )

        with patch("requests.get") as mock_requests_get:
            mock_response = MagicMock()
            mock_response.content = mock_csv_data.encode("utf-16-le")
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
                "As at date\tSubsidised CCS - CCSP (No. of applicants)\tSubsidised CCS - CCSP (Average waiting time in months)\n"
                "31-12-19\t1000\t12\n"
                "31-12-20\t1100\t13\n"
            )
            mock_response.content = mock_csv_data_partial.encode("utf-16-le")
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