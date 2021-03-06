"""
fred.py - Interface into the St. Louis Federal Reserve Bank's FRED API.

API documented at:
https://research.stlouisfed.org/docs/api/

https://api.stlouisfed.org/fred/series/observations?series_id=MORTGAGE30US&api_key=254f68a559b3068a1554a89f6d7e2435&observation_start=2019-01-01&observation_end=2019-12-31&file_type=json&frequency=m&aggregation_method=avg

Copyright (c) 2019 by Thomas J. Daley. All Rights Reserved.
"""
from decimal import Decimal
import json
import requests

import util.util as UTIL

BASEURL = {}
BASEURL["SERIES_SEARCH"] = "https://api.stlouisfed.org/fred/series/search?"
BASEURL["SERIES_OBSERVATIONS"] = "https://api.stlouisfed.org/fred/series/observations?"
BASEURL["CATEGORY"] = "https://api.stlouisfed.org/fred/category?"
BASEURL["CATEGORY_CHILDREN"] = "https://api.stlouisfed.org/fred/category/children?"
BASEURL["CATEGORY_SERIES"] = "https://api.stlouisfed.org/fred/category/series?"

SOURCE = "FRED"


class Fred(object):
    """
    Encapsulates an interface into the St. Louis Federal Reserve Bank's FRED time series
    databases.
    """

    def __init__(self):
        """
        Instance initializer.
        """
        key = 'FRED_API_KEY'
        try:
            self.api_key = UTIL.get_env(key)
            if self.api_key is None:
                raise ValueError(f"Unable to retrieve '{key}' from configuration.")
        except ValueError as e:
            UTIL.logmessage(f"Unable to retrieve '{key}': {str(e)}")
            self.api_key = None

    def make_url(self, url_name: str, **params: dict) -> str:
        """
        Construct a URL for querying the FRED servers.
        """
        url = BASEURL[url_name]
        args = []
        for arg, value in params.items():
            args.append("{}={}".format(arg, value))
        url = url + "&".join(args)

        # Allow caller to override our API key.
        if "api_key" not in args:
            url += "&api_key=" + self.api_key

        return url

    def retrieve(self, url_name: str, **params: dict):
        """
        Retrieve data from FRED servers.
        """
        response = requests.get(self.make_url(url_name, **params))
        result = response.content.decode()
        return result

    def series_observations(self, series_id: str, **kwargs):
        """
        Get observations from a series.

        See: https://research.stlouisfed.org/docs/api/fred/series_observations.html

        Args:
            series_id (str): Series ID, e.g. MORTGAGE30US
            **kwargs can be any argument identified on the FRED api page referenced above.

        Returns:
            The dataset requested.
        """
        kwargs["series_id"] = series_id.upper()
        result = self.retrieve("SERIES_OBSERVATIONS", **kwargs)
        return result

    def category(self, category_id: int = 0, **kwargs):
        """
        Get a category description.
        """
        kwargs["category_id"] = str(category_id)
        url = self.make_url("CATEGORY", **kwargs)
        print(url)

    def category_children(self, category_id: int = 0, **kwargs):
        """
        Get a list of child categories.
        """
        kwargs["category_id"] = str(category_id)
        url = self.make_url("CATEGORY_CHILDREN", **kwargs)
        print(url)

    def category_series(self, category_id: int = 0, **kwargs):
        """
        Get a list of series for a category.
        """
        kwargs["category_id"] = str(category_id)
        url = self.make_url("CATEGORY_SERIES", **kwargs)
        print(url)

    def series_search(self, search_text: str, **kwargs):
        """
        Get a list of series for a category.
        """
        kwargs["search_text"] = str(search_text)
        url = self.make_url("SERIES_SEARCH", **kwargs)
        print(url)


class FredUtil(object):
    """
    Higher-level interface into Fred that computes frequently used values.
    """

    def __init__(self):
        self.fred = Fred()

    def average_fixed_mortgage(self, year: int, month: int = 0, duration: int = 30) -> Decimal:
        """
        Get the average mortage interest rate for the requested period.

        Args:
            year (int): Year being queried. [REQUIRED]
            month (int): Month being queried. If omitted, the average is for
            the entire year. [1-12]
            duration (int): Term of mortgage loan in years. [5, 15, 30]

        Returns:
            (Decimal): Average mortgage interest rate for the period, or None
            if not found.
        """
        i_year = int(year)
        i_month = int(month)
        i_duration = int(duration)

        if i_duration not in [5, 15, 30]:
            raise ValueError(f"duration must be one of 5, 15, or 30, not '{duration}''")

        if i_month < 0 or i_month > 12:
            raise ValueError(
                "month must be in the range 1-12 (inclusive) or omitted, not '{month}'")

        if i_month == 0:
            observation_start = f"{year}-01-01"
            observation_end = f"{year}-12-31"
            frequency = "a"  # Annual
        else:
            # Figure out last day of the month, accounting for leap-years
            # (during my lifetime)
            last_day = [31, 28, 31, 30, 31, 30,
                        31, 31, 30, 31, 30, 31][i_month - 1]
            if i_year % 4 == 0 and i_month == 2:
                last_day = 29

            # FRED requires zero-padded values, e.g. "02" not "2"
            padded_month = f"0{month}"[-2:]
            padded_day = f"0{last_day}"[-2:]

            # Construct start and end dates
            observation_start = f"{year}-{padded_month}-01"
            observation_end = f"{year}-{padded_month}-{padded_day}"
            frequency = "m"  # Monthly

        params = {
            "observation_start": observation_start,
            "observation_end": observation_end,
            "frequency": frequency,
            "aggregation_method": "avg",
            "file_type": "json"
        }

        # Retrieve data.
        result = self.fred.series_observations(
            f"MORTGAGE{duration}US", **params)
        result = json.loads(result)
        rate = result["observations"][0]["value"]
        rate = Decimal(Decimal(rate)/100)
        return rate


if __name__ == "__main__":
    futil = FredUtil()
    print("-" * 40)
    print("Average 5 year mortgage rate in Feb 2018:", futil.average_fixed_mortgage(2018, 2, 5))
    print("-" * 40)
