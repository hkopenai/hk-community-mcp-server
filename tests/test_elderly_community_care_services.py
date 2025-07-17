"""
Module for testing the elderly community care services tool functionality.

This module contains unit tests for fetching and filtering elderly community care services data.
"""

import unittest
from unittest.mock import patch, MagicMock

from hkopenai.hk_community_mcp_server.tools.elderly_community_care_services import (
    _get_elderly_community_care_services,
    register,
)


class TestElderlyCommunityCareServices(unittest.TestCase):
    """
    Test class for verifying elderly community care services functionality.

    This class contains test cases to ensure the data fetching and filtering
    for elderly community care services work as expected.
    """

    def test_get_elderly_community_care_services(self):
        """
        Test the retrieval and filtering of elderly community care services data.

        This test verifies that the function correctly filters data by year range,
        returns empty results for non-matching years, and handles partial year matches.
        """
        # Mock the CSV data
        mock_csv_data = [
            {
                "As at date": "31-03-19",
                "Subsidised CCS (Total)": "100",
                "No. of applicants (Total)": "50",
                "Waiting time (Total)": "12",
            },
            {
                "As at date": "30-09-19",
                "Subsidised CCS (Total)": "110",
                "No. of applicants (Total)": "55",
                "Waiting time (Total)": "13",
            },
            {
                "As at date": "31-03-20",
                "Subsidised CCS (Total)": "120",
                "No. of applicants (Total)": "60",
                "Waiting time (Total)": "14",
            },
            {
                "As at date": "30-09-20",
                "Subsidised CCS (Total)": "130",
                "No. of applicants (Total)": "65",
                "Waiting time (Total)": "15",
            },
            {
                "As at date": "31-03-21",
                "Subsidised CCS (Total)": "140",
                "No. of applicants (Total)": "70",
                "Waiting time (Total)": "16",
            },
        ]

        with patch(
            "hkopenai.hk_community_mcp_server.tools.elderly_community_care_services.fetch_csv_from_url"
        ) as mock_fetch_csv_from_url:
            # Setup mock response for successful data fetching
            mock_fetch_csv_from_url.return_value = mock_csv_data

            # Test filtering by year range
            result = _get_elderly_community_care_services(2019, 2019)
            self.assertEqual(len(result), 2)
            self.assertEqual(result[0]["date"], "31-03-19")
            self.assertEqual(result[0]["data"]["Subsidised CCS (Total)"], "100")

            # Test empty result for non-matching years
            result = _get_elderly_community_care_services(2022, 2023)
            self.assertEqual(len(result), 0)

            # Test partial year match
            result = _get_elderly_community_care_services(2019, 2020)
            self.assertEqual(len(result), 4)

            # Test error handling when fetch_csv_from_url returns an error
            mock_fetch_csv_from_url.return_value = {"error": "CSV fetch failed"}
            result = _get_elderly_community_care_services(2019, 2019)
            self.assertEqual(result, {'error': 'CSV fetch failed'})

    def test_register_tool(self):
        """
        Test the registration of the get_elderly_community_care_services tool.

        This test verifies that the register function correctly registers the tool
        with the FastMCP server and that the registered tool calls the underlying
        _get_elderly_community_care_services function.
        """
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
            "hkopenai.hk_community_mcp_server.tools.elderly_community_care_services._get_elderly_community_care_services"
        ) as mock_get_elderly_community_care_services:
            decorated_function(start_year=2018, end_year=2019)
            mock_get_elderly_community_care_services.assert_called_once_with(2018, 2019)