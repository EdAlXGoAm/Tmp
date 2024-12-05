from TC_Common.TestCasesInfo import TestCasesInfo
from TC_Common.PrintFunctions import PrintFunctions
from TC_Common.CreateTCcommon import etm_create_process
from TC_PDF_Lib.ScrappingPDF import PDFScrapper
from TC_PDF_Lib.MappingPDFtoTC import PDFMapping
from UnitScripts.Log_script import Logger
import copy

class PDFCreation():
    def __init__(self, debug=False, path_tmp=None):
        self.log_object = Logger(debug, name="log_file_PDF.html")
        # ************ PATHS INITIALIZATION ************
        if path_tmp is None:
            return None
        self.path_tmp = path_tmp

        self.pdf_tc_info = []

    def read_pdf_file(self, file, mapping_obj):
        self.pdf_scrapper = PDFScrapper(file, self.path_tmp, mapping_obj)
        self.pdf_mapping = PDFMapping(self.path_tmp, self.pdf_scrapper, mapping_obj)
        test_cases_info = TestCasesInfo(mapping_obj, self.log_object)
        self.pdf_tc_info = copy.deepcopy(self.pdf_mapping.pdf_tc_info)
        for pdf_tc in self.pdf_tc_info:
            test_case = test_cases_info.new_test_case()
            test_cases_info.link_mapp_element_to_tc(pdf_tc["TestCaseFormat"], test_case)
            test_cases_info.add_test_case(test_case)
        return test_cases_info
    
    def create_pdf_test_cases(self, qm_context, file, mapping_obj, recycle=False, id_list=None, config=None, context_factory=None):
        PrintFunctions.print_header("CREATE PDF TEST CASES")
        test_cases_info = self.read_pdf_file(file, mapping_obj)
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