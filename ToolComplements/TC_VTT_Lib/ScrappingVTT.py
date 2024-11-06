from TC_Common.SelectorCmd import cmd_colors
from TC_Common.DictsFunctions import add_at_beginning_of_dict
import xml.etree.ElementTree as ET

class VTTScrapper():
    def __init__(self, path, mapping_obj):
        self.path = path
        self.paragraphs = []
        
        self.filtered_paragraphs = []

        self.maping_links = mapping_obj.mapping_links
        self.get_paragraphs(self.scrap())
        # self.filtered_paragraphs = self.validate_paragraphs(self.paragraphs)

    def scrap(self):
        def get_element_tree(file_path):
            tree = ET.parse(file_path)
            root = tree.getroot()
            # Parse root to String and print
            return root
        VTTpath = self.path
        VTTXMLpath = VTTpath.replace(".vtt", ".xml")
        
        VTTfile = open(VTTpath, "r")
        VTTcontents = VTTfile.read()
        VTTfile.close()

        VTTcontents = VTTcontents.replace("xmlns", "xxxx")

        VTTXMLfile = open(VTTXMLpath, "w")
        VTTXMLfile.write(VTTcontents)
        VTTXMLfile.close()

        content = get_element_tree(VTTXMLpath)
        return content
        
    def get_paragraphs(self, content):
        root = content
        tt = root.find("tt")
        def vtt_to_dict(element):
            result = {}
            steps = []
            for child in element:
                if child.tag in self.maping_links["VTTScrapp"]["STEPS_Labels"]:
                    new_vtt_to_dict_child = add_at_beginning_of_dict(vtt_to_dict(child), "step", child.tag)
                    steps.append(new_vtt_to_dict_child)
                else:
                    if child.tag in result:
                        if isinstance(result[child.tag], list):
                            result[child.tag].append(vtt_to_dict(child))
                        else:
                            result[child.tag] = [result[child.tag], vtt_to_dict(child)]
                    else:
                        result[child.tag] = vtt_to_dict(child)
                if len(steps) > 0:
                    result["steps"] = steps
            if not result:
                result = element.text
            return result
        vtt_dict = vtt_to_dict(tt)
        
        self.paragraphs = vtt_dict

    def validate_paragraphs(self, d):
        if isinstance(d, dict):
            # Si el diccionario tiene el campo 'active' y es 'False', retornamos None (indica que debe ser eliminado)
            if 'active' in d and d['active'] == 'false':
                print(f"--- {cmd_colors.RED}WARNING:{cmd_colors.END}is inactive.")
                return None
            
            # Si no, procesamos recursivamente cada valor en el diccionario
            return {key: self.validate_paragraphs(value) for key, value in d.items() if self.validate_paragraphs(value) is not None}
        
        elif isinstance(d, list):
            # Si es una lista, procesamos cada elemento recursivamente y eliminamos los que sean None
            return [self.validate_paragraphs(item) for item in d if self.validate_paragraphs(item) is not None]
        
        # Si es otro tipo (string, número, etc.), lo retornamos sin cambios
        return d