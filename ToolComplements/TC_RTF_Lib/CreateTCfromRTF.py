from TC_Common.SelectorCmd import cmd_colors
from TC_Common.SelectorCmd import CMDSelector
from TC_Common.TestCasesInfo import TestCasesInfo
from TC_Common.PrintFunctions import PrintFunctions
from TC_Common.CreateTCcommon import etm_create_process
from TC_RTF_Lib.ScrappingRTF import RTFScrapper
from TC_RTF_Lib.MappingRTFtoTC import RTFMapping
from UnitScripts.Log_script import Logger
import os
import time
import io
import copy

class RTFCreation():
    def __init__(self, debug=False, path_tmp=None):
        self.log_object = Logger(debug, name="log_file_RTF.html")
        # ************ PATHS INITIALIZATION ************
        if path_tmp is None:
            return None
        self.path_tmp = path_tmp

        self.rtf_tc_info = []

    def read_rtf_file(self, file, mapping_obj):
        self.rtf_scrapper = RTFScrapper(file, mapping_obj)
        self.rtf_mapping = RTFMapping(self.path_tmp, self.rtf_scrapper, mapping_obj)
        test_cases_info = TestCasesInfo(mapping_obj, self.log_object)
        self.rtf_tc_info = copy.deepcopy(self.rtf_mapping.rtf_tc_info)
        for rtf_tc in self.rtf_tc_info:
            test_case = test_cases_info.new_test_case()
            test_cases_info.link_mapp_element_to_tc(rtf_tc["TestCaseFormat"], test_case)
            test_cases_info.add_test_case(test_case)
        return test_cases_info

    def create_rtf_test_cases(self, qm_context, file, mapping_obj, recycle=False, id_list=None):
        PrintFunctions.print_header("CREATE RTF TEST CASES")
        test_cases_info = self.read_rtf_file(file, mapping_obj)
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