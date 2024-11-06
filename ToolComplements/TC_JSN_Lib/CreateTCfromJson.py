from TC_Common.SelectorCmd import cmd_colors
from TC_Common.SelectorCmd import CMDSelector
from TC_Common.TestCasesInfo import TestCasesInfo
from TC_Common.PrintFunctions import PrintFunctions
from TC_Common.CreateTCcommon import etm_create_process
from TC_VTC_Lib.ScrappingVTC import VTCScrapper
from TC_VTC_Lib.MappingVTCtoTC import VTCMapping
from UnitScripts.Log_script import Logger
import os
import time
import io
import copy

class JsonCreation():
    def __init__(self, debug=False, path_tmp=None):
        self.log_object = Logger(debug, name="log_file_Json.html")
        # ************ PATHS INITIALIZATION ************
        if path_tmp is None:
            return None
        self.path_tmp = path_tmp


    def read_json_file(self, file, mapping_obj):
        test_cases_info = TestCasesInfo(mapping_obj, self.log_object)
        test_cases_info.test_cases = test_cases_info.get_tc_from_json(file)
        return test_cases_info
    
    def create_json_test_cases(self, qm_context, file, mapping_obj, recycle=False, id_list=None):
        PrintFunctions.print_header("CREATE JSON TEST CASES")
        test_cases_info = self.read_json_file(file, mapping_obj)
        if test_cases_info == "Cancel":
            return
        if recycle:
            for index, test_case in enumerate(test_cases_info.test_cases):
                if index < len(id_list):
                    new_test_case = self.add_tcid(test_case, id_list[index])
                test_cases_info.test_cases[index] = new_test_case
        etm_create_process(qm_context, test_cases_info, self.path_tmp, self.log_object, recycle)
        
    def add_tcid(self, test_case, id):
        test_case.tcid = id
        return test_case
