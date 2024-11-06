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

class VTCCreation():
    def __init__(self, debug=False, path_tmp=None):
        self.log_object = Logger(debug, name="log_file_VTC.html")
        # ************ PATHS INITIALIZATION ************
        if path_tmp is None:
            return None
        self.path_tmp = path_tmp

        self.vtc_tc_info = []

    def read_vtc_file(self, file, mapping_obj):
        self.vtc_scrapper = VTCScrapper(file, mapping_obj)
        self.vtc_mapping = VTCMapping(self.path_tmp, self.vtc_scrapper, mapping_obj)
        test_cases_info = TestCasesInfo(mapping_obj, self.log_object)
        self.vtc_tc_info = copy.deepcopy(self.vtc_mapping.vtc_tc_info)
        for vtc_tc in self.vtc_tc_info:
            test_case = test_cases_info.new_test_case()
            test_cases_info.link_mapp_element_to_tc(vtc_tc["TestCaseFormat"], test_case)
            test_cases_info.add_test_case(test_case)
        return test_cases_info
    
    def create_vtc_test_cases(self, qm_context, file, mapping_obj, recycle=False, id_list=None):
        PrintFunctions.print_header("CREATE VTC TEST CASES")
        test_cases_info = self.read_vtc_file(file, mapping_obj)
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
