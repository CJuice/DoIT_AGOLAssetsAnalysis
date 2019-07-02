"""
Process for inspecting the inventory of assets in Maryland ArcGIS Online and providing analysis output.
Intended to be built on as we develop the analysis we want. A lot of the functionality has been borrowed from
the data freshness process and will diverge as needed.
"""


def main():

    # IMPORTS
    import time
    start_time = time.time()
    print(f"Start Time: {start_time} seconds since Epoch")

    import configparser
    import datetime
    import pandas as pd
    import requests

    from doit_AGOLAssetsAnalysis_Utility import Utility
    from doit_AGOLAssetsAnalysis_DatasetAGOL import DatasetAGOL

    # Disable the security warnings for https from data.maryland.gov
    requests.packages.urllib3.disable_warnings()

    print(f"\nImports Completed... {Utility.calculate_time_taken(start_time=start_time)} seconds since start")

    # VARIABLES
    parser = configparser.ConfigParser()
    today_date = datetime.datetime.now().strftime("%Y%m%d")
    summary_json_file = r"Docs\ProcessOutputs\{today_date}_AGOL_Assets_Inventory_Summary.csv".format(today_date=today_date)
    # FUNCTIONS

    # FUNCTIONALITY
    master_list_of_results = DatasetAGOL.request_all_data_catalog_results()

    # Print outs for general understanding of data.json level process
    print(f"Data Catalog Results Requests Process Completed... {Utility.calculate_time_taken(start_time=start_time)} seconds since start")
    print(f"RESULTS: {len(master_list_of_results)} ")
    type_list = []
    for item in master_list_of_results:
        type_ = item.get("type", None) if item is not None else None
        type_list.append(type_)

    # Evaluate asset types and summarize
    counts_ser = pd.Series(data=type_list)
    value_counts = counts_ser.value_counts()
    sum = value_counts.sum()
    value_counts_dict = value_counts.to_dict()
    value_counts_dict["TOTAL"] = [sum]  # Put into a list so that can create a dataframe directly from passing dict
    summary_df = pd.DataFrame(value_counts_dict)
    summary_df.to_csv(path_or_buf=summary_json_file, index=False)

    # For print out purposes
    print(summary_df)
    exit()
    # Upserting results to hosted table
    agol_password = parser["AGOL"]["PASSWORD"]
    agol_root_url = parser["AGOL"]["ROOT_URL"]
    agol_username = parser["AGOL"]["USER_NAME"]
    agol_layer_id = parser["AGOL"]["LAYER_ID"]
    print(f"AGOL variable parsing complete. Time passed since start = {datetime.now() - start_time}")


    print(f"\nProcess Completed... {Utility.calculate_time_taken(start_time=start_time)} seconds since start")


if __name__ == "__main__":
    main()