
import os
import time
import json
import copy
from TC_Common.SelectorCmd import CMDSelector
from TC_Common.SelectorCmd import Terminal
from TC_Common.SelectorCmd import cmd_colors
from TC_Common.CreateTCcommon import val_field
from heppy.qm.test_step import TestStepTuple

class TestCasesInfo():
    class TestCaseData():
        def __init__(self, sections, categories, attributes):
            self.tcid = ""
            self.title = ""
            self.description = ""
            self.state = ""
            self.sections = copy.deepcopy(sections)
            self.categories = copy.deepcopy(categories)
            self.attributes = copy.deepcopy(attributes)
            self.tp_obj = {}
            self.ts_obj = {}
    class tp_ts_obj():
        def __init__(self, name, type_input):
            self.name = name
            self.type = type_input

    def __init__(self, mapping_obj, log_object):
        self.log_object = log_object
        self.test_cases = []
        self.sections_dict = {}
        self.categories_dict = {}
        self.attributes_dict = {}

        self.define_sections(mapping_obj.test_cases_sections)
        self.define_categories(mapping_obj.test_cases_categories)
        self.define_attributes(mapping_obj.test_cases_attributes)

    # def print_message(self, type="INFO", function="", msg="", print_prefix="", log=None):
    #     if type == "INFO":
    #         print(f"{print_prefix}{msg}")
    #         if log:
    #             log(f"{print_prefix}{msg}")
    #     elif type == "FATAL":
    #         print(f"{print_prefix}{cmd_colors.RED}Fatal Error.{cmd_colors.END} |{function}| {msg}")
    #         if log:
    #             log(f"{print_prefix}{cmd_colors.RED}Fatal Error.{cmd_colors.END} |{function}| {msg}")
    #         time.sleep(.2)
    #     elif type == "ERROR":
    #         print(f"{print_prefix}{cmd_colors.RED}Error:{cmd_colors.END} |{function}| {msg}")
    #         if log:
    #             log(f"{print_prefix}{cmd_colors.RED}Error:{cmd_colors.END} |{function}| {msg}")
    #         time.sleep(.1)
    #     elif type == "RESULT":
    #         print(f"{print_prefix}{cmd_colors.BLUE}Result:{cmd_colors.END} |{function}| {msg}")
    #         if log:
    #             log(f"{print_prefix}{cmd_colors.BLUE}Result:{cmd_colors.END} |{function}| {msg}")
    #         if debug_creation_test_case:
    #             key_to_continue = input(f"Press ENTER to continue...")
    #     elif type == "WARNING":
    #         print(f"{print_prefix}{cmd_colors.YELLOW}Warning:{cmd_colors.END} |{function}| {msg}")
    #         if log:
    #             log(f"{print_prefix}{cmd_colors.YELLOW}Warning:{cmd_colors.END} |{function}| {msg}")
    #         time.sleep(.1)
    #     elif type == "ABORTED":
    #         print(f"{print_prefix}{cmd_colors.RED}Error (Action Aborted):{cmd_colors.END} |{function}| {msg} {cmd_colors.RED}Action Cancelled.{cmd_colors.END}")
    #         if log:
    #             log(f"{print_prefix}{cmd_colors.RED}Error (Action Aborted):{cmd_colors.END} |{function}| {msg} {cmd_colors.RED}Action Cancelled.{cmd_colors.END}")
    #         time.sleep(.2)

    def define_sections(self, sections):
        sections = sections
        self.sections_dict = {section: [] for section in sections}
    def define_categories(self, categories):
        categories = categories
        self.categories_dict = {category: [] for category in categories}
    def define_attributes(self, attributes):
        attributes = attributes
        self.attributes_dict = {attribute: [] for attribute in attributes}

    def new_test_case(self):
        return self.TestCaseData(self.sections_dict, self.categories_dict, self.attributes_dict)

    def add_test_case(self, test_case):
        self.test_cases.append(test_case)

    def get_tc_from_json(self, path):
        with open(path, "r", encoding="utf-8") as fl:
            test_cases = json.load(fl)
        test_cases_list = []
        for test_case in test_cases:
            tc = self.new_test_case()
            tc.tcid = test_case["tcid"]
            tc.title = test_case["title"]
            tc.description = test_case["description"]
            tc.state = test_case["state"]
            tc.sections = test_case["sections"]
            tc.categories = test_case["categories"]
            tc.attributes = test_case["attributes"]
            tc.tp_obj = test_case["tp_obj"]
            tc.ts_obj = test_case["ts_obj"]
            test_cases_list.append(tc)
        return test_cases_list

    def save_tc_in_json(self, path, file):
        def obj_dict(obj):
            return obj.__dict__
        
        json_string = json.dumps(self.test_cases, default=obj_dict, indent=4, ensure_ascii=False)
        filename = f"{path}/{file}.json"
        with open(filename, "w+", encoding="utf-8") as fl:
            fl.write(json_string)
    
    def link_mapp_element_to_tc(self, element_tc, test_case):
        test_case.title = element_tc["Title"]["content"]
        test_case.description = element_tc["Description"]["content"]
        test_case.state = element_tc["State"]["content"]
        for section in element_tc["Sections"]:
            test_case.sections[section] = element_tc["Sections"][section]["content"]
        for category in element_tc["Categories"]:
            test_case.categories[category] = element_tc["Categories"][category]["content"]
        for attribute in element_tc["Attributes"]:
            test_case.attributes[attribute] = element_tc["Attributes"][attribute]["content"]
        return test_case
    
    def link_clean_to_tc(self, clean, test_case):
        test_case.title = clean["Title"]["default"]
        test_case.description = clean["Description"]["default"]
        test_case.state = clean["State"]["default"]
        for section in clean["Sections"]:
            test_case.sections[section] = clean["Sections"][section]["default"]
        for category in clean["Categories"]:
            test_case.categories[category] = clean["Categories"][category]["default"]
        for attribute in clean["Attributes"]:
            test_case.attributes[attribute] = clean["Attributes"][attribute]["default"]
        return test_case
    
    def get_t_ps_id_or_name(self, type, qm_context):
        t_ps_input_type_selector = CMDSelector()
        t_ps_input_type_selector_title = f"{"TEST PLAN" if type == "TP" else "TEST SUITE"}\nDo you want provide the ID or Name for the {type}?\n (None to ignore)"
        t_ps_input_type_selector.title = t_ps_input_type_selector_title
        t_ps_input_type_selector.options = ["ID", "Name", "None", "Cancel"]
        t_ps_input_type = t_ps_input_type_selector.select()
        if t_ps_input_type == "Cancel":
            return None
        os.system('')
        Terminal.save_screen()
        print(f"************************* CREATE TEST CASE *************************")
        print(f" Please Enter the {"Test Plan" if type == "TP" else "Test Suite"} '{t_ps_input_type}' for the Test Cases")
        if t_ps_input_type == "ID" or t_ps_input_type == "Name":
            retry_counter = 0
            while True:
                retry_counter += 1
                if retry_counter > 3:
                    selection = CMDSelector()
                    selection.title = f"Retry limit reached. Do you want to Cancel?"
                    selection.options = ["Retry", "Cancel"]
                    selection = selection.select()
                    if selection == "Cancel":
                        os.system('cls')
                        return None
                    retry_counter = 0
                t_ps_title = input(f" Test {"Plan" if type == "TP" else "Suite"}: ")
                if t_ps_title == "":
                    self.log_object.justprint_message("ERROR", "get_t_ps_id_or_name", f"Test {"Plan" if type == "TP" else "Suite"} cannot be empty. Try again.", print_prefix="\t")
                    continue
                if t_ps_input_type == "ID":
                    if not t_ps_title.isdigit():
                        self.log_object.justprint_message("ERROR", "get_t_ps_id_or_name", "Test Plan ID must be a number. Try again.", print_prefix="\t")
                        continue
                    try:
                        test_ps_etm = qm_context.test_plans().test_plan_by_database_id(t_ps_title) if type == "TP" else qm_context.test_suites().test_suite_by_database_id(t_ps_title)
                    except Exception as error:
                        self.log_object.justprint_message("FATAL", "get_t_ps_id_or_name", "Connection to ETM failed.", print_prefix="\t")
                        return None
                    if test_ps_etm:
                        break
                    else:
                        self.log_object.justprint_message("ERROR", "get_t_ps_id_or_name", f"Test Plan not found by ID: {t_ps_title}. Try again.", print_prefix="\t")
                        continue
                elif t_ps_input_type == "Name":
                    break
        elif t_ps_input_type == "None":
            t_ps_title = ""
        Terminal.restore_screen()
        t_ps_obj = self.tp_ts_obj(t_ps_title, t_ps_input_type)
        return t_ps_obj
    
    def etm_clean_test_case(self, qm_context, test_case, title, foreign_id, print_prefix=""):
        tp_title = input(f"{print_prefix}  Test Plan ID to remove (Empty to ignore): ")
        ts_title = input(f"{print_prefix}  Test Suite ID to remove (Empty to ignore): ")
        tc_clean = self.new_test_case()
        # Read CleanTestCase.json
        with open(f"{os.path.dirname(__file__)}/../UnitScripts/CleanTestCase.json", "r", encoding="utf-8") as file:
            mapping_to_clean = json.load(file)
            self.link_clean_to_tc(mapping_to_clean["TestCaseFormat"], tc_clean)
        if ts_title != "":
            self.etm_remove_tc_from_t_sp(qm_context, "TS", ts_title, test_case, print_prefix)
        if tp_title != "":
            self.etm_remove_tc_from_t_sp(qm_context, "TP", tp_title, test_case, print_prefix)
        test_case = self.etm_fill_test_case(qm_context, tc_clean, test_case, title_action="Clean", print_prefix=print_prefix)
        return test_case

    def etm_recycle_test_case(self, qm_context, id=None, title=None, foreign_id=None, print_prefix=""):
        if title is None:
            self.log_object.print_message("ABORTED", "etm_recycle_test_case", "Not Title provided.", print_prefix)
            return None
        if val_field(id):
            test_case = self.etm_find_test_case(qm_context, id=id, print_prefix=print_prefix)
            if test_case:
                test_case = self.etm_clean_test_case(qm_context, test_case, title, foreign_id, print_prefix=print_prefix)
                self.log_object.print_and_log("")
                return test_case
            else:
                selection = CMDSelector()
                selection.title = f"Test Case with ID: {id} not found.\nDo you want to create a new Test Case\n\n(A new ID will be assigned)?"
                selection.options = ["Create New", "Cancel"]
                key_to_continue = selection.select()
                if key_to_continue == "Create New":
                    return self.etm_new_test_case(qm_context, None, title, foreign_id, print_prefix=print_prefix)
                else:
                    return None
        else:
            self.log_object.print_message("ABORTED", "etm_recycle_test_case", "Not ID provided.", print_prefix)
            return None

    def etm_force_new_test_case(self, qm_context, title=None, foreign_id=None, print_prefix=""):
        if title is None:
            key_to_continue = input(f"{print_prefix}{cmd_colors.RED}Fatal error:{cmd_colors.END} Test Case Title not found.")
            time.sleep(.2)
            return None
        if val_field(title):
            try:
                new_test_case = qm_context.test_cases().create_new_test_case(title)
                self.log_object.print_message("RESULT", "etm_force_new_test_case", f"Test Case created with Title: {title}", print_prefix)
                return new_test_case
            except Exception as error:
                self.log_object.print_message("FATAL", "etm_force_new_test_case", "Connection to ETM failed.", print_prefix)

    def etm_new_test_case(self, qm_context, id=None, title=None, foreign_id=None, print_prefix=""):
        if title is None:
            self.log_object.print_message("ERROR", "etm_new_test_case", "Test Case Title not found.", print_prefix)
            return None
        if val_field(id):
            recycle_input = CMDSelector()
            recycle_input.title = f"WARNING: You provided an ID ({id}) to create a new Test Case.\nDo you want to recycle the ID or Try Again ignoring the ID?"
            recycle_input.options = ["Recycle", "Try Again"]
            recycle_input = recycle_input.select()
            self.log_object.print_and_log("")
            if recycle_input == "Recycle":
                self.log_object.print_message("INFO", "etm_new_test_case", f"- You selected to recycle the ID: {id}", print_prefix)
                return self.etm_recycle_test_case(qm_context, id, title, foreign_id, print_prefix=print_prefix)
            elif recycle_input == "Try Again":
                self.log_object.print_message("INFO", "etm_new_test_case", "- You selected to Try Again.", print_prefix)
                return self.etm_new_test_case(qm_context, None, title, foreign_id, print_prefix=print_prefix)
            else:
                return None
        elif val_field(title):
            test_case = self.etm_find_test_case(qm_context, title=title, print_prefix=print_prefix)
            if test_case:
                recycle_input = CMDSelector()
                recycle_input.title = f"WARNING: A Test Case with Title: '{title}' already exists.\n\nDo you want to:\n • RECYCLE the ID\n • Create a new Test Case with DUPLICATED Title or\n • Cancel"
                recycle_input.options = ["Recycle", "Create Duplicate", "Cancel"]
                recycle_input = recycle_input.select()
                self.log_object.print_and_log("")
                if recycle_input == "Recycle":
                    self.log_object.print_message("INFO", "etm_new_test_case", f"- You selected to recycle the ID: {test_case.database_id()}", print_prefix)
                    return self.etm_recycle_test_case(qm_context, test_case.database_id(), title, foreign_id, print_prefix=print_prefix)
                elif recycle_input == "Create Duplicate":
                    self.log_object.print_message("INFO", "etm_new_test_case", f"- You selected to create a duplicate Test Case.", print_prefix)
                    return self.etm_force_new_test_case(qm_context, title, foreign_id, print_prefix=print_prefix)
                elif recycle_input == "Cancel":
                    return None
            else:
                try:
                    new_test_case = qm_context.test_cases().create_new_test_case(title)
                    self.log_object.print_message("RESULT", "etm_new_test_case", f"Test Case created with Title: {title}", print_prefix)
                    return new_test_case
                except Exception as error:
                    self.log_object.print_message("FATAL", "etm_new_test_case", "Connection to ETM failed.", print_prefix)
                    return None
                
    def etm_find_test_case(self, qm_context, id=None, title=None, foreign_id=None, print_prefix=""):
        if val_field(id):
            self.log_object.print_message("INFO", "etm_find_test_case", f"Searching Test Case by ID: {id} ...", print_prefix)
            self.log_object.print_message("INFO", "etm_find_test_case", "--- Please wait...", print_prefix)
            try:
                test_case = qm_context.test_cases().test_case_by_database_id(id)
            except Exception as error:
                self.log_object.print_message("FATAL", "etm_find_test_case", "Connection to ETM failed.", print_prefix)
                return None
            if test_case is not None:
                self.log_object.print_message("RESULT", "etm_find_test_case", f"Test Case found with ID: {id}", print_prefix)
                return test_case
            else:
                self.log_object.print_message("RESULT", "etm_find_test_case", f"Test Cases not found with ID: {id}", print_prefix)
                return None
        elif val_field(title):
            self.log_object.print_message("INFO", "etm_find_test_case", f"Searching Test Case by Name: {id} ...", print_prefix)
            self.log_object.print_message("INFO", "etm_find_test_case", "--- Please wait...", print_prefix)
            try:
                test_cases = qm_context.test_cases().test_cases_by_name(title)
            except Exception as error:
                self.log_object.print_message("FATAL", "etm_find_test_case", "Connection to ETM failed.", print_prefix)
                return None
            if len(test_cases) == 1:
                self.log_object.print_message("RESULT", "etm_find_test_case", f"Test Case found with Title: {title}", print_prefix)
                return test_cases[0]
            elif len(test_cases) > 1:
                tc_index_selector = CMDSelector()
                tc_index_selector.title = f"Multiple Test Cases found ({len(test_cases)}) with title: {title}\nPlease select the Test Case to continue:"
                options = [f"ID: {tc.database_id()} > {tc.name()}" for tc in test_cases]
                tc_index_selector.options = options
                tc_index = tc_index_selector.select()
                self.log_object.print_message("RESULT", "etm_find_test_case", f"Test Case found with Title: {title}", print_prefix)
                return test_cases[tc_index]
            else:
                self.log_object.print_message("RESULT", "etm_find_test_case", f"No previous Test Cases found with Title: {title}", print_prefix)
                return None
        elif val_field(foreign_id):
            self.log_object.print_message("INFO", "etm_find_test_case", f"Searching Test Case by Foreign ID: {foreign_id} ...", print_prefix)
            self.log_object.print_message("INFO", "etm_find_test_case", "--- Please wait...", print_prefix)
            try:
                test_cases = qm_context.test_cases().test_cases_by_foreign_id(foreign_id)
            except Exception as error:
                self.log_object.print_message("FATAL", "etm_find_test_case", "Connection to ETM failed.", print_prefix)
                return None
            if len(test_cases) == 1:
                self.log_object.print_message("RESULT", "etm_find_test_case", f"Test Case found with Foreign ID: {foreign_id}", print_prefix)
                return test_cases[0]
            elif len(test_cases) > 1:
                tc_index_selector = CMDSelector()
                tc_index_selector.title = f"Multiple Test Cases found ({len(test_cases)}) with Foreign ID: {foreign_id}\nPlease select the Test Case to continue:"
                options = [f"ID: {tc.database_id()} > {tc.name()}" for tc in test_cases]
                tc_index_selector.options = options
                tc_index = tc_index_selector.select()
                self.log_object.print_message("RESULT", "etm_find_test_case", f"Test Case found with Foreign ID: {foreign_id}", print_prefix)
                return test_cases[tc_index]
            else:
                self.log_object.print_message("RESULT", "etm_find_test_case", f"No previous Test Cases found with Foreign ID: {foreign_id}", print_prefix)
                return None
        else:
            self.log_object.print_message("ABORTED", "etm_find_test_case", f"ID, Title or Foreign ID not found.", print_prefix)
            return None

    def etm_set_title(self, qm_context, test_case_data, testcase, print_prefix=""):
        if testcase is None:
            self.log_object.print_message("ABORTED", "etm_set_title", "Not Test Case provided.", print_prefix)
            return None
        if test_case_data.title:
            try:
                testcase.set_name(test_case_data.title)
                testcase.store()
                self.log_object.print_message("SUCCESS", "etm_set_title", f"Test Case Title set: {test_case_data.title}", print_prefix)
                return testcase
            except Exception as error:
                self.log_object.print_message("FATAL", "etm_set_title", "Connection to ETM failed.", print_prefix)
                return None
        return None
    
    def etm_remove_tc_from_t_sp(self, qm_context, type, t_sp_id, testcase, print_prefix=""):
        if testcase is None:
            self.log_object.print_message("ABORTED", "etm_set_title", "Not Test Case provided.", print_prefix)
            return None
        if t_sp_id:
            try:
                test_sp_etm = qm_context.test_suites().test_suite_by_database_id(t_sp_id) if type == "TS" else qm_context.test_plans().test_plan_by_database_id(t_sp_id)
                if test_sp_etm:
                    try:
                        test_sp_etm.remove_test_case(testcase)
                        test_sp_etm.store()
                        self.log_object.print_message("RESULT", "etm_remove_tc_from_t_sp", f"Test Case removed from {type}: {t_sp_id}", print_prefix)
                        return testcase
                    except Exception as error:
                        self.log_object.print_message("FATAL", "etm_remove_tc_from_t_sp", "Connection to ETM failed.", print_prefix)
                        return None
                else:
                    self.log_object.print_message("ERROR", "etm_remove_tc_from_t_sp", f"{type} not found by ID: {t_sp_id}", print_prefix)
                    return None
            except Exception as error:
                self.log_object.print_message("FATAL", "etm_remove_tc_from_t_sp", "Connection to ETM failed.", print_prefix)
                return None
        else:
            self.log_object.print_message("ERROR", "etm_remove_tc_from_t_sp", f"{type} ID not provided.", print_prefix)
            return None
    
    def etm_set_t_sp(self, qm_context, type, test_case_data, testcase, print_prefix="", test_suite=None):
        if testcase is None:
            self.log_object.print_message("ABORTED", "etm_set_t_sp", "Not Test Case provided.", print_prefix)
            return ((None, None) if type == "TS" else testcase)
        tc_title = test_case_data.title
        tc_id = testcase.database_id()
        t_sp_title_obj = test_case_data.ts_obj if type == "TS" else test_case_data.tp_obj
        t_sp_title = t_sp_title_obj.name
        if t_sp_title_obj.type == "None":
            return ((testcase, None) if type == "TS" else testcase)
        # ************ SEARCH TEST SUITE/PLAN in ETM Database ************
        if t_sp_title:
            if t_sp_title_obj.type == "Remove":
                testcase = self.etm_remove_tc_from_t_sp(qm_context, type, t_sp_title, testcase, print_prefix)
                return ((testcase, None) if type == "TS" else testcase)
            if t_sp_title_obj.type == "ID":
                try:
                    test_sp_etm = qm_context.test_suites().test_suite_by_database_id(t_sp_title) if type == "TS" else qm_context.test_plans().test_plan_by_database_id(t_sp_title)
                except Exception as error:
                    self.log_object.print_message("FATAL", "etm_set_t_sp", "Connection to ETM failed.", print_prefix)
                    return ((None, None) if type == "TS" else testcase)
                if test_sp_etm:
                    self.log_object.print_message("RESULT", "etm_set_t_sp", f"{type} found. ID: {test_sp_etm.database_id()} Title: {test_sp_etm.name()}", print_prefix)
                else:
                    self.log_object.print_message("ERROR", "etm_set_t_sp", f"{type} not found by ID: {t_sp_title}. {cmd_colors.RED}Action Cancelled.{cmd_colors.END}", print_prefix)
                    return ((None, None) if type == "TS" else testcase)
            elif t_sp_title_obj.type == "Name":
                try:
                    test_sp_etm_array = qm_context.test_suites().bulk_fetch(f'title="{t_sp_title}"') if type == "TS" else qm_context.test_plans().bulk_fetch(f'title="{t_sp_title}"')
                except Exception as error:
                    self.log_object.print_message("FATAL", "etm_set_t_sp", "Connection to ETM failed.", print_prefix)
                    return ((None, None) if type == "TS" else testcase)
                if test_sp_etm_array:
                    if len(test_sp_etm_array) > 1:
                        self.log_object.print_message("WARNING", "etm_set_t_sp", f"Multiple {type} found with title: {t_sp_title}", print_prefix)
                        dict_test_sp = {}
                        array_test_sp = {}
                        for ts in test_sp_etm_array:
                            array_test_sp[f"ID: {ts.database_id()} > {ts.name()}"] = ts.database_id()
                            array_test_sp.append(f"ID: {ts.database_id()} > {ts.name()}")
                        selector_test_sp = CMDSelector()
                        selector_test_sp.title = f"Multiple {type} found with title: {t_sp_title}\nPlease select the Test Suite to continue:"
                        selector_test_sp.options = array_test_sp
                        test_suite_selected = selector_test_sp.select()
                        test_sp_etm = qm_context.test_suites().test_suite_by_database_id(dict_test_sp[test_suite_selected]) if type == "TS" else qm_context.test_plans().test_plan_by_database_id(dict_test_sp[test_suite_selected])
                    test_sp_etm = test_sp_etm_array[0]
                    self.log_object.print_message("RESULT", "etm_set_t_sp", f"{type} found. ID: {test_sp_etm.database_id()} Title: {test_sp_etm.name()}", print_prefix)
                else:
                    self.log_object.print_message("RESULT", "etm_set_t_sp", f"{type} not found by Name: {t_sp_title}", print_prefix)
                    test_sp_etm = None
        # • • • • • • • ♦ ♦ ♦ ♦ ♦ ♦ ♦ ♦ ♦ ♦ ♦ • • • • • • •

        # ************ CREATE TEST SUITE/PLAN in ETM Database ************
        if test_sp_etm is None:
            if t_sp_title_obj.type == "Name":
                try:
                    test_sp_etm = qm_context.test_suites().create_test_suite(t_sp_title) if type == "TS" else qm_context.test_plans().create_new_test_plan(t_sp_title)
                    self.log_object.print_message("RESULT", "etm_set_t_sp", f"{type} created with title: {t_sp_title}", print_prefix)
                except Exception as error:
                    self.log_object.print_message("FATAL", "etm_set_t_sp", "Connection to ETM failed.", print_prefix)
                    return ((None, None) if type == "TS" else testcase)
        # • • • • • • • ♦ ♦ ♦ ♦ ♦ ♦ ♦ ♦ ♦ ♦ ♦ • • • • • • •

        # ************ SET TEST SUITE/PLAN in ETM Database ************
        if testcase not in test_sp_etm.test_cases():
            try:
                if type == "TS":
                    test_sp_etm.append_test_case(testcase)
                elif type == "TP":
                    test_sp_etm.add_test_case(testcase)
                if test_suite:
                    test_sp_etm.add_test_suite(test_suite)
                test_sp_etm.store()
                self.log_object.print_message("RESULT", "etm_set_t_sp", f"Test Case added to {type}: {t_sp_title}", print_prefix)
            except Exception as error:
                self.log_object.print_message("FATAL", "etm_set_t_sp", "Connection to ETM failed.", print_prefix)
                return ((None, None) if type == "TS" else testcase)
        return ((testcase, test_sp_etm) if type == "TS" else testcase)

    def create_test_script(self, qm_context, tc_title, tc_script, test_script=None, print_prefix=""):
        class TestScript():
            def __init__(self):
                self.test_step = ''
                self.expected_result = ''
        try:
            test_step_list = list()

            if isinstance(tc_script, str):
                for test_step in tc_script.split(';'):
                    description = test_step.split('=')[0]
                    expexted_result = test_step.split('=')[1]
                    test_step_list.append(TestStepTuple(description, expexted_result))
            elif isinstance(tc_script, list):
                for test_step in tc_script:
                    if isinstance(test_step, dict):
                        test_step_list.append(TestStepTuple(test_step["test_step"], test_step["expected_result"]))
                    elif isinstance(test_step, str):
                        description = test_step.split('=')[0]
                        expexted_result = test_step.split('=')[1]
                        test_step_list.append(TestStepTuple(description, expexted_result))
            if len(test_step_list) == 0:
                print(f"{print_prefix}{cmd_colors.BLUE}    Test Script{cmd_colors.END} is empty.")
                return test_script
            else:
                print(f"{print_prefix}{cmd_colors.BLUE}    Test Script{cmd_colors.END} created with {len(test_step_list)} steps.")
                for tstep in test_step_list:
                    print(f"{print_prefix}\t - Description: {tstep.description} | Expected results: {tstep.expected_result}")

            if not test_script:
                created_test_script = qm_context.test_scripts().create_manual_test_script(tc_title, test_step_list)
                created_test_script.store()

                return created_test_script

            else:
                for tstep in test_script.test_steps():
                    test_script.test_steps().remove_step(tstep)

                for tstep in test_step_list:
                    test_script.test_steps().append_new_step(tstep)

                test_script.store()

                return test_script

        except Exception as error:
            return f"Error. TScript: {tc_title} Reason: {error}"

    def etm_fill_test_case(self, qm_context, test_case_data, testcase, title_action="Fill", print_prefix="", config=None, context_factory=None):
        errors_count = 0
        success_count = 0
        fatal_count = 0
        print_active = False if title_action == "Clean" else True
        if testcase is None:
            self.log_object.print_message("ABORTED", "etm_fill_test_case", "Not Test Case provided.", print_prefix, active=print_active)
            return None
        def print_header_page(title_action):
            os.system('cls')
            if title_action == "Fill":
                print(f"************************* FILLING TEST CASE DATA *************************")
            elif title_action == "Clean":
                print("************************* CLEANING TEST CASES TO RECYCLE *************************")
                print("Please wait...")
        if title_action == "Clean":
            self.log_object.justlog_message("INFO", "etm_fill_test_case", "Test Case Cleaned", print_prefix)
        try:
            print_header_page(title_action)
            self.log_object.print_and_log(f"\n{cmd_colors.GREEN}Updating DESCRIPTION{cmd_colors.END} in TC: {testcase.name()}", print_prefix="    ", active=print_active)
            testcase.set_description(test_case_data.description)
            testcase.store()
            self.log_object.print_message("SUCCESS", "etm_fill_test_case", "Updated DESCRIPTION", print_prefix, active=print_active)
            success_count += 1
        except Exception as error:
            self.log_object.print_message("ERROR", "etm_fill_test_case", f"Error saving {cmd_colors.RED}DESCRIPTION{cmd_colors.END}", print_prefix, active=print_active)
            errors_count += 1
        time.sleep(.1)

        try:
            self.log_object.print_and_log(f"\n{cmd_colors.GREEN}Updating STATE{cmd_colors.END} in TC: {testcase.name()}", print_prefix="    ", active=print_active)
            testcase.set_state(test_case_data.state)
            testcase.store()
            self.log_object.print_message("SUCCESS", "etm_fill_test_case", "Updated STATE", print_prefix, active=print_active)
            success_count += 1
        except Exception as error:
            self.log_object.print_message("ERROR", "etm_fill_test_case", f"Error saving {cmd_colors.RED}STATE{cmd_colors.END}", print_prefix, active=print_active)
            errors_count += 1
        time.sleep(.1)
        
        try:
            self.log_object.print_and_log(f"\n{cmd_colors.GREEN}Updating SECTIONS{cmd_colors.END} in TC: {testcase.name()}", print_prefix="    ", active=print_active)
            local_success_count = 0
            for section in test_case_data.sections:
                if section == "Test Scripts":
                    try:
                        test_script_etm = qm_context.test_scripts().bulk_fetch(f'title="{test_case_data.title}"')

                        if test_script_etm:
                            if title_action == "Clean":
                                try:
                                    for ts in test_script_etm:
                                        # Remove Test Scripts from Test Case
                                        testcase.remove_linked_test_script(ts)
                                        testcase.store()
                                    self.log_object.print_message("SUCCESS", "etm_fill_test_case", f"Updated SECTION - {section}", print_prefix, active=print_active)
                                    success_count += 1
                                    # skip to next section
                                    continue
                                except Exception as error:
                                    self.log_object.print_message("ERROR", "etm_fill_test_case", f"Error saving {cmd_colors.RED}SECTION - {section}{cmd_colors.END}", print_prefix, active=print_active)
                                    errors_count += 1
                                    # skip to next section
                                    continue
                            else:
                                test_script_etm = test_script_etm[0]
                                test_script_etm = self.create_test_script(qm_context, test_case_data.title, test_case_data.sections["Test Scripts"], test_script_etm, print_prefix)

                            if test_script_etm not in testcase.linked_test_scripts():
                                testcase.add_linked_test_script(test_script_etm)

                        else:
                            if title_action == "Clean":
                                self.log_object.print_message("SUCCESS", "etm_fill_test_case", f"Updated SECTION - {section}", print_prefix, active=print_active)
                                success_count += 1
                                # skip to next section
                                continue
                            test_script_etm = self.create_test_script(qm_context, test_case_data.title, test_case_data.sections["Test Scripts"], print_prefix=print_prefix)
                            if test_script_etm:
                                testcase.add_linked_test_script(test_script_etm)
                        
                        testcase.store()
                        self.log_object.print_message("SUCCESS", "etm_fill_test_case", f"Updated SECTION - {section}", print_prefix, active=print_active)
                        success_count += 1
                        local_success_count += 1
                    except Exception as error:
                        self.log_object.print_message("ERROR", "etm_fill_test_case", f"Error saving {cmd_colors.RED}SECTION - {section}{cmd_colors.END}", print_prefix, active=print_active)
                        errors_count += 1
                    time.sleep(.1)
                elif section == "Requirement Links":
                    requirement_list = list()
                    if isinstance(test_case_data.sections[section], str):
                        test_case_data.sections[section] = [test_case_data.sections[section]]
                    for req in test_case_data.sections[section]:
                        if isinstance(req, str) and req.isdigit() and int(req) > 0:
                            if config:
                                def get_qr_context():
                                    try:
                                        candidate_context = None

                                        for rm_context in context_factory.rm_contexts():
                                            if rm_context.local_configuration_name() == config.get('jazz_configuration', 'rm_stream_name'):
                                                candidate_context = rm_context
                                                break

                                        return candidate_context

                                    except Exception as ex:
                                        return None
                                try:
                                    rm_context = get_qr_context()
                                    req_obj = rm_context.requirements().requirement_by_database_id(int(req))
                                    if str(req_obj.type_uri()).split('/')[-1] == "requirement":
                                        reqLink = req_obj.element_url()
                                        requirement_list.append(reqLink)
                                except Exception as error:
                                    self.log_object.print_message("ERROR", "etm_fill_test_case", f"Error saving {cmd_colors.RED}SECTION - {section}{cmd_colors.END}", print_prefix, active=print_active)
                                    errors_count += 1
                                    continue
                            else:
                                self.log_object.print_message("ERROR", "etm_fill_test_case", f"Error saving {cmd_colors.RED}SECTION - {section}{cmd_colors.END}", print_prefix, active=print_active)
                                errors_count += 1
                        else:
                            requirement_list.append(req)
                    if len(requirement_list) == 0:
                        self.log_object.print_message("SUCCESS", "etm_fill_test_case", f"Updated SECTION - {section}", print_prefix, active=print_active)
                        continue
                    try:
                        testcase.set_linked_requirement_urls_and_store(requirement_list, False)
                        self.log_object.print_message("SUCCESS", "etm_fill_test_case", f"Updated SECTION - {section}", print_prefix, active=print_active)
                        success_count += 1
                        local_success_count += 1
                    except Exception as error:
                        self.log_object.print_message("ERROR", "etm_fill_test_case", f"Error saving {cmd_colors.RED}SECTION - {section}{cmd_colors.END}", print_prefix, active=print_active)
                        errors_count += 1
                    time.sleep(.1)
                elif section == "Confidential Comments" or section == "Attachments" or section == "Architecture Element Links" or section=="Development Items" or section=="Test Case Execution Records" or section=="Formal Review":
                    self.log_object.print_message("WARNING", "etm_fill_test_case", f"Section - {section} not implemented", print_prefix, active=print_active)
                    continue
                else:
                    try:
                        testcase.sections().set_value(section, test_case_data.sections[section], is_rich_text=False)
                        testcase.store()
                        self.log_object.print_message("SUCCESS", "etm_fill_test_case", f"Updated SECTION - {section}", print_prefix, active=print_active)
                        success_count += 1
                        local_success_count += 1
                    except Exception as error:
                        self.log_object.print_message("ERROR", "etm_fill_test_case", f"Error saving {cmd_colors.RED}SECTION - {section}{cmd_colors.END}", print_prefix, active=print_active)
                        errors_count += 1
                    time.sleep(.1)

            self.log_object.print_and_log("", active=print_active)
            self.log_object.print_message("SUCCESS", "etm_fill_test_case", "Updated SECTIONS", print_prefix, active=print_active)
        except Exception as error:
            if local_success_count == 0:
                fatal_count += 1
                self.log_object.print_and_log("", active=print_active)
                self.log_object.print_message("FATAL", "etm_fill_test_case", f"Error saving {cmd_colors.RED}SECTIONS{cmd_colors.END} in TestCase: {error}", print_prefix, active=print_active)
        
        try:
            self.log_object.print_and_log(f"\n{cmd_colors.GREEN}Updating CATEGORIES{cmd_colors.END} in TC: {testcase.name()}", print_prefix="    ", active=print_active)
            local_success_count = 0
            for category in test_case_data.categories:
                try:
                    testcase.custom_categories().set_value(category, test_case_data.categories[category])
                    testcase.store()
                    self.log_object.print_message("SUCCESS", "etm_fill_test_case", f"Updated CATEGORY - {category}", print_prefix, active=print_active)
                    success_count += 1
                    local_success_count += 1
                except Exception as error:
                    self.log_object.print_message("ERROR", "etm_fill_test_case", f"Error saving {cmd_colors.RED}CATEGORY - {category}{cmd_colors.END}", print_prefix, active=print_active)
                    errors_count += 1
                time.sleep(.1)
            self.log_object.print_and_log("", active=print_active)
            self.log_object.print_message("SUCCESS", "etm_fill_test_case", "Updated CATEGORIES", print_prefix, active=print_active)
        except Exception as error:
            if local_success_count == 0:
                fatal_count += 1
                self.log_object.print_and_log("", active=print_active)
                self.log_object.print_message("FATAL", "etm_fill_test_case", f"Error saving {cmd_colors.RED}CATEGORIES{cmd_colors.END} in TestCase: {error}", print_prefix, active=print_active)
        try:
            self.log_object.print_and_log(f"\n{cmd_colors.GREEN}Updating ATTRIBUTES{cmd_colors.END} in TC: {testcase.name()}", print_prefix="    ", active=print_active)
            local_success_count = 0
            for attribute in test_case_data.attributes:
                try:
                    testcase.custom_attributes().set_value(attribute, test_case_data.attributes[attribute])
                    testcase.store()
                    self.log_object.print_message("SUCCESS", "etm_fill_test_case", f"Updated ATTRIBUTE - {attribute}", print_prefix, active=print_active)
                    success_count += 1
                    local_success_count += 1
                except Exception as error:
                    self.log_object.print_message("ERROR", "etm_fill_test_case", f"Error saving {cmd_colors.RED}ATTRIBUTE - {attribute}{cmd_colors.END}", print_prefix, active=print_active)
                    errors_count += 1
                time.sleep(.1)
            self.log_object.print_and_log("", active=print_active)
            self.log_object.print_message("SUCCESS", "etm_fill_test_case", "Updated ATTRIBUTES", print_prefix, active=print_active)
        except Exception as error:
            if local_success_count == 0:
                fatal_count += 1
                self.log_object.print_and_log("", active=print_active)
                self.log_object.print_message("FATAL", "etm_fill_test_case", f"Error saving {cmd_colors.RED}ATTRIBUTES{cmd_colors.END} in TestCase: {error}", print_prefix, active=print_active)

        self.log_object.print_and_log("", active=print_active)
        if fatal_count == 0:
            if errors_count == 0:
                self.log_object.print_and_log(f"{cmd_colors.GREEN}Updating FINISHED SUCCESS{cmd_colors.END} Test Case '{testcase.name()}' filled: with {cmd_colors.GREEN}{success_count} success{cmd_colors.END}, {cmd_colors.RED}{errors_count} errors{cmd_colors.END}", print_prefix, active=print_active)
            elif errors_count > 0:
                self.log_object.print_and_log(f"{cmd_colors.GREEN}Updating FINISHED {cmd_colors.YELLOW}WITH ERRORS{cmd_colors.END} Test Case '{testcase.name()}' filled: with {cmd_colors.GREEN}{success_count} success{cmd_colors.END}, {cmd_colors.RED}{errors_count} errors{cmd_colors.END}", print_prefix, active=print_active)            
        else:
            self.log_object.print_and_log(f"{cmd_colors.RED}Updating FINISHED {cmd_colors.RED}WITH FATAL ERRORS{cmd_colors.END} Test Case '{testcase.name()}' filled: with {cmd_colors.GREEN}{success_count} success{cmd_colors.END}, {cmd_colors.RED}{errors_count} errors{cmd_colors.END}, {cmd_colors.RED}{fatal_count} fatal{cmd_colors.END}", print_prefix, active=print_active)
        time.sleep(.1)
        return testcase