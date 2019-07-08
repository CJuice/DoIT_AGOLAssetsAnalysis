"""
File designated for process variables in order to centralize variables, and de-clutter main script.
Author: CJuice
Date: 20190702
Modifications:

"""
import os

# NOT DERIVED
_root_file_path = os.path.dirname(__file__)
arcgis_root_url = r"https://www.arcgis.com"
credentials_file = f"{_root_file_path}/Docs/md_doit_agol_credentials.cfg"

# DERIVED
arcgis_sharing_rest_url = f"{arcgis_root_url}/sharing/rest"
arcgis_data_catalog_url = f"{arcgis_sharing_rest_url}/search"  # Dependent so out of alphabetic order
