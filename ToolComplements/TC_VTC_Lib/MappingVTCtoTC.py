from TC_Common.SelectorCmd import cmd_colors
from TC_Common.SelectorCmd import CMDSelector
from TC_Common.SelectorCmd import Terminal
from TC_Common.CreateTCcommon import save_tc_in_json
from TC_Common.DictsFunctions import (
    add_at_beginning_of_dict,
    move_at_beginning_of_dict,
    copy_dict_key,
    remove_dict_key,
    subarrays_to_dicts,
    elevate_key,
    convert_keys_to_dict,
    convert_keys_to_strings,
    convert_keys_arrays_to_strings,
    convert_list_to_formatted_strings,
    convert_deepest_arrays_to_strings,
    convert_keys_to_strings_new,
    obtener_llaves_primer_nivel,
    evaluar_llaves,
    transform_values,
    join_string_arrays,
    recursive_evaluation_keys
)
import os
import json
import time
import re
import copy

delr = '\033[1A\033[K'
up = '\033[A'

class VTCMapping():
    def __init__(self, path_tmp=None, vtc_scrapper=None, mapping_obj=None):
        if path_tmp is None:
            return None
        self.path_tmp = path_tmp
        self.vtc_test_cases_debug = []
        self.vtc_tc_info = self.create_mapping_links(vtc_scrapper, mapping_obj)

    

    def create_mapping_links(self, vtc_scrapper, mapping_obj):
        mapping_links = mapping_obj.mapping_links
        vtc_tc = []
        self. vtc_test_cases_debug = []

        if recursive_evaluation_keys(vtc_scrapper.paragraphs, ['TraceItems', 'TraceItem']):
            trace_items = vtc_scrapper.paragraphs['TraceItems']['TraceItem']
        else:
            return None
        traceItemDic = {}
        for trace_item in trace_items:
            if recursive_evaluation_keys(trace_item, ['@attributes', 'ID']):
                traceItemDic[trace_item['@attributes']['ID']] = trace_item
        print(traceItemDic)

        if recursive_evaluation_keys(vtc_scrapper.paragraphs, ['TestCases', 'TestCase']):
            test_cases = vtc_scrapper.paragraphs['TestCases']['TestCase']
        else:
            return None
        for test_case in test_cases:
            if recursive_evaluation_keys(test_case, ['TraceItem-Refs', 'TraceItem-Ref']):
                trace_item_refs = test_case['TraceItem-Refs']['TraceItem-Ref']
            else:
                trace_item_refs = []
            if isinstance(trace_item_refs, str):
                trace_item_refs = [trace_item_refs]
            test_case['req_links_ids'] = trace_item_refs
            req_links = []
            for req_link_id in test_case['req_links_ids']:
                if traceItemDic.get(req_link_id):
                    req_links.append(traceItemDic[req_link_id]['Reference'])
            test_case['req_links'] = req_links
        


        title_prefix = input(f"Do you want to add a prefix to the title of the Test Cases? (Default: ''): ")
        if title_prefix != "":
            title_prefix = title_prefix.strip() + " "
        vtc_tc_mapped = []
        for element in test_cases:
            title = element["Name"]
            description = element["ID"]
            vtc_tc_mapped.append(mapping_obj.generate_mapped_link(element, "VTC", title, description, title_prefix))
        
        return vtc_tc_mapped