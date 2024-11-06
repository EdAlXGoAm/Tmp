from TC_Common.SelectorCmd import cmd_colors
from TC_Common.SelectorCmd import CMDSelector
from TC_Common.SelectorCmd import Terminal
from TC_Common.CreateTCcommon import save_tc_in_json
import os
import json
import time
import re
import copy

delr = '\033[1A\033[K'
up = '\033[1A'

class RTFMapping():
    def __init__(self, path_tmp=None, rtf_scrapper=None, mapping_obj=None):
        if path_tmp is None:
            return None
        self.path_tmp = path_tmp
        self.rtf_titles = [title for title in mapping_obj.mapping_links["RTF"]["Titles"]]
        self.rtf_tc_info = self.create_mapping_links(rtf_scrapper, mapping_obj)
    
    def polish_title(self, title):
        # Lista de caracteres conflictivos
        and_chars = ['+', '&']
        # Reemplaza cada carácter conflictivo por su versión escapada
        for char in and_chars:
            title = title.replace(char, 'and')
        return title
        
    def create_mapping_links(self, rtf_scrapper, mapping_obj):
        # self.mapping_links["RTF"]["Titles"].keys()
        for paragraph in rtf_scrapper.paragraphs:
            # remove last empty lines in paragraph
            while re.search(r"^\s*$", paragraph.paragraph.split("\n")[-1]):
                paragraph.paragraph = "\n".join(paragraph.paragraph.split("\n")[:-1])
            # Creates the object ELEMENT
            num_lines_in_paragraph = len(paragraph.paragraph.split("\n"))
            for num_line, line in enumerate(paragraph.paragraph.split("\n")):
                for tag_to_fill in self.rtf_titles:
                    if re.search(r'^' + tag_to_fill.lower(), line.lower()):
                        closing_tag = False
                        content_tag = []
                        for j in range(num_line+1, num_lines_in_paragraph):
                            content = paragraph.paragraph.split("\n")[j]
                            # Compare if content match with any tag of test_case_data
                            for tag in self.rtf_titles:
                                if tag.lower() in content.lower():
                                    closing_tag = True
                                    break
                            else:
                                if not(tag_to_fill.lower() == "test of" and "Test case n/m" in content):
                                    if tag_to_fill.lower() == "suitable test environments":
                                        if content.lower() == "hil":
                                            content = "HIL/Bench/Lab"
                                        if content.lower() == "veh":
                                            content = "Vehicle"
                                    if tag_to_fill.lower() == "regression":
                                        if content.lower() == "yes":
                                            content = "True"
                                        if content.lower() == "no":
                                            content = "False"
                                    content_tag.append(content)
                            if closing_tag:
                                break
                        paragraph.element[tag_to_fill] = content_tag
            for line in paragraph.paragraph.split("\n"):
                if re.search(r"^\[", line.strip()):
                    # legacy id is the content between brackets
                    paragraph.element["legacy_id"] = line.split("[")[1].split("]")[0]
                    title = line.split("]")[1].strip()
                    paragraph.title = self.polish_title(title)
        title_prefix = input(f"Do you want to add a prefix to the title of the test cases? (Default: ''):")
        if title_prefix != "":
            title_prefix = title_prefix.strip() + " "
        rtf_tc = []
        for paragraph in rtf_scrapper.paragraphs:
            title = paragraph.title
            description = paragraph.description
            rtf_tc.append(mapping_obj.generate_mapped_link(paragraph.element, "RTF", title, description, title_prefix))

        # Saving a Copy of the mapping links filled
        with open(f"{self.path_tmp}/mapping_links_filled.json", 'w', encoding="utf-8") as file:
            json.dump(rtf_tc, file, indent=4, ensure_ascii=False)
        return rtf_tc
