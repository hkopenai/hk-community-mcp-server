"""
Module for fetching elderly wait time data for community care services.

This module provides tools to retrieve data on the number of applicants and average
waiting times for subsidised community care services for the elderly in Hong Kong.
"""

from typing import Any, Dict, List
from hkopenai_common.csv_utils import fetch_csv_from_url
from pydantic import Field
from typing_extensions import Annotated


def register(mcp):
    """Registers the elderly wait time CCS tool with the FastMCP server."""

    @mcp.tool(
        description="Retrieve data on the number of applicants and average waiting time for subsidised community care services for the elderly in Hong Kong."
    )
    def get_elderly_community_care_services(
        start_year: Annotated[int, Field(description="Start year for data range")],
        end_year: Annotated[int, Field(description="End year for data range")],
    ) -> List[Dict[str, Any]]:
        return _get_elderly_community_care_services(start_year, end_year)


def _get_elderly_community_care_services(
    start_year: Annotated[int, Field(description="Start year for data range")],
    end_year: Annotated[int, Field(description="End year for data range")],
) -> List[Dict[str, Any]]:
    """
    MCP tool to get the number of applicants and average waiting time for subsidised community care services
    for the elderly in Hong Kong.

    Args:
        start_year: Start year for data range
        end_year: End year for data range

    Returns:
        List of dictionaries containing data on applicants and waiting times for the specified year range.
    """
    url = "https://www.swd.gov.hk/datagovhk/elderly/statistics-on-waiting-list-and-waiting-time-for-ccs.csv"
    data = fetch_csv_from_url(url, encoding="utf-16-le", delimiter="\t")

    # Filter data by year range and extract English content only, excluding "As at date"
    filtered_data = []
    for row in data:
        date_str = row.get("As at date", "")
        year_str = date_str.split("-")[-1]
        try:
            year = int(year_str)
            # Convert 2-digit year to 4-digit year (assuming years < 100 are in 2000s)
            if year < 100:
                year += 2000
            if start_year <= year <= end_year:
                # Filter to include only English columns and exclude "As at date"
                english_data = {
                    key: value
                    for key, value in row.items()
                    if key.strip().startswith("Subsidised CCS")
                    or key.strip().startswith("No. of applicants")
                    or key.strip().startswith("Waiting time")
                    or key.strip().startswith("No. of elderly persons classified")
                }
                filtered_data.append({"date": date_str, "data": english_data})
        except ValueError as e:
            filtered_data.append(
                {
                    "error": f"Invalid year format: {year_str}, error: {str(e)}",
                    "date": date_str,
                    "row": row,
                }
            )

    return filtered_data
