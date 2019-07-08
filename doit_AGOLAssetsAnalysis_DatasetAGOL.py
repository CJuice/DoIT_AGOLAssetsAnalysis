"""
Contains the DatasetAGOL class that is for storing dataset values as class attributes and for providing functionality
necessary to get/process the values.

NOTE: This was taken from the data freshness process.

Author: CJuice
Date: 20190702
Revisions:

"""

import json
import doit_AGOLAssetsAnalysis_Variables_AGOL as var

from doit_AGOLAssetsAnalysis_Utility import Utility


class DatasetAGOL:
    """
    Class for storing information on a arcgis online datasets and for processing values for output needs.
    """

    OWNER = 'owner:mdimapdatacatalog'
    RECORD_LIMIT = '100'  # When changed from 100 the return quantity doesn't actually change. Unsure why ineffective.
    SORT_FIELD = 'title'

    def __init__(self):
        """
        Class is only used for the static method but is primed for expansion per data freshness functionality.
        """
        pass

    @staticmethod
    def request_all_data_catalog_results() -> list:
        """
        Make web requests and accumulate records until no more are returned for the dataset of interest

        :return: returns a list of json/dicts for datasets
        """
        more_records_exist = True
        start_number = 0
        master_list_of_dicts = []

        while more_records_exist:
            data = {'q': DatasetAGOL.OWNER,
                    'num': DatasetAGOL.RECORD_LIMIT,
                    'start': start_number,
                    'sortField': DatasetAGOL.SORT_FIELD,
                    'f': 'json'
                    }
            response = Utility.request_POST(url=var.arcgis_data_catalog_url, data=data)
            try:
                resp_json = response.json()
            except json.JSONDecodeError as jse:
                print(f"JSONDecodeError after making post request to arcgis online. url={var.arcgis_data_catalog_url}, data={data} {jse}")
                exit()
            else:
                results = resp_json.get("results", {})
                start_number = resp_json.get("nextStart", None)
                master_list_of_dicts.extend(results)
                # print(f"Start Number: {start_number}")

            # AGOL nextStart equal to -1 must indicate end of records reached
            if start_number == -1:
                more_records_exist = False

        return master_list_of_dicts

