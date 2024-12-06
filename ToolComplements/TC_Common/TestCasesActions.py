from TC_Common.SelectorCmd import cmd_colors
from TC_Common.SelectorCmd import CMDSelector
from TC_Common.SelectorCmd import create_path
from TC_Common.FilesFunctions import select_file
from TC_Common.Mapping_common import MappingClass
from TC_Common.PrintFunctions import PrintFunctions
from TC_JSN_Lib.CreateTCfromJson import JsonCreation
from TC_RTF_Lib.CreateTCfromRTF import RTFCreation
from TC_EXCEL_Lib.CreateTCfromExcel import ExcelCreation
from TC_PDF_Lib.CreateTCfromPDF import PDFCreation
from TC_VTT_Lib.CreateTCfromVTT import VTTCreation
from TC_VTC_Lib.CreateTCfromVTC import VTCCreation
import os
import time

class TestCasesActions():
    def __init__(self, debug_in_console=False):
        self.tmp_file_path = create_path(f"{os.path.dirname(__file__)}/../tmp")

        self.path_files = create_path('D:/DemoFiles')
        self.path_rtf_files = self.path_files
        self.path_excel_files = self.path_files
        self.path_vtt_files = self.path_files
        self.path_vtc_files = self.path_files
        self.path_mapp = f'{os.path.dirname(__file__)}/../../MAPP'
        
        # ************ JSON FEATURE INITIALIZATION ************
        self.path_json_mapping_files = create_path(f'{self.path_mapp}')
        self.json_actions = JsonCreation(debug=debug_in_console, path_tmp=self.tmp_file_path) # Object from CreateTCfromJson.py
        # ************ RTF FEATURE INITIALIZATION ************
        self.path_rtf_mapping_files = create_path(f'{self.path_mapp}/RTFMapping')
        self.rtf_actions = RTFCreation(debug=debug_in_console, path_tmp=self.tmp_file_path) # Object from CreateTCfromRTF.py
        # ************ EXCEL FEATURE INITIALIZATION ************
        self.excel_actions = ExcelCreation(debug=debug_in_console, path_tmp=self.tmp_file_path) # Object from CreateTCfromExcel.py
        # ************ PDF FEATURE INITIALIZATION ************
        self.path_pdf_mapping_files = create_path(f'{self.path_mapp}/PDFMapping')
        self.pdf_actions = PDFCreation(debug=debug_in_console, path_tmp=self.tmp_file_path) # Object from CreateTCfromRTF.py
        # ************ VTT FEATURE INITIALIZATION ************
        self.path_vtt_mapping_files = create_path(f'{self.path_mapp}/VTTMapping')
        self.vtt_actions = VTTCreation(debug=debug_in_console, path_tmp=self.tmp_file_path) # Object from CreateTCfromVTT.py
        # ************ VTC FEATURE INITIALIZATION ************
        self.path_vtc_mapping_files = create_path(f'{self.path_mapp}/VTCMapping')
        self.vtc_actions = VTCCreation(debug=debug_in_console, path_tmp=self.tmp_file_path) # Object from CreateTCfromVTC.py
        
        self.actions = [
            "Create Test Cases",
            # "Recycle Test Cases",
            "Exit"
        ]

    def action(self, action, qm_context, config, context_factory):
        if action == "Create Test Cases":
            self.create_test_cases(qm_context, config=config, context_factory=context_factory)
        elif action == "Recycle Test Cases":
            self.create_test_cases(qm_context, recycle=True, config=config, context_factory=context_factory)

    def select_file_type(self):
        os.system('cls')
        print(f"************************* CREATE TEST CASES *************************")
        type_file_selector = CMDSelector()
        type_file_selector.title = "Select the file with the test cases to create:"
        type_file_selector.options = ["Json", "RTF", "Excel", "PDF", "VTC", "VTT", "Cancel"]
        type_file = type_file_selector.select()
        if type_file == "Cancel":
            return
        print(f"--- Selected file type: {cmd_colors.CYAN}{type_file}{cmd_colors.END}\n")
        return type_file
    
    def create_test_cases(self, qm_context, recycle=False, config=None, context_factory=None):
        type_file = self.select_file_type()
        PrintFunctions.print_header(f"CREATE {type_file} TEST CASES") if not recycle else PrintFunctions.print_header(f"RECYCLE {type_file} TEST CASES")
        id_list = None
        if recycle:
            recycle_obj = self.Recycle_ID_List(self.path_mapp)
            id_list = recycle_obj.get_id_list()
            if id_list == "Cancel":
                return "Cancel"
        if type_file == "Json":
            file = select_file(path=self.path_files, extension=".json", type_file="JSON", recursive=True)
            if file == "Cancel":
                return "Cancel"
            mapping_obj = MappingClass(self.path_json_mapping_files)
            self.json_actions.create_json_test_cases(qm_context, file, mapping_obj, recycle, id_list, config=config, context_factory=context_factory)
        if type_file == "RTF":
            file = select_file(path=self.path_files, extension=".txt", type_file="RTF", recursive=True)
            if file == "Cancel":
                return "Cancel"
            mapping_obj = MappingClass(self.path_rtf_mapping_files)
            if not mapping_obj.MappingClassError:
                self.rtf_actions.create_rtf_test_cases(qm_context, file, mapping_obj, recycle, id_list, config=config, context_factory=context_factory)
        elif type_file == "Excel":
            file = select_file(path=self.path_files, extension=[".xlsx", ".csv"], type_file="EXCEL", recursive=True)
            if file == "Cancel":
                return "Cancel"
            self.excel_actions.create_excel_test_cases(qm_context, file, recycle, id_list, config=config, context_factory=context_factory)
        elif type_file == "PDF":
            file = select_file(path=self.path_files, extension=[".pdf", ".json"], type_file="PDF", recursive=True)
            if file == "Cancel":
                return "Cancel"
            mapping_obj = MappingClass(self.path_pdf_mapping_files)
            if not mapping_obj.MappingClassError:
                self.pdf_actions.create_pdf_test_cases(qm_context, file, mapping_obj, recycle, id_list, config=config, context_factory=context_factory)
        elif type_file == "VTC":
            file = select_file(path=self.path_files, extension=".vtc-tso", type_file="VTC", recursive=True)
            if file == "Cancel":
                return "Cancel"
            mapping_obj = MappingClass(self.path_vtc_mapping_files)
            if not mapping_obj.MappingClassError:
                self.vtc_actions.create_vtc_test_cases(qm_context, file, mapping_obj, recycle, id_list, config=config, context_factory=context_factory)
        elif type_file == "VTT":
            file = select_file(path=self.path_files, extension=".vtt", type_file="VTT", recursive=True)
            if file == "Cancel":
                return "Cancel"
            mapping_obj = MappingClass(self.path_vtt_mapping_files)
            if not mapping_obj.MappingClassError:
                self.vtt_actions.create_vtt_test_cases(qm_context, file, mapping_obj, recycle, id_list, config=config, context_factory=context_factory)

    class Recycle_ID_List():
        def __init__(self, path_id_list):
            self.actions = [
                "ID",
                "ID Range",
                "ID List",
                "Cancel"
            ]
            self.path_id_list = path_id_list
        
        def recycle_selector(self):
            recycle_selector = CMDSelector()
            recycle_selector.title = "Do you want to input the reclycle ID by range or by list (file)?"
            recycle_selector.options = self.actions
            recycle = recycle_selector.select()
            return recycle

        def read_ids_from_file(self, file):
            id_list = []
            with open(file, 'r') as f:
                for line in f:
                    try:
                        id_list.append(int(line.strip()))
                    except ValueError:
                        print(f"--- {cmd_colors.RED}ERROR:{cmd_colors.END} Invalid ID in file.")
                        return False
            return id_list

        def one_id(self):
            is_number = False
            while not is_number:
                try:
                    id_list = [int(input("Input the ID to recycle: "))]
                    is_number = True
                    if id_list[0] == -1:
                        return "Cancel"
                except ValueError:
                    print(f"--- {cmd_colors.RED}ERROR:{cmd_colors.END} Invalid ID. Please input a number.\nInput -1 to cancel.")
            return id_list
        
        def validate_range(self, range_id):
            try:
                range_id = range_id.split("-")
                if len(range_id) != 2:
                    raise ValueError
                range_id = list(map(int, range_id))
                if range_id[0] > range_id[1]:
                    raise ValueError
                return range_id
            except ValueError:
                print(f"--- {cmd_colors.RED}ERROR:{cmd_colors.END} Invalid range ID.")
                return False
            
        def range_id(self):
            is_valid = False
            while not is_valid:
                range_id = input("Input the range of ID to recycle (e.g. 1-100): ")
                if range_id == '-1':
                    return "Cancel"
                range_id_list = self.validate_range(range_id)
                if range_id_list:
                    is_valid = True
                else:
                    print(f"--- {cmd_colors.RED}ERROR:{cmd_colors.END} Invalid range ID. Aborting recycle action.\nInput -1 to cancel.")
            id_list = list(range(range_id_list[0], range_id_list[1] + 1))
            print(f"--- Selected range: {cmd_colors.CYAN}{id_list}{cmd_colors.END}")
            return id_list

        def id_list(self):
            is_valid = False
            while not is_valid:
                id_file = select_file(self.path_id_list, ".txt", "ID List", recursive=True)
                print(f"--- Selected file: {cmd_colors.CYAN}{id_file}{cmd_colors.END}")
                id_list = self.read_ids_from_file(id_file)
                if not id_list:
                    print(f"--- {cmd_colors.RED}ERROR:{cmd_colors.END} Invalid ID list. Try again.")
                    continue
                selector = CMDSelector()
                selector.title = f"ID List: {"\n".join(map(str, id_list))}\nDo you want to continue with this list?"
                selector.options = ["Yes", "No"]
                if selector.select() == "Yes":
                    is_valid = True
            return id_list
        
        def get_id_list(self):
            self.selection = self.recycle_selector()
            if self.selection == "Cancel":
                return "Cancel"
            if self.selection == "ID":
                return self.one_id()
            elif self.selection == "ID Range":
                return self.range_id()
            elif self.selection == "ID List":
                return self.id_list()