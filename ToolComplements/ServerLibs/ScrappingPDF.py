from UnitScripts.pdf_to_text_tables_indent import extraer_texto_con_marcado_e_indentacion
from TC_Common.IndexTree import IndexTree
from TC_Common.DictsFunctions import (recursive_evaluation_keys)
from ServerLibs.Mapping_common import MappingClass
import copy
import os
import re
import json

class PDFScrapper():
        
    def __init__(self, path, path_tmp, mapping_file, text_scrapped, index_to_search):
        self.mapping_obj = MappingClass(mapping_file)
        self.path = path
        self.path_tmp = path_tmp
        self.paragraphs = []
        self.paragraphs_descarted = []
        self.text_scrapped = text_scrapped
        self.tc_start_regex = r"^\["
        self.index_tree = IndexTree()
        if index_to_search:
            self.index_tree.active = True
            self.index_tree.index_of_interest = int(index_to_search)

        self.mapping_links = self.mapping_obj.mapping_links
        if self.index_tree.active:
            self.index_tree.create_index_tree(self.text_scrapped, "Table of Content")
        self.get_paragraphs(self.text_scrapped)

        with open(os.path.join(self.path_tmp, "paragraphs.txt"), "w", encoding='utf-8') as f:
            for paragraph in self.paragraphs:
                f.write(f"{paragraph['title']}\n")
                f.write(f"----------------------\n")
                f.write(f"{paragraph['paragraph']}\n")
                f.write(f"----------------------\n\n")
        # self.preparing_paragraphs()


    class ParagraphCandidate():
        def __init__(self):
            self.title = ""
            self.paragraph = ""
            self.paragraph_lines = []
            self.description = ""
            self.element = {}
    
    def new_paragraph_candidate(self, title, paragraph):
        # candidate = self.ParagraphCandidate()
        # candidate.title = title
        # candidate.description = paragraph["ancestros"]
        # candidate.paragraph = paragraph["texto"]
        # candidate.paragraph_lines = paragraph["text_array"]
        candidate = {}
        candidate["title"] = title
        candidate["description"] = paragraph["ancestros"]
        candidate["paragraph"] = paragraph["texto"]
        candidate["paragraph_lines"] = paragraph["text_array"]
        return candidate

    def get_paragraphs(self, content):
        candidates = []
        for index, ln in enumerate(content):
            tmp_paragraph = '\n'.join(content[index:])
            tmp_paragraph_array = tmp_paragraph.split("\n")
            line = ln.strip()
            # if line is key of index_tree.dict_index
            dict_index_copy = copy.deepcopy(self.index_tree.dict_index)
            for index, key in enumerate(self.index_tree.dict_index):
                if key in line:
                    # Search key in self.index_tree.index_lines (partial match)
                    index_of_index_line = [index for index, index_line in enumerate(self.index_tree.index_lines) if key in index_line][0]
                    # Cut tmp_paragraph until next line with index
                    if index_of_index_line+1 < len(self.index_tree.index_lines):
                        end_line = self.index_tree.index_lines[index_of_index_line+1]
                        index_of_end_line = tmp_paragraph_array.index(end_line)
                        tmp_paragraph = "\n".join(tmp_paragraph_array[:index_of_end_line])
                    else:
                        if index == len(self.index_tree.dict_index)-1:
                            print(f"index: {index}")
                            try:
                                line_with_next_index = next(line for line in tmp_paragraph_array if line.startswith(str(self.index_tree.index_of_interest + 1)))
                                index_of_end_line = tmp_paragraph_array.index(line_with_next_index)
                                tmp_paragraph = "\n".join(tmp_paragraph_array[:index_of_end_line])
                            except Exception as e:
                                print(f"Error: {e}")
                        else:
                            tmp_paragraph = tmp_paragraph
                    tmp_paragraph_array = tmp_paragraph.split("\n")
                    dict_index_copy[key]["texto"] = tmp_paragraph
                    dict_index_copy[key]["text_array"] = tmp_paragraph_array
                    candidates.append(self.new_paragraph_candidate(key, dict_index_copy[key]))
        self.paragraphs = candidates

    def preparing_paragraphs(self):
        titles = [title for title in self.mapping_links["PDFScrapp"]]
        # reverse iteration of titles
        reverse_titles = titles[::-1]
        new_paragraphs = []
        discarded_paragraphs = []
        for main_index, paragraph in enumerate(self.paragraphs):
            tmp_paragraph = paragraph["paragraph"].split("\n")
            paragraph["element"] = {}
            paragraph["mainpart_added"] = None

            lines_set = '\n'.join(tmp_paragraph)
            if "Test Case ID:" in lines_set:
                paragraph["mainpart_added"] = "#03fc8c"  # Agregar propiedad Verde claro
                paragraph["tooltip"] = "Test Case ID: True\nMain Part: True\nDescription: True"

            # Adding Main Part for TestCases wo Titles [Preparation, Main Part, Completion]
            lines_set = '\n'.join(tmp_paragraph)
            if "Test Case ID:" in lines_set and not "Main Part" in lines_set:
                main_part_added = False
                for index, line in enumerate(tmp_paragraph):
                    if re.search(r"^\s*(Call|Set|For Each|Wait|Send)\b.*", line):
                        main_part_added = True
                        tmp_paragraph = tmp_paragraph[:index] + ["Main Part"] + tmp_paragraph[index:]
                        break
            # Adding Main Part for NetTestCases
            lines_set = '\n'.join(tmp_paragraph)
            if not "Test Case ID:" in lines_set and not "Main Part" in lines_set:
                main_part_added = False
                for index, line in enumerate(tmp_paragraph):
                    if re.search(r"^\s*(Call|Set|For Each|Wait|Send)\b.*", line):
                        tmp_paragraph = tmp_paragraph[:index] + ["Main Part"] + tmp_paragraph[index:]
                        main_part_added = True
                        break


            # Adding Description for TestCases w Description
            lines_set = '\n'.join(tmp_paragraph)
            if "Test Case ID:" in lines_set:
                index_begin_description = 0
                for index, line in enumerate(tmp_paragraph):
                    if index_begin_description > 0:
                        if any(title in line for title in titles):
                            index_end_description = index
                            if main_index == 4:
                                print("Breaked")
                            break
                    if "Test Case ID" in line:
                        index_begin_description = index + 1
                if index_begin_description > 0 and index_end_description > 0 and index_end_description > index_begin_description:
                    tmp_paragraph = tmp_paragraph[:index_begin_description] + ["Description"] + tmp_paragraph[index_begin_description:index_end_description] + tmp_paragraph[index_end_description:]

            lines_set = '\n'.join(tmp_paragraph)
            if "Test Case ID:" in lines_set and "Description" not in lines_set:
                main_part_added = "Main Part" in lines_set
                if main_part_added:
                    paragraph["mainpart_added"] = "#03fcf8"  # Agregar propiedad Azul aqua
                else:
                    paragraph["mainpart_added"] = "#0390fc"  # Agregar propiedad Azul claro
                paragraph["tooltip"] = f"Test Case ID: True\nMain Part: {main_part_added}\nDescription: False"
            if "Test Case ID:" not in lines_set:
                if main_part_added:
                    paragraph["mainpart_added"] = "#eebf3e"  # Agregar propiedad Amarillo claro
                    paragraph["tooltip"] = f"Test Case ID: False\nMain Part: True\nDescription: False"
                else:
                    paragraph["mainpart_added"] = "#e61b1b"  # Agregar propiedad Amarillo claro
                    paragraph["tooltip"] = f"Test Case ID: False\nMain Part: False\nDescription: False"

            cutted_paragraph = tmp_paragraph
            for index, tag_to_fill in enumerate(reverse_titles):
                identifier = self.mapping_links["PDFScrapp"][tag_to_fill]["identifier"]
                index_until_break = None
                for index, _ in enumerate(cutted_paragraph):
                    size_paragraph = len(cutted_paragraph)
                    lines_set = '\n'.join(cutted_paragraph[size_paragraph-index-1:])
                    if identifier in lines_set:
                        index_until_break = index
                        line_to_modify = size_paragraph - index_until_break - 1
                        tmp_paragraph[line_to_modify] = '## ' + tmp_paragraph[line_to_modify]
                        break
                    else:
                        index_until_break = None
                if index_until_break is not None:
                    remove = self.mapping_links["PDFScrapp"][tag_to_fill]["remove"]
                    lines_set = lines_set.replace(remove, "")
                    paragraph["element"][tag_to_fill] = lines_set
                    steps = ["Preparation", "Main Part", "Completion"]
                    if tag_to_fill in steps:
                        paragraph["element"][tag_to_fill] = paragraph["element"][tag_to_fill].replace('Call', 'Step')
                    cutted_paragraph = cutted_paragraph[:size_paragraph-index_until_break-1]

                paragraph["paragraph"] = '\n'.join(tmp_paragraph)
                paragraph["paragraph_lines"] = tmp_paragraph
                
            if "Main Part" not in paragraph["paragraph"]:
                discarded_paragraphs.append(paragraph)
            else:
                new_paragraphs.append(paragraph)
        self.paragraphs = new_paragraphs
        self.paragraphs_descarted = discarded_paragraphs
    def scrap_pdf(self, header_page=None):
        text = extraer_texto_con_marcado_e_indentacion(self.path, self.path_tmp, x_tol=2, y_tol=3, pixels_per_space=5, page_indicada=header_page)
        return text
    