"""
Process for inspecting the inventory of assets in Maryland ArcGIS Online and providing analysis output.
Intended to be built on as we develop the analysis we want. A lot of the functionality has been borrowed from
the data freshness process and will diverge as needed.

Request all data catalog assets.
Get the “type” for each asset.
Get the unique “type” values and the number of times they occur
Establish connection with the AGOL assets inventory stats hosted table
Push the summary stats up to the table to update existing values to most current values

Author: CJuice
Date Created: 20190703
Revisions:

"""


def main():

    # IMPORTS
    import time
    start_time = time.time()
    print(f"Start Time: {start_time} seconds since Epoch")

    import configparser
    # import pandas as pd
    import requests
    import doit_AGOLAssetsAnalysis_Variables_AGOL as var

    from arcgis.gis import GIS
    from doit_AGOLAssetsAnalysis_Utility import Utility
    from doit_AGOLAssetsAnalysis_DatasetAGOL import DatasetAGOL

    # Disable the security warnings for https from data.maryland.gov
    requests.packages.urllib3.disable_warnings()

    print(f"\nImports Completed... {Utility.calculate_time_taken(start_time=start_time)} seconds since start")

    # VARIABLES
    parser = configparser.ConfigParser()
    parser.read(filenames=[var.credentials_file])
    agol_password = parser["AGOL"]["PASSWORD"]
    agol_root_url = parser["AGOL"]["ROOT_URL"]
    agol_username = parser["AGOL"]["USER_NAME"]
    agol_layer_id = parser["AGOL"]["LAYER_ID"]

    # FUNCTIONALITY
    # make a request to the data catalog and get the type value of each asset
    master_list_of_results = DatasetAGOL.request_all_data_catalog_results()
    type_list = []
    for item in master_list_of_results:
        type_ = item.get("type", None) if item is not None else None
        type_list.append(type_)

    # Print outs for general understanding of data.json level process
    print(f"Data Catalog Results Requests Process Completed... {Utility.calculate_time_taken(start_time=start_time)} seconds since start")
    print(f"RESULTS: {len(master_list_of_results)} ")

    # Need to get set of unique asset types, and perform summary on values
    counts_ser = pd.Series(data=type_list)
    value_counts = counts_ser.value_counts()  # Unique values and the number of times they occur
    total_number_of_assets_encountered = value_counts.sum()
    value_counts_dict = value_counts.to_dict()

    # Need the total number of assets encountered in the available values for display so add it to the dict
    value_counts_dict["TOTAL"] = total_number_of_assets_encountered

    # This portion requires the intepreter to be ESRI ArcGIS Pro python
    # Upserting results to hosted table

    # Need an agol connection session thingy
    gis = GIS(url=agol_root_url, username=agol_username, password=agol_password)
    print(f"AGOL connection established... {Utility.calculate_time_taken(start_time=start_time)} seconds since start")

    # Need to get the hosted feature table based on id.
    asset_inventory_table_agol = gis.content.get(agol_layer_id)
    asset_inventory_tables_list = asset_inventory_table_agol.tables
    asset_inventory_table = asset_inventory_tables_list[0]

    # Need to get feature set for layer, isolate record, and change attribute value. Used ESRI dev docs for guidance
    try:
        asset_inventory_feature_set = asset_inventory_table.query()
        asset_inventory_features_list = asset_inventory_feature_set.features

        if len(asset_inventory_features_list) != 1:
            print(f"WARNING: More than one feature in the truck count feature layer. Expected 1\n{asset_inventory_features_list}")
            exit()

        first_record = asset_inventory_features_list[0]
        headers_to_skip = ("ObjectId",)
        headers_in_table = first_record.attributes.keys() - headers_to_skip
        for header in headers_in_table:
            new_header = header.replace("_", " ")
            first_record.attributes[header] = value_counts_dict.get(new_header, None)  # PRODUCTION
            # first_record.attributes[header] = -9999  # TESTING

        # Need to change the existing count value to the newest value pulled from the database
        update_result = asset_inventory_table.edit_features(updates=[asset_inventory_features_list[0]])
        print(f"Result of update: {update_result}")

    except RuntimeError as rte:
        print(f"Runtime Error raised: {rte}")
        exit()

    print(f"\nProcess Completed... {Utility.calculate_time_taken(start_time=start_time)} seconds since start")


if __name__ == "__main__":
    main()