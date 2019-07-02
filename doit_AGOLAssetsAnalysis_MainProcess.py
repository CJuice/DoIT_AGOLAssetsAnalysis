"""

"""


def main():

    # IMPORTS
    import time
    start_time = time.time()
    print(f"Start Time: {start_time} seconds since Epoch")

    import datetime
    import pandas as pd
    import requests

    from doit_AGOLAssetsAnalysis_Utility import Utility
    from doit_AGOLAssetsAnalysis_DatasetAGOL import DatasetAGOL

    # Disable the security warnings for https from data.maryland.gov
    requests.packages.urllib3.disable_warnings()

    print(f"\nImports Completed... {Utility.calculate_time_taken(start_time=start_time)} seconds since start")

    # VARIABLES
    today_date = datetime.datetime.now().strftime("%Y%m%d")
    summary_json_file = r"Docs\ProcessOutputs\{today_date}_AGOL_Assets_Inventory_Summary.json".format(today_date=today_date)
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
    value_counts_dict["TOTAL"] = sum

    summary_df = pd.Series(value_counts_dict).to_frame().reset_index()
    summary_df.rename(columns={"index": "Asset Type", 0: "Count"}, inplace=True)
    summary_df.to_json(path_or_buf=summary_json_file, orient="records")

    # For print out purposes
    print(summary_df)


    print(f"\nProcess Completed... {Utility.calculate_time_taken(start_time=start_time)} seconds since start")


if __name__ == "__main__":
    main()