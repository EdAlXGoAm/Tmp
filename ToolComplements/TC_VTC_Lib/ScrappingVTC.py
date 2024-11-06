from TC_Common.SelectorCmd import cmd_colors

import xml.etree.ElementTree as ET

class VTCScrapper():
    def __init__(self, path, mapping_obj):
        self.path = path
        self.paragraphs = []

        self.filtered_paragraphs = []

        self.maping_links = mapping_obj.mapping_links
        self.get_paragraphs(self.scrap())
        
    def scrap(self):
        def get_element_tree(file_path):
            tree = ET.parse(file_path)
            root = tree.getroot()
            return root
        VTCpath = self.path
        VTCXMLpath = VTCpath.replace(".vtc", ".xml")

        VTCfile = open(VTCpath, "r")
        VTCcontents = VTCfile.read()
        VTCfile.close()

        VTCcontents = VTCcontents.replace("xmlns", "xxxx")

        VTCXMLfile = open(VTCXMLpath, "w")
        VTCXMLfile.write(VTCcontents)
        VTCXMLfile.close()

        content = get_element_tree(VTCXMLpath)
        return content
    
    def get_paragraphs(self, content):
        root = content
        TestCases = root.find("TestCases")
        TraceItemsa = root.find("TraceItems")
        def vtc_to_dict(element):
            result = {}
            if element.attrib:
                result["@attributes"] = element.attrib
            for child in element:
                if child.tag in result:
                    if isinstance(result[child.tag], list):
                        result[child.tag].append(vtc_to_dict(child))
                    else:
                        result[child.tag] = [result[child.tag], vtc_to_dict(child)]
                else:
                    result[child.tag] = vtc_to_dict(child)
            if not result:
                result = element.text
            return result
        vtc_dict = {
            "TestCases": vtc_to_dict(TestCases),
            "TraceItems": vtc_to_dict(TraceItemsa)
            }

        self.paragraphs = vtc_dict