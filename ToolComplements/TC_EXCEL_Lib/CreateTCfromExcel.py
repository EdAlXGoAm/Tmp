from TC_Common.SelectorCmd import cmd_colors
from TC_Common.SelectorCmd import CMDSelector
from TC_Common.TestCasesInfo import TestCasesInfo
from TC_Common.PrintFunctions import PrintFunctions
from TC_Common.CreateTCcommon import etm_create_process

from UnitScripts.Log_script import Logger
import os
import re
import pandas as pd
import math


class ExcelCreation():
    def __init__(self, debug=False, path_tmp=None):
        self.log_object = Logger(debug, name="log_file_Excel.html")
        # ************ PATHS INITIALIZATION ************
        if path_tmp is None:
            return None
        self.path_tmp = path_tmp
        
        self.excel_tc_info = []

    def get_excel_cell(self, row, col, args):
        cell = row.get(col, args)
        try:
            if math.isnan(cell):
                cell = ''
        except:
            return cell
        return cell

    def read_excel_file(self, file):
        class MappingObjectTemp():
            def __init__(self):
                self.test_cases_sections = []
                self.test_cases_categories = []
                self.test_cases_attributes = []
        class TestScript():
            def __init__(self):
                self.test_step = ''
                self.expected_result = ''
        if re.match(r'.*\.xlsx', file):
            df = pd.read_excel(file)
        elif re.match(r'.*\.csv', file):
            df = pd.read_csv(file)
        # Identificar las columnas que corresponden a sections, categories y attributes
        sections_columns = [col for col in df.columns if col.startswith('Section:')]
        categories_columns = [col for col in df.columns if col.startswith('Category:')]
        attributes_columns = [col for col in df.columns if col.startswith('Attribute:')]

        # Obtener los nombres sin prefijos para inicializar los diccionarios
        sections = [col.split(':')[1] for col in sections_columns]
        categories = [col.split(':')[1] for col in categories_columns]
        attributes = [col.split(':')[1] for col in attributes_columns]

        mapping_obj = MappingObjectTemp()
        mapping_obj.test_cases_sections = sections
        mapping_obj.test_cases_categories = categories
        mapping_obj.test_cases_attributes = attributes

        # Inicializar el objeto TestCasesInfo
        test_cases_info = TestCasesInfo(mapping_obj, self.log_object)

        for _, row in df.iterrows():
            if self.get_excel_cell(row, 'Title', '') != '':
                test_case = test_cases_info.new_test_case()

                # Llenar tcid, title y description
                test_case.tcid = self.get_excel_cell(row, 'ID', '')
                test_case.title = self.get_excel_cell(row, 'Title', '')
                test_case.description = self.get_excel_cell(row, 'Description', '')
                test_case.state = self.get_excel_cell(row, 'State', '')

                tp_title = self.get_excel_cell(row, 'Test Plan', '')
                ts_title = self.get_excel_cell(row, 'Test Suite', '')
                if tp_title.strip().isdigit():
                    tp_input_type = 'ID'
                else:
                    tp_input_type = 'Name'
                if ts_title.strip().isdigit():
                    ts_input_type = 'ID'
                else:
                    ts_input_type = 'Name'
                tp_object = test_cases_info.tp_ts_obj(tp_title, tp_input_type)
                ts_object = test_cases_info.tp_ts_obj(ts_title, ts_input_type)
                test_case.tp_obj = tp_object
                test_case.ts_obj = ts_object
                
                # Llenar los diccionarios sections, categories y attributes
                for section in sections_columns:
                    if section.split(':')[1] == 'Test Scripts':
                        if 'Expected Results' in df.columns:
                            test_scripts = []
                            test_script = {}
                            test_script["test_step"] = str(self.get_excel_cell(row, section, ''))
                            test_script["expected_result"] = str(self.get_excel_cell(row, 'Expected Results', ''))
                            test_scripts.append(test_script)
                            test_case.sections[section.split(':')[1]] = test_scripts
                        else:
                            test_scripts = []
                            test_script = {}
                            content = str(self.get_excel_cell(row, section, ''))
                            for line in content.split(';'):
                                test_script = {}
                                try: 
                                    test_script["test_step"] = line.split('=')[0]
                                except:
                                    test_script["test_step"] = line
                                try:
                                    test_script["expected_result"] = line.split('=')[1]
                                except:
                                    test_script["expected_result"] = ''
                                test_scripts.append(test_script)
                    else:
                        test_case.sections[section.split(':')[1]] = str(self.get_excel_cell(row, section, ''))
                for category in categories_columns:
                    test_case.categories[category.split(':')[1]] = str(self.get_excel_cell(row, category, ''))
                    print(f"{cmd_colors.YELLOW}Category: {category.split(':')[1]}{cmd_colors.END}")
                for attribute in attributes_columns:
                    test_case.attributes[attribute.split(':')[1]] = str(self.get_excel_cell(row, attribute, ''))

                test_case.sections['Test Scripts'] = test_scripts
                test_cases_info.add_test_case(test_case)
            
            else:
                if isinstance(test_case.sections['Test Scripts'], list):
                    test_case = test_cases_info.test_cases[-1]
                    test_scripts = test_case.sections['Test Scripts']
                    test_script = {}
                    test_script["test_step"] = str(self.get_excel_cell(row, 'Section:Test Scripts', ''))
                    test_script["expected_result"] = str(self.get_excel_cell(row, 'Expected Results', ''))
                    test_scripts.append(test_script)
                    test_case.sections['Test Scripts'] = test_scripts
                    test_cases_info.test_cases[-1] = test_case

        return test_cases_info

    def create_excel_test_cases(self, qm_context, file, recycle=False, id_list=None, config=None, context_factory=None):
        PrintFunctions.print_header("CREATE EXCEL TEST CASES")
        test_cases_info = self.read_excel_file(file)
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
