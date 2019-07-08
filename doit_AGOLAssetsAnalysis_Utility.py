"""
A class of static utility methods
Author: CJuice
Date: 20190702
Modifications:

"""

import requests
import time


class Utility:
    """
    Class of utility static methods for use in processing.
    """

    @staticmethod
    def request_GET(url: str, params: dict = None) -> requests.models.Response:
        """
        Make a GET request to a web resource and return response.
        :param url: the url to which to make the request
        :param params: params to pass in the request
        :return:
        """
        if params is None:
            params = {}

        try:
            response = requests.get(url=url, params=params)
        except Exception as e:
            print(f"Error with request to {url}. Error:{e}")
            return requests.models.Response()
        else:
            return response

    @staticmethod
    def request_POST(url: str, data: dict = None, verify: bool = False) -> requests.models.Response:
        """
        Make a POST request for a web resource and return response
        :param url: the url to which to make the request
        :param data: data to be passed in request
        :param verify:
        :return:
        """
        if data is None:
            data = {}

        try:
            response = requests.post(url=url, data=data, verify=verify)
        except Exception as e:
            # TODO: Refine exception handling
            print(f"Error during post request to url:{url}, data:{data}: {e}")
            exit()
        else:
            return response

    @staticmethod
    def calculate_time_taken(start_time: float) -> float:
        """
        Calculate the time difference between now and the value passed as the start time

        :param start_time: Time value representing start of processing
        :return: Difference value between start time and current time
        """
        return time.time() - start_time
