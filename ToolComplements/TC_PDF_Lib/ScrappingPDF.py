from UnitScripts.pdf_to_text_tables_indent import extraer_texto_con_marcado_e_indentacion
from TC_Common.IndexTree import IndexTree
from TC_Common.DictsFunctions import (recursive_evaluation_keys)
import copy
import os
import re

class PDFScrapper():
        
    def __init__(self, path, path_tmp, mapping_obj):
        self.path = path
        self.path_tmp = path_tmp
        self.paragraphs = []
        self.header_page = None

        self.tc_start_regex = r"^\["
        self.index_tree = IndexTree()
        self.ask_for_index()
        self.ask_for_header_page()

        self.mapping_links = mapping_obj.mapping_links
        if self.index_tree.active and self.header_page:
            self.index_tree.create_index_tree(self.scrap_pdf(self.header_page), "Table of Content")
        self.get_paragraphs(self.scrap_pdf(self.header_page))
        with open(os.path.join(self.path_tmp, "paragrapgs.txt"), "w") as f:
            for paragraph in self.paragraphs:
                f.write(f"{paragraph.title}\n")
                f.write(f"----------------------\n")
                f.write(f"{paragraph.paragraph}\n")
                f.write(f"----------------------\n\n")
        self.preparing_paragraphs()

    def ask_for_index(self):
        index = input("If TestCases are numbered, please provide the index: ")
        if index.isdigit():
            self.index_tree.active = True
            self.index_tree.index_of_interest = int(index)

    def ask_for_header_page(self):
        page = input("If the pages have a header, please provide the page number of the first page with the header: ")
        if page.isdigit():
            self.header_page = int(page)

    class ParagraphCandidate():
        def __init__(self):
            self.title = ""
            self.paragraph = ""
            self.paragraph_lines = []
            self.description = ""
            self.element = {}
    
    def new_paragraph_candidate(self, title, paragraph):
        candidate = self.ParagraphCandidate()
        candidate.title = title
        candidate.description = paragraph["ancestros"]
        candidate.paragraph = paragraph["texto"]
        candidate.paragraph_lines = paragraph["text_array"]
        return candidate

    def get_paragraphs(self, content):
        candidates = []
        for index, ln in enumerate(content):
            tmp_paragraph = '\n'.join(content[index:])
            tmp_paragraph_array = tmp_paragraph.split("\n")
            line = ln.strip()
            # if line is key of index_tree.dict_index
            dict_index_copy = copy.deepcopy(self.index_tree.dict_index)
            for key in self.index_tree.dict_index:
                if key in line:
                    # Search key in self.index_tree.index_lines (partial match)
                    index_of_index_line = [index for index, index_line in enumerate(self.index_tree.index_lines) if key in index_line][0]
                    # Cut tmp_paragraph until next line with index
                    if index_of_index_line+1 < len(self.index_tree.index_lines):
                        end_line = self.index_tree.index_lines[index_of_index_line+1]
                        index_of_end_line = tmp_paragraph_array.index(end_line)
                        tmp_paragraph = "\n".join(tmp_paragraph_array[:index_of_end_line])
                    else:
                        tmp_paragraph = tmp_paragraph
                    tmp_paragraph_array = tmp_paragraph.split("\n")
                    dict_index_copy[key]["texto"] = tmp_paragraph
                    dict_index_copy[key]["text_array"] = tmp_paragraph_array
                    candidates.append(self.new_paragraph_candidate(key, dict_index_copy[key]))
        self.paragraphs = candidates

    def preparing_paragraphs(self):
        titles = [title for title in self.mapping_links["PDFScrapp"]]
        print(f"Titles: {titles}")
        # reverse iteration of titles
        reverse_titles = titles[::-1]
        print(f"Reverse Titles: {reverse_titles}")
        for index, paragraph in enumerate(self.paragraphs):
            print(f"-{index}----- Paragraph: {paragraph.title} -------")
            tmp_paragraph = paragraph.paragraph.split("\n")

            # Adding Main Part for TestCases wo Titles [Preparation, Main Part, Completion]
            lines_set = '\n'.join(tmp_paragraph)
            if "Test Case ID:" in lines_set and not "Main Part" in lines_set:
                for index, line in enumerate(tmp_paragraph):
                    if re.search(r"^\s*(Call|Set|For Each|Wait)\b.*", line):
                        tmp_paragraph = tmp_paragraph[:index] + ["Main Part"] + tmp_paragraph[index:]
                        break

            # Adding Main Part for NetTestCases
            lines_set = '\n'.join(tmp_paragraph)
            if not "Test Case ID:" in lines_set and not "Main Part" in lines_set:
                for index, line in enumerate(tmp_paragraph):
                    if re.search(r"^\s*(Call|Set|For Each|Wait)\b.*", line):
                        tmp_paragraph = tmp_paragraph[:index] + ["Main Part"] + tmp_paragraph[index:]
                        break

            # Adding Description for TestCases w Description
            lines_set = '\n'.join(tmp_paragraph)
            if "Test Case ID:" in lines_set:
                index_begin_description = 0
                for index, line in enumerate(tmp_paragraph):
                    if "Test Case ID" in line:
                        index_begin_description = index + 1
                    if index_begin_description > 0:
                        for title in titles:
                            if title in line:
                                index_end_description = index
                                break
                if index_begin_description > 0 and index_end_description > 0 and index_end_description > index_begin_description:
                    tmp_paragraph = tmp_paragraph[:index_begin_description] + ["Description"] + tmp_paragraph[index_begin_description:index_end_description] + tmp_paragraph[index_end_description:]

            for index, tag_to_fill in enumerate(reverse_titles):
                identifier = self.mapping_links["PDFScrapp"][tag_to_fill]["identifier"]
                index_until_break = None
                for index, _ in enumerate(tmp_paragraph):
                    size_paragraph = len(tmp_paragraph)
                    lines_set = '\n'.join(tmp_paragraph[size_paragraph-index-1:])
                    if identifier in lines_set:
                        print(f"Tag to fill: {tag_to_fill}")
                        # print(f"Lines: {lines_set}")
                        index_until_break = index
                        break
                    else:
                        index_until_break = None
                if index_until_break is not None:
                    remove = self.mapping_links["PDFScrapp"][tag_to_fill]["remove"]
                    lines_set = lines_set.replace(remove, "")
                    paragraph.element[tag_to_fill] = lines_set
                    steps = ["Preparation", "Main Part", "Completion"]
                    if tag_to_fill in steps:
                        paragraph.element[tag_to_fill] = paragraph.element[tag_to_fill].replace('Call', 'Step')
                    tmp_paragraph = tmp_paragraph[:size_paragraph-index_until_break-1]

                paragraph.paragraph = '\n'.join(tmp_paragraph)
                paragraph.paragraph_lines = tmp_paragraph
    
    def scrap_pdf(self, header_page=None):
        text = extraer_texto_con_marcado_e_indentacion(self.path, self.path_tmp, x_tol=2, y_tol=3, pixels_per_space=5, page_indicada=header_page)
        return text
    