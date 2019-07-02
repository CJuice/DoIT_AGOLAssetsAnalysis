"""
Contains the DatasetAGOL class that is for storing dataset values as class attributes and for providing functionality
necessary to get/process the values.
Author: CJuice
Date: 20190702
Modifications:

"""

import datetime
import json
import xml.etree.ElementTree as ET
import requests
import doit_AGOLAssetsAnalysis_Variables_AGOL as var

from bs4 import BeautifulSoup
from dateutil import parser as date_parser
from doit_AGOLAssetsAnalysis_Utility import Utility


class DatasetAGOL:
    """
    Class for storing information on a arcgis online datasets and for processing values for output needs.
    An object is instantiated to None for all attributes and then the values are assigned after extraction from json or
        after processing.
    Attributes are organized by their original source or into derived values. Three resources are consulted and these
    are the data catalog json, the metadata xml for each dataset, and the group to which the asset is assigned.
    The values in the response are extracted, assigned, and stored as attributes but the original is not saved.
    The attributes have been organized alphabetically within their source groups. The derived values category
    comes from processing raw values and involve decision making or conversions.
    """

    OWNER = 'owner:mdimapdatacatalog'
    RECORD_LIMIT = '100'  # When changed from 100 the return quantity doesn't actually change. Unsure why ineffective.
    SORT_FIELD = 'title'

    def __init__(self):
        """
                Instantiate the default dataset object in preparation for value assignments.

                Values in metadata xml (for example) that were previously sourced from data catalog have been ignored.
                 The following listing captures the decisions made while building this process.

                d = data catalog, m = metadata

                DATA CATALOG NOTES:
                appCategories - dropped after inspection. All values Null
                banner - dropped after inspection. All values Null
                categories - dropped after inspection. All values Null
                culture - dropped after inspection. All values en-us
                documentation - dropped after inspection. All values Null
                groupDesignations - dropped after inspection. All values Null
                guid - dropped after inspection. All values Null
                industries - dropped after inspection. All values Null
                languages - dropped after inspection. All values Null
                largeThumbnail - dropped storage because doesn't appear to have much value at this time
                listed - dropped after inspection. All values Null
                proxyFilter - dropped after inspection. All values Null
                screenshots - dropped after inspection. All values Null
                size - dropped after inspection. All values Null
                snippet - dropped after inspection. All values Null
                thumbnail - dropped storage because doesn't appear to have much value at this time

                METADATA NOTES:
                dataIdInfo
                    resTitle - title (d)
                    idAbs - description (d)
                    idPurp - title (d) or snippit (d) (appears to just be the title value)
                    idCredit - accessInformation (d)
                    dataChar>CharSetDc - Not stored (unknown meaning or value)
                    searchKeys>keyword - tags (d)
                    resConst>Consts>useLimit - licenseInfo (d)
                dataExt>geoEle>GeoBndBox> - Not stored (Appears to be bounding box coordinates). Not present in all.
                distInfo
                    distTranOps>onLineSrc>linkage - url (d)
                Esri
                    ArcGISStyle - Not Stored (metadata style indicator)
                    ArcGISFormat - Not Stored (unknown meaning)
                    ArcGISProfile - Not Stored (unknown value)
                    PublishStatus - Not Stored (unknown meaning or value)
                mdDateSt - Not Stored (unknonw meaning or value)
                mdFileID - id (d)
                mdChar>CharSetCd - Not Stored (uknown meaning or value)
                mdContact>role<RoleCd - Not Stored (uknown meaning or value)
                Binary - Not Stored (appears to be for images like thumbnails). Not present in all.

                XML NOTES:
                    From examining every asset as of 20190621 CJuice. I did not explore every nook and cranny. There
                    could be remaining values present to exploit but deep comparison of the xml for every asset
                    would need to occur.
                    set of root xml elements -
                        {'mdChar', 'Esri', 'mdContact', 'mdDateSt', 'dataIdInfo', 'distInfo', 'Binary', 'mdFileID'}
                    set of children xml elements under dataIdInfo -
                        {'resConst', 'dataExt', 'searchKeys', 'dataChar', 'idAbs', 'idPurp', 'idCitation', 'idCredit'}
                    set of children xml elements under idCitation -
                        {'date', 'citRespParty', 'resTitle', 'collTitle'}
                    set of children xml elements under date -
                        {'reviseDate', 'pubDate'}

                GROUP NOTES:
                The category attribute comes from inspection of the group to which the asset is assigned. A Group has
                substantial data available on it and this prompted the design of a Group class. See the group class for
                more details on what could be extracted.

        """

        # NON-DERIVED
        self.portal = "Data Catalog"  # Would make a constant but mapping to pandas df field becomes more cumbersome.
        self.group_id = None

        # Data Catalog sourced attributes
        self.access = None
        self.access_information = None
        # self.app_categories = None
        self.average_rating = None
        # self.banner = None
        # self.categories = None
        self.content_status = None
        self.created = None
        # self.culture = None
        self.description_raw = None
        # self.documentation = None
        self.extent = None
        # self.group_designations = None
        # self.guid = None
        self.id = None
        # self.industries = None
        # self.languages = None
        # self.large_thumbnail = None
        self.license_info_raw = None
        # self.listed = None
        self.modified = None
        self.name = None
        self.number_of_comments = None
        self.number_of_ratings = None
        self.number_of_views = None
        self.org_id = None
        self.owner = None
        self.properties = None
        # self.proxy_filter = None
        self.score_completeness = None
        # self.screenshots = None
        # self.size = None
        # self.snippet = None
        self.spatial_reference = None
        self.tags = None
        # self.thumbnail = None
        self.title = None
        self.type_ = None
        self.type_keywords = None
        self.url = None

        # Metadata XML sourced attributes
        # self.esri_metadata_xml_element = None
        self.maintenance_frequency_code = None
        self.meta_creation_date_str = None
        self.meta_creation_time_str = None
        self.meta_modification_date_str = None
        self.meta_modification_time_str = None
        self.organization_name = None
        self.publication_date_str = None

        # Source URL Query
        self.number_of_rows = None  # Old process did not do this.
        self.columns = None

        # DERIVED
        self.category = None
        self.column_names_string = None
        self.created_dt = None
        self.days_since_last_data_update = None
        self.description_text = None
        self.license_info_text = None
        self.maintenance_frequency_word = None
        self.meta_creation_date_dt = None
        self.meta_creation_time_dt = None
        self.meta_modification_date_dt = None
        self.meta_modification_time_dt = None
        self.metadata_url = None
        self.missing_metadata_fields = None  # Socrata output contains these values but too many to do for agol
        self.modified_dt = None
        self.publication_date_dt = None
        self.tags_string = None
        self.url_agol_item_id = None
        self.updated_recently_enough = None

    def assign_data_catalog_json_to_class_values(self, data_json: dict):
        """
        Get values from json and assign to class attributes
        Some of these are commented out because they were not deemed useful after inspection. The functionality was
        kept so that in the future it could be easily turned on if needed.
        :param data_json:
        :return:
        """
        self.access = data_json.get("access", None)
        self.access_information = data_json.get("accessInformation", None)
        # self.app_categories = data_json.get("appCategories", None)
        self.average_rating = data_json.get("avgRating", None)
        # self.banner = data_json.get("banner", None)
        # self.categories = data_json.get("categories", None)
        self.content_status = data_json.get("contentStatus", None)
        self.created = data_json.get("created", None)
        # self.culture = data_json.get("culture", None)
        self.description_raw = data_json.get("description", None)
        # self.documentation = data_json.get("documentation", None)
        self.extent = data_json.get("extent", None)
        # self.group_designations = data_json.get("groupDesignations", None)
        # self.guid = data_json.get("guid", None)
        self.id = data_json.get("id", None)
        # self.industries = data_json.get("industries", None)
        # self.languages = data_json.get("languages", None)
        # self.large_thumbnail = data_json.get("largeThumbnail", None)
        self.license_info_raw = data_json.get("licenseInfo", None)
        # self.listed = data_json.get("listed", None)
        self.modified = data_json.get("modified", None)
        self.name = data_json.get("name", None)
        self.number_of_comments = data_json.get("numComments", None)
        self.number_of_ratings = data_json.get("numRatings", None)
        self.number_of_views = data_json.get("numViews", None)
        self.org_id = data_json.get("orgId", None)
        self.owner = data_json.get("owner", None)
        self.properties = data_json.get("properties", None)
        # self.proxy_filter = data_json.get("proxyFilter", None)
        self.score_completeness = data_json.get("scoreCompleteness", None)
        # self.screenshots = data_json.get("screenshots", None)
        # self.size = data_json.get("size", None)
        # self.snippet = data_json.get("snippit", None)
        self.spatial_reference = data_json.get("spatialReference", None)
        self.tags = data_json.get("tags", None)
        # self.thumbnail = data_json.get("thumbnail", None)
        self.title = data_json.get("title", None)
        self.type_ = data_json.get("type", None)
        self.type_keywords = data_json.get("typeKeywords", None)
        self.url = data_json.get("url", None)

    def build_standardized_item_url(self):
        """
        Build the standard dataset url based on the unique item id value and store.
        :return:
        """
        self.url_agol_item_id = var.arcgis_item_url.format(item_id=self.id)

    def build_metadata_xml_url(self):
        """
        Build the url for requesting the metadata for a dataset and assign to attribute
        :return:
        """
        self.metadata_url = var.arcgis_metadata_url.format(arcgis_items_root_url=var.arcgis_items_root_url,
                                                           item_id=self.id)

    def calculate_days_since_last_data_update(self):
        """
        Subtract rows updated date in seconds from process initiation time in seconds and convert to whole days.
        :return:
        """
        if self.publication_date_dt is not None:
            try:
                self.days_since_last_data_update = (var.process_initiation_datetime - self.publication_date_dt).days
            except TypeError as te:
                print(f"TypeError: {te}. pub tz:{self.publication_date_dt.tzinfo}, process tz: {var.process_initiation_datetime.tzinfo}, {self.url_agol_item_id}")
                self.days_since_last_data_update = None

    def check_for_null_source_url_and_replace(self):
        """
        Check the url attribute for null and replace with a value identified by socrata as a valid url.
        :return:
        """
        self.url = "https://N.U.LL" if self.url is None else self.url

    def convert_milliseconds_attributes_to_datetime(self):
        """
        Convert milliseconds value to datetime values and assign to attributes.
        At time of design this applied to the created value and the modified value.
        :return:
        """
        def local_inner_function(id_for_error, value_in_millis):
            try:
                return datetime.datetime.fromtimestamp(value_in_millis/1000)
            except TypeError as te:
                print(f"TypeError during convert_milliseconds_to_datetime(). value:{value_in_millis}, Asset: {id_for_error}. {te}")
                return None

        self.created_dt = local_inner_function(id_for_error=self.id, value_in_millis=self.created)
        self.modified_dt = local_inner_function(id_for_error=self.id, value_in_millis=self.modified)

    def create_tags_string(self):
        """
        Join list of strings together to make commas separated string for output.
        :return:
        """
        self.tags_string = ", ".join(self.tags) if self.tags is not None else None

    def extract_and_assign_esri_date_time_values(self, element: ET.Element):
        """
        Extract values from esri xml element and assign to instance attributes.
        :param element: xml element to examine
        :return:
        """
        # Extract ESRI xml value/section
        esri_metadata_xml_element = Utility.extract_first_immediate_child_feature_from_element(
            element=element,
            tag_name="Esri")

        # Safeguard against None and return
        if esri_metadata_xml_element is None:
            print(f"ESRI XML Tag is None. Asset: {self.url_agol_item_id}")
            return

        # Setup of the tags to be extracted
        esri_xml_tags_and_values = {"CreaDate": None,
                                    "CreaTime": None,
                                    "ModDate": None,
                                    "ModTime": None}

        # search for and extract the items, then store in dict
        for tag_name, value in esri_xml_tags_and_values.items():
            try:
                esri_xml_tags_and_values[tag_name] = Utility.extract_first_immediate_child_feature_from_element(
                    element=esri_metadata_xml_element,
                    tag_name=tag_name).text
            except AttributeError as ae:
                print(f"ESRI XML Tag '{tag_name}' NOT FOUND. Call to .text raised Attribute Error: {ae}. Asset: {self.url_agol_item_id}")

        # Assign the values in the dict to the relevant attribute
        self.meta_creation_date_str = esri_xml_tags_and_values.get("CreaDate")
        self.meta_creation_time_str = esri_xml_tags_and_values.get("CreaTime")
        self.meta_modification_date_str = esri_xml_tags_and_values.get("ModDate")
        self.meta_modification_time_str = esri_xml_tags_and_values.get("ModTime")

        return

    def extract_and_assign_field_names(self, response: requests.models.Response):
        """
        Extract values from response json and assign to attributes
        :param response: response from request
        :return:
        """
        try:

            # Need the response json
            fields_list = response.json().get("fields", None)
        except Exception as e:
            print(f"Unanticipated Exception while extracting field names from response. {e}. {self.url_agol_item_id}")
        else:

            # Protect against None and return
            if fields_list is None:
                return

            # for field in the fields list get the name or substitute a string indicating an error/issue.
            accumulated_field_names_list = []
            for field in fields_list:
                accumulated_field_names_list.append(field.get("name", "ERROR_DoIT"))

            # make a comma separated string of list items and assign
            self.column_names_string = ", ".join(accumulated_field_names_list)

    def extract_and_assign_maintenance_frequency_code(self, element: ET.Element):
        """
        Extract and assign values from xml element.

        Specific to maintenance frequency code. After the following dataIdInfo/resMaint/maintFreq/MaintFreqCd
        :param element: xml element
        :return:
        """

        data_id_info_element = Utility.extract_first_immediate_child_feature_from_element(element=element, tag_name="dataIdInfo") if element is not None else None
        res_maintenance_element = Utility.extract_first_immediate_child_feature_from_element(element=data_id_info_element, tag_name="resMaint") if data_id_info_element is not None else None
        maint_freq_element = Utility.extract_first_immediate_child_feature_from_element(element=res_maintenance_element, tag_name="maintFreq") if res_maintenance_element is not None else None
        maint_freq_code_element = Utility.extract_first_immediate_child_feature_from_element(element=maint_freq_element, tag_name="MaintFreqCd") if maint_freq_element is not None else None
        maint_freq_code_dict = maint_freq_code_element.attrib if maint_freq_code_element is not None else None
        self.maintenance_frequency_code = maint_freq_code_dict.get("value", None) if maint_freq_code_dict is not None else None

    def extract_and_assign_organization_name(self, element):
        """
        Extract and assign values from xml element.

        Specific to organization name. After the following dataIdInfo/idCitation/citRespParty/rpOrgName
        :param element: xml element
        :return:
        """

        data_id_info_element = Utility.extract_first_immediate_child_feature_from_element(element=element,
                                                                                          tag_name="dataIdInfo") if element is not None else None
        id_citation_element = Utility.extract_first_immediate_child_feature_from_element(element=data_id_info_element,
                                                                                         tag_name="idCitation") if data_id_info_element is not None else None
        cit_resp_party_element = Utility.extract_first_immediate_child_feature_from_element(element=id_citation_element,
                                                                                  tag_name="citRespParty") if id_citation_element is not None else None
        rp_org_name_element = Utility.extract_first_immediate_child_feature_from_element(element=cit_resp_party_element,
                                                                                      tag_name="rpOrgName") if cit_resp_party_element is not None else None
        self.organization_name = rp_org_name_element.text if rp_org_name_element is not None else None

    def extract_and_assign_publication_date(self, element):
        """
        Extract and assign values from xml element.

        Specific to publication date. After the following dataIdInfo/idCitation/date/pubDate
        :param element:
        :return:
        """

        data_id_info_element = Utility.extract_first_immediate_child_feature_from_element(element=element, tag_name="dataIdInfo") if element is not None else None
        id_citation_element = Utility.extract_first_immediate_child_feature_from_element(element=data_id_info_element, tag_name="idCitation") if data_id_info_element is not None else None
        date_element = Utility.extract_first_immediate_child_feature_from_element(element=id_citation_element, tag_name="date") if id_citation_element is not None else None
        pub_date_element = Utility.extract_first_immediate_child_feature_from_element(element=date_element, tag_name="pubDate") if date_element is not None else None
        self.publication_date_str = pub_date_element.text if pub_date_element is not None else None

    def is_up_to_date(self):
        """
        Determine if a dataset is up to date according to its update frequency.
        Created two dictionaries, instead of one, to hold integer comparison value snd string values. The integer
        values are checked against the number of days since the data has been updated. If the update frequency value
        is a string then retrieve the string value from the string dict. If no value is found in the dicts then the
        metadata is deemed as missing.
        :return:
        """

        updated_enough_ints = {"Continual": 0,
                               "Daily": 1,
                               "Weekly": 7,
                               "Fortnightly": 14,
                               "Monthly": 31,
                               "Quarterly": 91,
                               "Biannually": 730,
                               "Annually": 365}

        updated_enough_strings = {"As Needed": var.evaluation_difficult,
                                  "Irregular": var.evaluation_difficult,
                                  "Not Planned": var.updated_enough_yes,
                                  "Unknown": f"{var.better_metadata_needed} {var.update_frequency_missing}",
                                  "": f"{var.better_metadata_needed} {var.update_frequency_missing}",
                                  "Empty": f"{var.better_metadata_needed} {var.update_frequency_missing}",
                                  "-9999": "DoIT ERROR"}

        answer = None
        int_check = updated_enough_ints.get(self.maintenance_frequency_word, None)
        string_check = updated_enough_strings.get(self.maintenance_frequency_word, None)

        if int_check is not None and self.days_since_last_data_update is not None:
            answer = var.updated_enough_yes if self.days_since_last_data_update <= int_check else var.updated_enough_no
        elif string_check is not None:
            answer = string_check
        else:
            answer = var.metadata_missing

        self.updated_recently_enough = answer
        return

    def parse_date_like_string_attributes(self):
        """
        Parse date like strings into datetime objects and assign.

        NOTE: The attributes of interest at the time of design were esri's creation date and time, esri's modification
        date and time, and the publication date that is auto-populated unless we manually enter a value
        :return:
        """
        def local_inner_function(value: str):
            """
            Parse the string date and time value and return all while protected with try/except.
            :param value: string value to be parsed
            :return:
            """
            # For real time or continual update data we have used "Continual" in the publication date metadata field.
            #   Since that is not a datetime we need to check and convert. This is necessary for later steps when we
            #   determine the freshness of the data.
            if value is None:

                # Normally just try to parse and catch exception but so many None that print outs get excessive.
                return None
            elif value == "Continual":
                return var.process_initiation_datetime

            try:
                return date_parser.parse(value)
            except (ValueError, TypeError) as err:
                print(f"Exception during parsing of date like string {value}. {err}")
                return None

        self.meta_creation_date_dt = local_inner_function(value=self.meta_creation_date_str)
        self.meta_creation_time_dt = local_inner_function(value=self.meta_creation_time_str)
        self.meta_modification_date_dt = local_inner_function(value=self.meta_modification_date_str)
        self.meta_modification_time_dt = local_inner_function(value=self.meta_modification_time_str)
        self.publication_date_dt = local_inner_function(value=self.publication_date_str)

    def parse_html_attribute_values_to_soup_get_text(self):
        """
        Parse html like strings to isolate the text and remove html code, and assign to attribute
        :return:
        """
        def local_inner_function(id_for_error, value):
            """
            Parse string using BeautifulSoup to isolate meaningful text (sans html code characters)
            :param id_for_error: asset id for meaningful printout
            :param value: string to be souped
            :return:
            """
            try:
                soup = BeautifulSoup(value, "html.parser")
                return soup.get_text()
            except Exception as e:
                print(f"Unanticipated Exception raised in parsing license_info using BeautifulSoup. Asset: {id_for_error}. {e}")
                return None

        self.license_info_text = local_inner_function(id_for_error=self.id, value=self.license_info_raw)
        self.description_text = local_inner_function(id_for_error=self.id, value=self.description_raw)

    def process_maintenance_frequency_code(self):
        """
        Determine, based on code value, which maintenance frequency string to assign.

        Note: To keep AGOL process similar to socrata process we will convert the code to a word and then use the word
        to check if is up to date. Could just use these codes instead but wanted to keep similar to Socrata process for
        ease of understanding in future.
        :return:
        """

        # Protect against None
        if self.maintenance_frequency_code is None:
            return
        else:
            code_conversion_dict = {"000": "Empty",  # Guessing at this
                                    "001": "Continual",
                                    "002": "Daily",
                                    "003": "Weekly",
                                    "004": "FortNightly",
                                    "005": "Monthly",
                                    "006": "Quarterly",
                                    "007": "Biannually",
                                    "008": "Annually",
                                    "009": "As Needed",
                                    "010": "Irregular",
                                    "011": "Not Planned",
                                    "012": "Unknown",
                                    }
            self.maintenance_frequency_word = code_conversion_dict.get(self.maintenance_frequency_code, "-9999")

    def process_category_from_group_object(self, group_object_title: str):
        """
        Remove a default string value from the group object title and assign
        :param group_object_title:  title of group
        :return:
        """
        self.category = group_object_title.replace("Maryland GIS Data Catalog: ", "") if group_object_title is not None else None

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

