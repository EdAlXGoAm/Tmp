import re

class RTFScrapper():
    class ParagraphCandidate():
        def __init__(self, num_line):
            self.num_line = num_line
            self.paragraph = ""
            self.closed = False
            self.description = ""
            self.element = {}
        
    class IndexTree():
        def __init__(self):
            self.active = False
            self.index = 0
            self.children = {}

        def add_child(self, line):
            index_str = str(self.index)
            if line.startswith(index_str):
                if re.search(r"\b\d+(\.\d+)*\b", line):
                    level_string = re.search(r"\b\d+(\.\d+)*\b", line).group()
                    level = level_string.count(".")
                    if level not in self.children:
                        self.children[level_string] = []
                    self.children[level_string] = line

        def get_index_level(self, index_str, level):
            index_level = ""
            for i in range(level+1):
                if i > 0:
                    index_level += "."
                index_level += index_str.split(".")[i]
            return index_level

        def compare_index_line(self, line):
            comparison = re.search(r"\b\d+(\.\d+)*\b", line)
            if comparison:
                index_line = comparison.group()
                first_number = index_line.split(".")[0]
                if first_number == str(self.index):
                    level_of_index = index_line.count(".")
                    description = ""
                    for i in range(level_of_index):
                        if i > 0:
                            description += "\n"
                        description += self.children[self.get_index_level(index_line, i)]
                    description += "\n" + line
                    return description
                else:
                    return ""
            else:
                return ""

    def __init__(self, path, mapping_obj):
        self.path = path
        self.paragraphs = []

        self.tc_start_regex = r"^\["
        self.index_tree = self.IndexTree()
        self.ask_for_index()

        self.mapping_links = mapping_obj.mapping_links
        self.get_paragraphs(self.scrap())
        self.validate_paragraphs(self.mapping_links["RTF"]["Titles"])
    
    def ask_for_index(self):
        index = input("If TestCases are numbered, please provide the index: ")
        if index.isdigit():
            self.index_tree.active = True
            self.index_tree.index = int(index)

    def scrap(self):
        with open(self.path, 'r', encoding="utf-8") as file:
            content = file.readlines()
        return content

    def new_paragraph_candidate(self, num_line, line, content):
        candidate = self.ParagraphCandidate(num_line)
        candidate.description = self.index_tree.compare_index_line(content[num_line-1])
        candidate.paragraph += line + "\n"
        return candidate

    def get_paragraphs(self, content):
        candidates = []
        for index, ln in enumerate(content):
            line = ln.strip()
            if self.index_tree.active:
                self.index_tree.add_child(line)
            if re.search(self.tc_start_regex, line):
                if len(candidates) > 0:
                    if candidates[-1].closed == True:
                        candidates.append(self.new_paragraph_candidate(index, line, content))
                else:
                    candidates.append(self.new_paragraph_candidate(index, line, content))
            elif re.search(r"^\s*$", line):
                if len(candidates) > 0:
                    if candidates[-1].closed == False:
                        candidates[-1].paragraph += line
                        candidates[-1].closed = True
            else:
                if len(candidates) > 0:
                    
                    if candidates[-1].closed == False:
                        candidates[-1].paragraph += line + "\n"

        self.paragraphs = candidates
    
    def validate_paragraphs(self, titles):
        titles = [title for title in self.mapping_links["RTF"]["Titles"]]
        new_candidates = []
        for candidate in self.paragraphs:
            validated = False
            for ln in candidate.paragraph.split("\n"):
                line = ln.lower().strip()
                for title in titles:
                    if title in line:
                        validated = True
                        break
            if validated:
                new_candidates.append(candidate)
        self.paragraphs = new_candidates