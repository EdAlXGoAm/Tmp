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
up = '\033[A'

class PDFMapping():
    def __init__(self, path_tmp=None, pdf_scrapper=None, mapping_obj=None):
        if path_tmp is None:
            return None
        self.path_tmp = path_tmp
        self.pdf_titles = [title for title in mapping_obj.mapping_links["PDF"]["Titles"]]
        self.pdf_tc_info = self.create_mapping_links(pdf_scrapper, mapping_obj)

    def polish_title(self, title):
        # Lista de caracteres conflictivos
        and_chars = ['+', '&']
        # Reemplaza cada carácter conflictivo por su versión escapada
        for char in and_chars:
            title = title.replace(char, 'and')
        return title
    
    def create_mapping_links(self, pdf_scrapper, mapping_obj):
        for paragraph in pdf_scrapper.paragraphs:
            # remove last empty lines in paragraph
            while re.search(r"^\s*$", paragraph.paragraph.split("\n")[-1]):
                paragraph.paragraph = "\n".join(paragraph.paragraph.split("\n")[:-1])
            # Creates the object ELEMENT
            num_lines_in_paragraph = len(paragraph.paragraph.split("\n"))
            print(f"----------------------------------")
            print(f"Paragraph: {paragraph.title}")
            for num_line, line in enumerate(paragraph.paragraph.split("\n")):
                for tag_to_fill in self.pdf_titles:
                    if re.search(r'^' + tag_to_fill.lower(), line.lower()):
                        print(f"Tag to fill: {tag_to_fill}")

        title_prefix = input(f"Do you want to add a prefix to the title of the test cases? (Default: ''):")
        if title_prefix != "":
            title_prefix = title_prefix.strip() + " "
        
        pdf_tc = []
        for paragraph in pdf_scrapper.paragraphs:
            title = paragraph.title
            description = ' | '.join(paragraph.description)
            pdf_tc.append(mapping_obj.generate_mapped_link(paragraph.element, "PDF", title, description, title_prefix))

        # Saving a Copy of the mapping links filled
        with open(f"{self.path_tmp}/mapping_links_filled.json", 'w', encoding="utf-8") as file:
            json.dump(pdf_tc, file, indent=4, ensure_ascii=False)
        os.system('code -n ' + f"{self.path_tmp}/mapping_links_filled.json")
        return pdf_tc
