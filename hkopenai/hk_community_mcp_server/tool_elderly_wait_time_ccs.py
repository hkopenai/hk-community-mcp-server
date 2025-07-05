"""
Module for fetching elderly wait time data for community care services.

This module provides tools to retrieve data on the number of applicants and average
waiting times for subsidised community care services for the elderly in Hong Kong.
"""

import csv
import io
import requests
from typing import Dict, List, Any


def fetch_elderly_wait_time_data(
    start_year: int, end_year: int
) -> List[Dict[str, Any]]:
    """
    Fetch data on the number of applicants and average waiting time for subsidised community care services
    for the elderly in Hong Kong within the specified year range.

    Args:
        start_year (int): The starting year for the data range.
        end_year (int): The ending year for the data range.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing the filtered data for the specified year range.
    """
    url = "https://www.swd.gov.hk/datagovhk/elderly/statistics-on-waiting-list-and-waiting-time-for-ccs.csv"
    response = requests.get(url)
    response.raise_for_status()

    # The content is in UTF-16 LE encoding
    content = response.content.decode("utf-16-le")
    # Ensure consistent line endings by replacing \r\n with \n
    csv_file = io.StringIO(content)
    csv_reader = csv.DictReader(csv_file, delimiter="\t")

    # Filter data by year range and extract English content only, excluding "As at date"
    filtered_data = []
    for row in csv_reader:
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


def get_elderly_wait_time_ccs(start_year: int, end_year: int) -> List[Dict[str, Any]]:
    """
    MCP tool to get the number of applicants and average waiting time for subsidised community care services
    for the elderly in Hong Kong.

    Args:
        start_year: Start year for data range
        end_year: End year for data range

    Returns:
        List of dictionaries containing data on applicants and waiting times for the specified year range.
    """
    return fetch_elderly_wait_time_data(start_year, end_year)
