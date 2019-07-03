"""
File designated for process variables in order to centralize variables, and de-clutter main script.
Author: CJuice
Date: 20190702
Modifications:

"""
import datetime
import os

# NOT DERIVED
_root_file_path = os.path.dirname(__file__)
# all_map_layers = "All map layers from MD iMAP are in the process of being surveyed to determine this information."
# arcgis_item_url = "https://maryland.maps.arcgis.com/home/item.html?id={item_id}"
arcgis_root_url = r"https://www.arcgis.com"
credentials_file = f"{_root_file_path}/Docs/md_doit_agol_credentials.cfg"

# better_metadata_needed = "Better Metadata Needed."
# dataframe_to_header_mapping_for_excel_output = {"Dataset Name": "title", "Link": "url_agol_item_id",
#                                                 "Agency Performing Data Updates": "organization_name",
#                                                 "Owner": "owner",
#                                                 "Data Provided By": "organization_name",
#                                                 "Source URL": "url",
#                                                 "Update Frequency": "maintenance_frequency_word",
#                                                 "Date of Most Recent Data Change": "publication_date_dt",
#                                                 "Days Since Last Data Update": "days_since_last_data_update",
#                                                 "Date of Most Recent View Change in Data or Metadata": "publication_date_dt",
#                                                 "Days Since Last View Update": "days_since_last_data_update",
#                                                 "Updated Recently Enough": "updated_recently_enough",
#                                                 "Number of Rows": "number_of_rows",
#                                                 "Tags Keywords": "tags_string", "Column Names": "column_names_string",
#                                                 "Missing Metadata Fields": "missing_metadata_fields",
#                                                 "Portal": "portal",
#                                                 "Category": "category"}
# json_output_columns_list = ["category", "description_text", "id", "publication_date_dt", "portal", "organization_name", "url", "tags", "title", "type_", "url_agol_item_id"]
# json_param_for_request = {'f': 'json'}
# metadata_missing = "Metadata on update frequency are missing. Dataset owner should provide this information to resolve this issue."
# null_string = "NULL"
# number_of_seconds_in_a_day = 86400
# other_update_frequency = "Other Update Frequency - If frequency isn't included in list above, please describe it here."
# output_excel_sheetname = datetime.datetime.now().strftime('%Y%m%d')
# types_to_evaluate = ("Feature Service", "Image Service", "Map Service") # Currently ignored types: Code Attachment, Web Map, Web Mapping Application
# update_frequency_missing = "Update frequency metadata are missing. Dataset owner should add metadata to resolve this issue."
# update_frequency_unknown = "Update frequency metadata is Unknown. Dataset owner should add metadata to resolve this issue."
# updated_enough_no = "No"
# updated_enough_yes = "Yes"
# whether_dataset = "Whether dataset is up to date cannot be calculated until the Department of Information Technology collects metadata on update frequency."

# DERIVED
# arcgis_group_url = "{arcgis_items_root_url}/{item_id}/groups/"
arcgis_sharing_rest_url = f"{arcgis_root_url}/sharing/rest"
arcgis_data_catalog_url = f"{arcgis_sharing_rest_url}/search"  # Dependent so out of alphabetic order
# arcgis_items_root_url = f"{arcgis_sharing_rest_url}/content/items"  # Dependent so out of alphabetic order
# arcgis_metadata_url = "{arcgis_items_root_url}/{item_id}/info/metadata/metadata.xml"
# evaluation_difficult = f"{updated_enough_yes}. The data are updated as needed, which makes evaluation difficult. As an approximate measure, this dataset is evaluated as updated recently enough because it has been updated in the past month."
# fields_query_params = {"where": "1=1", "outFields": "*", "returnGeometry": False, "resultRecordCount": 1, "f": "pjson"}
# output_excel_file_path_data_freshness_AGOL = f"{_root_file_path}/DataFreshnessOutputs/AGOL_data_freshness.xlsx"
# output_excel_file_path_full_dataframe = r"{_root_file_path}/Docs/{date}AGOL_data_output.xlsx".format(_root_file_path=_root_file_path, date=datetime.datetime.now().strftime('%Y%m%d'))
# output_json_file_path_data_freshness_AGOL = f"{_root_file_path}/DataFreshnessOutputs/AGOL_data_freshness.json"
# process_initiation_datetime = datetime.datetime.now(datetime.timezone.utc)
# record_count_params = {"where": "1=1", "returnGeometry": False, "returnCountOnly": True, "f": "pjson"}
# root_service_query_url = r"{data_source_rest_url}/query"
