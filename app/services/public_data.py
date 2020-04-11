"""
public_data.py - Implementation of PublicData queries.

Based on documentation available at: http://www.publicdata.com/pdapidocs/pdsearchdocs.php

Copyright (c) 2020 by Thomas J. Daley, J.D. Licensed under BSD License.
"""
from datetime import datetime
import os
import redis
import requests
import xml.etree.ElementTree as ET
import xml

import util.util as UTIL

SEARCH_URL = 'http://lbsearch.publicdata.com/pdsearch.php'
TAX_SEARCH_PARTS = [
    'p1={street} {city}',
    'matchany=all',
    'input=grp_cad_{state.lower()}_advanced_main',
    'type=advanced',
    'dlnumber={api_key}'
    'dlstate=UID',
    'id=',
    'identifier=',
    'sessionid={session_id}',
    'o=grp_cad_advanced_main',
    'disp=XML',
]
TAX_SEARCH_URL = '{}?{}'.format(SEARCH_URL, '&'.join(TAX_SEARCH_PARTS))

DETAILS_URL = 'http://lbsearch.publicdata.com/pddetails.php'
PROP_DETAILS_PARTS = [
    'db={db}',
    'rec={rec}',
    'ed={edition}',
    'dlnumber={api_key}',
    'dlstate=UID',
    'id=',
    'identifier=',
    'sessionid={session_id}',
    'disp=XML',
]
PROP_DETAILS_URL = '{}?{}'.format(DETAILS_URL, '&'.join(PROP_DETAILS_PARTS))

LOGIN_URL = 'https://login.publicdata.com/pdmain.php/logon/checkAccess?disp=XML&login_id={api_key}&password={password}'

SOURCE = "PUBLICDATA"


class PDTaxRecords(object):
    """
    Encapsulates an interface into PublicData's tax records API.
    """

    def __init__(self):
        """
        Instance initializer.
        """
        key = 'PUBLIC_DATA_API_KEY'
        try:
            api_key = UTIL.get_env(key)
            if api_key is None:
                raise ValueError(f"Unable to retrieve '{key}' from configuration.")
        except ValueError as e:
            UTIL.logmessage(f"Unable to retrieve '{key}': {str(e)}")
            api_key = None

        key = 'PUBLIC_DATA_API_PASSWORD'
        try:
            api_password = UTIL.get_env(key)
            if api_password is None:
                raise ValueError(f"Unable to retrieve '{key}' from configuration.")
        except ValueError as e:
            UTIL.logmessage(f"Unable to retrieve '{key}': {str(e)}")
            api_password = None

        self.api_key = api_key
        self.api_password = api_password
        self.redis = redis_connection()

    def login(self) -> str:
        """
        Get today's session code. Checks for a cached session code with today's
        date as the file name. If no file found, then perform a login and cache
        the session code.

        Args:
            None.
        Returns:
            (str): Today's session code.
        """
        key = f'{SOURCE}-SESSIONKEY-{today_yyyymmdd()}'
        session_key = self.redis.get(key)
        if session_key is not None:
            return session_key

        # Here to perform a login because we have no day key for today's date.
        url = LOGIN_URL.format(api_key=self.api_key, password=self.api_password)
        tree = self.load_xml(url)

        session_key = session_key(tree)
        self.redis.setex(key, 60*60*24, session_key)
        return session_key

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
            if root.get("type").lower() == "error":
                message = error_message(root)
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

    def parse_search(self, tree) -> dict:
        """
        Parse an XML tree from a property search.

        Args:
            tree (xml.etree.ElementTree): XML from load_xml()
        Returns:
            (dict): Containing descriptive information on the property:
                * street
                * city
                * state
                * zip
                * county
                * assessed_value
                * market_value
        """
        root = tree.getroot()
        address = root.find("./response/results/result/address")
        street = address.find("street").text
        city = address.find("city").text
        state = address.find("state").text
        zip_code = address.find("zipcode").text
        latitide = address.find("latitude").text
        longitude = address.find("longitude").text
        try:
            zestimate = float(root.find("./response/results/result/zestimate/amount").text)
        except Exception:
            zestimate = float(0.0)
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

    def search(self, street_address: str, city: str, state: str) -> (bool, str, object):
        """
        Search PublicData for a list of houses that match this address.

        Args:
            street_address (str): Street address of subject property
            city (str): City in which the property is located
            state (str): State in which the property is located (two-character code, e.g. 'TX')

        Returns:
            (bool, str, object): The *bool* indicates success or failure.
                                 The *str* provides a diagnostic message.
                                 The *object* is an ET tree, if successful otherwise NoneType.
        """
        session_id = self.login()
        try:
            url = TAX_SEARCH_URL.format(
                street=street_address,
                city=city,
                state=state,
                api_key=self.api_key,
                session_id=session_id
            )
            (load_ok, message, xml_tree) = self.load_xml(url)
        except Exception as e:
            message = str(e)
            UTIL.logmessage(f"Error retrieving from {url}: {message}")
            return None

        try:
            zinfo = self.parse_search(xml_tree)
            return zinfo
        except Exception as e:
            message = str(e)
            UTIL.logmessage(f"Error parsing XML: {message}")
        return None


def redis_connection():
    """
    Return a connection to our Redis service.
    """
    return redis.Redis(
        host=UTIL.get_env('REDIS_HOST', 'localhost'),
        port=int(UTIL.get_env('REDIS_PORT', 6379)),
        db=0
    )


def today_yyyymmdd() -> str:
    """
    Get the current date in YYYYMMDD format.
    Args:
        None.
    Returns:
        (str): Today's date in YYYYMMDD format.
    """
    return datetime.now().strftime("%Y%m%d")


def session_key(tree) -> str:
    """
    Find the session key in an XML tree.

    Args:
        tree (XML Tree): XML Tree retrieved from login url.
    Returns:
        (str): Today's API key or NoneType on failure.
    """
    root = tree.getroot()
    child = root.find('user')
    sid = child.find('id').text

    # Check for errors
    if sid is None:
        child = root.find('pdheaders')
        message = child.find('pdheader1').text
        raise Exception(f"PublicData login failure: {message}")

    # We had a successful login
    session_id = child.find('sessionid').text
    return session_id


def error_message(root) -> str:
    """
    Find an error message in XML that has indicated an error.
    Unfortunately, the error message is not in the same place, depending on
    the error. Here we have a list of paths to search for and we go through
    them until we find a message or run out of places to look.
    Args:
        root (xml.etree.ElementTree): Root node of an element tree
    Returns:
        (str): Error message
        (NoneType): Indicates we didn't find a message.
    """

    # Paths we will search. We search in the order in which the path
    # appears in the *paths* list, so insert them in the order you want
    # them searched.
    #
    # I do not understand why find() fails and findall() works.
    # tjd 07/16/2019
    paths = ["message", "./pdheaders/pdheader1"]
    message = None
    for path in paths:
        message_node = root.findall(path)
        if message_node:
            message = message_node[0].text
            break

    return message
