from TC_Common.SelectorCmd import cmd_colors
from TC_Common.SelectorCmd import CMDSelector
from TC_Common.TestCasesInfo import TestCasesInfo
from TC_Common.PrintFunctions import PrintFunctions
from TC_Common.CreateTCcommon import etm_create_process
from TC_VTT_Lib.ScrappingVTT import VTTScrapper
from TC_VTT_Lib.MappingVTTtoTC import VTTMapping
from UnitScripts.Log_script import Logger
import os
import time
import copy


class VTTCreation():
    def __init__(self, debug, path_tmp=None):
        self.log_object = Logger(debug, name="log_file_VTT.html")
        # ************ PATHS INITIALIZATION ************
        if path_tmp is None:
            return None
        self.path_tmp = path_tmp
        
        self.vtt_tc_info = []

    def read_vtt_file(self, file, mapping_obj):
        self.vtt_scrapper = VTTScrapper(file, mapping_obj)
        self.vtt_mapping = VTTMapping(self.path_tmp, self.vtt_scrapper, mapping_obj)
        test_cases_info = TestCasesInfo(mapping_obj, self.log_object)
        self.vtt_tc_info = copy.deepcopy(self.vtt_mapping.vtt_tc_info)
        for vtt_tc in self.vtt_tc_info:
            test_case = test_cases_info.new_test_case()
            test_cases_info.link_mapp_element_to_tc(vtt_tc["TestCaseFormat"], test_case)
            test_cases_info.add_test_case(test_case)
        return test_cases_info

    def create_vtt_test_cases(self, qm_context, file, mapping_object, recycle=False, id_list=None, config=None, context_factory=None):
        PrintFunctions.print_header("CREATE VTT TEST CASES")
        test_cases_info = self.read_vtt_file(file, mapping_object)
        if test_cases_info == "Cancel":
            return
        if recycle:
            for index, test_case in enumerate(test_cases_info.test_cases):
                if index < len(id_list):
                    new_test_case = self.add_tcid(test_case, id_list[index])
                test_cases_info.test_cases[index] = new_test_case
        etm_create_process(qm_context, test_cases_info, self.path_tmp, self.log_object, recycle, config=config, context_factory=context_factory)

    def add_tcid(self, test_case, id):
        test_case.tcid = id
        return test_case
