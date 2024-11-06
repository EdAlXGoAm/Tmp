from TC_Common.FilesFunctions import select_file
from TC_Common.SelectorCmd import CMDSelector
from TC_Common.SelectorCmd import cmd_colors
from TC_Common.SelectorCmd import Terminal
from TC_Common.CreateTCcommon import val_field
from TC_Common.DictsFunctions import (
    recursive_evaluation_keys
)
import copy
import json
import re

class MappingClass():
    def __init__(self, path_mapping_files):
        self.path_mapping_files = path_mapping_files
        self.mapping_links = {}
        self.test_cases_sections = []
        self.test_cases_categories = []
        self.test_cases_attributes = []
        self.MappingClassError = False
        self.mapping_file = select_file(self.path_mapping_files, ".json", "MAPPING", recursive=True)
        if self.mapping_file == "Cancel":
            self.MappingClassError = True
            return
        with open(f"{self.mapping_file}", 'r', encoding="utf-8") as file:
            self.mapping_links = json.load(file)
            if self.mapping_links == "Cancel":
                self.MappingClassError = True
                return
        if self.get_arrays() == "Cancel":
            self.MappingClassError = True
            return

    def get_arrays(self):
        try:
            self.test_cases_sections = [section for section in self.mapping_links["TestCaseFormat"]["Sections"]]
            self.test_cases_categories = [category for category in self.mapping_links["TestCaseFormat"]["Categories"]]
            self.test_cases_attributes = [attribute for attribute in self.mapping_links["TestCaseFormat"]["Attributes"]]
        except KeyError:
            print(f"--- {cmd_colors.RED}ERROR:{cmd_colors.END} The MAPPING file is not well formatted.")
            return "Cancel"
        

    def generate_mapped_link(self, element, main_key, title, description, title_prefix_input=None):
        title_prefix = title_prefix_input if val_field(title_prefix_input) else ""
        mapping_link = copy.deepcopy(self.mapping_links)
        mapping_link[main_key]["Title"]["content"] = title
        mapping_link[main_key]["Description"]["content"] = description
        for tag_to_fill in element:
            quick_eval = recursive_evaluation_keys(mapping_link, [main_key, "Titles", tag_to_fill])
            if quick_eval:
                mapping_link[main_key]["Titles"][tag_to_fill]["content"] = element.get(tag_to_fill, '')
        
        # Mapping TITLE
        mapping_link["TestCaseFormat"]["Title"]["content"] = self.mapping_to_TestCaseFormat(main_key, "Title", mapping_link, title_prefix)
        # Mapping DESCRIPTION
        mapping_link["TestCaseFormat"]["Description"]["content"] = self.mapping_to_TestCaseFormat(main_key, "Description", mapping_link)
        # Mapping STATUS
        mapping_link["TestCaseFormat"]["State"]["content"] = self.mapping_to_TestCaseFormat(main_key, "State", mapping_link)
        # Mapping SECTIONS
        self.mapping_to_TestCaseFormat_Group("Sections", mapping_link, main_key)
        # Mapping CATEGORIES
        self.mapping_to_TestCaseFormat_Group("Categories", mapping_link, main_key)
        # Mapping ATTRIBUTES
        self.mapping_to_TestCaseFormat_Group("Attributes", mapping_link, main_key)

        return mapping_link
    
    def mapping_to_TestCaseFormat(self, main_key, key, mapping_link, prefix=None):
        if self.mapping_links["TestCaseFormat"][key]["content"] == []:
            return mapping_link["TestCaseFormat"][key]["default"]
        if prefix:
            content = prefix
        else:
            content = ""
        for array in self.mapping_links["TestCaseFormat"][key]["content"]:
            mapping_tmp = copy.deepcopy(mapping_link)
            for tag in array:
                mapping_tmp = mapping_tmp[tag]
            content += self.validation(key.upper(), mapping_tmp["content"], self.mapping_links["TestCaseFormat"][key]["validation"], mapping_link[main_key][key]["content"])
        return content
    
    def mapping_to_TestCaseFormat_Group(self, type_mapping, mapping_link, main_key):
        for mapping in self.mapping_links["TestCaseFormat"][type_mapping]:
            content = ""
            for array in self.mapping_links["TestCaseFormat"][type_mapping][mapping]["content"]:
                if isinstance(array, list) and len(array) == 1 and isinstance(array[0], str) and "'" in array[0]:
                    content += array[0].strip("'")  # Concatena el contenido del string sin comillas
                else:
                    mapping_tmp = copy.deepcopy(mapping_link)
                    for tag in array:
                        mapping_tmp = mapping_tmp[tag]
                    if mapping_tmp["type"] == "array":
                        if len(content) == 0:
                            content = self.validation(type_mapping.upper() + " " + mapping, mapping_tmp["content"], mapping_link["TestCaseFormat"][type_mapping][mapping]["validation"], mapping_link[main_key]["Title"]["content"])
                        else:
                            content.extend(self.validation(type_mapping.upper() + " " + mapping, mapping_tmp["content"], mapping_link["TestCaseFormat"][type_mapping][mapping]["validation"], mapping_link[main_key]["Title"]["content"]))
                    elif mapping_tmp["type"] == "string" and "\n".join(mapping_tmp["content"]) != "":
                        if content != "":
                            content += "\n"
                        if type(mapping_tmp["content"]) == list:
                            content += "\n".join(self.validation(type_mapping.upper() + " " + mapping, mapping_tmp["content"], mapping_link["TestCaseFormat"][type_mapping][mapping]["validation"], mapping_link[main_key]["Title"]["content"]))
                        else:
                            content += self.validation(type_mapping.upper() + " " + mapping, mapping_tmp["content"], mapping_link["TestCaseFormat"][type_mapping][mapping]["validation"], mapping_link[main_key]["Title"]["content"])
            if self.mapping_links["TestCaseFormat"][type_mapping][mapping]["content"]:
                mapping_link["TestCaseFormat"][type_mapping][mapping]["content"] = content
            else:
                mapping_link["TestCaseFormat"][type_mapping][mapping]["content"] = mapping_link["TestCaseFormat"][type_mapping][mapping]["default"]

    
    def validation(self, structure, content, validation, test_title):
        def regex_fix(structure, validation):
            Terminal.save_screen()
            print(f"{cmd_colors.YELLOW}WARNING{cmd_colors.END} - The content <<{content}>> not pass the validation <<{validation}>>")
            content_fixed = False
            while not content_fixed:
                content = input(f"Provide a new content for the {structure} (validation: {validation}): ")
                if re.search(validation, content):
                    content_fixed = True
                else:
                    print(f"{cmd_colors.RED}ERROR{cmd_colors.END} - The content <<{content}>> not pass the validation <<{validation}>> - Try again")
            Terminal.restore_screen()
            return content
        def array_fix(structure, validation, content):
            selection = CMDSelector()
            selection.title = f"WARNING - \nTEST CASE: {test_title}\nThe content <<{content}>>\nnot pass the validation \n<<{validation}>>\nSelect a new value for the {structure} in the list: "
            selection.options = validation
            content = selection.select()
            return content
        print(f"***** Validation of {structure} *****")
        if type(validation) == list:
            if type(content) == list:
                new_content = []
                for item in content:
                    valid = False
                    for val in validation:
                        if item == val:
                            valid = True
                        elif item.lower().strip() == val.lower().strip():
                            valid = True
                            item = val
                    if not valid:
                        item = array_fix(structure, validation, item)
                    new_content.append(item)
                content = new_content
            elif type(content) == str:
                valid = False
                for val in validation:
                    if content == val:
                        valid = True
                    elif content.lower().strip() == val.lower().strip():
                        valid = True
                        content = val
                if not valid:
                    content = array_fix(structure, validation, content)
            print(f"--- VALIDATION: {validation}")
            print(f"--- CONTENT: {content}")
        elif type(validation) == str:
            if re.search(r"^\'", validation):
                if not re.search(validation, content):
                    content = regex_fix(structure, validation)
                print(f"--- VALIDATION: {validation}")
                print(f"--- CONTENT: {content}")
        return content