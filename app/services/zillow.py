"""
zillow.py - Implementation of Zillow queries.

Based on documentation available at: https://www.zillow.com/howto/api/GetSearchResults.htm

Copyright (c) 2020 by Thomas J. Daley, J.D. Licensed under BSD License.
"""
from datetime import datetime
import os
import requests
import xml.etree.ElementTree as ET
import xml

import util.util as UTIL

SEARCH_URL = "https://www.zillow.com/webservice/GetSearchResults.htm?zws-id={}&address={}&citystatezip={}"
SOURCE = "ZILLOW"


class Zillow(object):
    """
    Encapsulates an interface into PublicData's web site via Python.
    """

    def __init__(self):
        """
        Instance initializer.
        """
        key = 'ZILLOW_API_KEY'
        try:
            zws_id = UTIL.get_env(key)
            if zws_id is None:
                raise ValueError(f"Unable to retrieve '{key}' from configuration.")
        except ValueError as e:
            UTIL.logmessage(f"Unable to retrieve '{key}': {str(e)}")
            zws_id = None

        self.zws_id = zws_id

    def load_xml(self, url: str) -> (bool, str, object):
        """
        Load XML from a URL.

        Args:
            url (str): URL to load from.

        Returns:
            (bool, str, object): The *bool* indicates success or failure.
                                 The *str* provides a diagnostic message.
                                 The *object* is an ET tree, if successful otherwise NoneType.
        """
        try:
            # Retrieve response from server
            response = requests.get(url, allow_redirects=False)

            # Convert response from stream of bytes to string
            content = response.content.decode()

            # Deserialize response to XML element tree
            tree = ET.ElementTree(ET.fromstring(content))

            # See if we got an error response.
            root = tree.getroot()
            return_code = root.find("./message/code").text
            if return_code != "0":
                message = root.find("./message/text").text
                return (False, message, tree)

            # All looks ok from a 30,000-foot level.
            # Return response to our caller.
            return (True, "OK", tree)
        except xml.etree.ElementTree.ParseError as e:
            UTIL.logmessage(f"Error parsing XML: {str(e)}")
            UTIL.logmessage(f"Failed XML: {content}")
            return (False, str(e), None)
        except Exception as e:
            UTIL.logmessage(f"Error reading cache or loading from URL: {str(e)}")
            UTIL.logmessage(f"Failed URL: {url}")
            return (False, str(e), None)

        return (False, "Programmer Error", None)

    def parse(self, tree) -> dict:
        """
        Parse an XML tree for a home value.

        Args:
            tree (xml.etree.ElementTree): XML from load_xml()
        Returns:
            (dict): Containing descriptive information on the property:
                * street
                * city
                * state
                * zip
                * latitude
                * longitude
                * details_link
                * comps_link
                * zbranding
                * value
        """
        root = tree.getroot()
        address = root.find("./response/results/result/address")
        street = address.find("street").text
        city = address.find("city").text
        state = address.find("state").text
        zip_code = address.find("zipcode").text
        latitide = address.find("latitude").text
        longitude = address.find("longitude").text
        zestimate = float(root.find("./response/results/result/zestimate/amount").text)
        details_link = root.find("./response/results/result/links/homedetails").text
        comps_link = root.find("./response/results/result/links/comparables").text
        zbranding = '<a href="{}">See more details for {} on Zillow.</a>'.format(details_link, street)
        zillow_info = {
            'street': street,
            'city': city,
            'state': state,
            'zip': zip_code,
            'latitude': latitide,
            'longitude': longitude,
            'details_link': details_link,
            'comps_link': comps_link,
            'zbranding': zbranding,
            'value': zestimate,
        }
        return zillow_info

    def search(self, street_address: str, city_state_zip: str) -> (bool, str, object):
        """
        Search Zillow for a house value

        Args:
            street_address (str): Street address of subject property
            city_state_zip (str): City, state, and ZIP of subject property

        Returns:
            (bool, str, object): The *bool* indicates success or failure.
                                 The *str* provides a diagnostic message.
                                 The *object* is an ET tree, if successful otherwise NoneType.
        """
        try:
            url = SEARCH_URL.format(self.zws_id, street_address, city_state_zip)
            (load_ok, message, xml_tree) = self.load_xml(url)
        except Exception as e:
            message = str(e)
            UTIL.logmessage(f"Error retrieving from {url}: {message}")
            return (False, message, None)

        try:
            zinfo = self.parse(xml_tree)
            return (True, 'OK', zinfo)
        except Exception as e:
            message = str(e)
            UTIL.logmessage(f"Error parsing XML: {message}")
        return (False, message, None)
