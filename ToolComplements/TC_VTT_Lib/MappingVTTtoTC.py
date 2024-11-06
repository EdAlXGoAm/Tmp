from TC_Common.SelectorCmd import cmd_colors
from TC_Common.SelectorCmd import CMDSelector
from TC_Common.CreateTCcommon import save_tc_in_json
from TC_Common.DictsFunctions import (
    add_at_beginning_of_dict,
    move_at_beginning_of_dict,
    copy_dict_key,
    remove_dict_key,
    subarrays_to_dicts,
    elevate_key,
    convert_keys_to_dict,
    convert_keys_to_strings,
    convert_keys_arrays_to_strings,
    convert_list_to_formatted_strings,
    convert_deepest_arrays_to_strings,
    convert_keys_to_strings_new,
    obtener_llaves_primer_nivel,
    evaluar_llaves,
    transform_values,
    join_string_arrays
)
import os
import json
import time
import re
import copy

delr = '\033[1A\033[K'
up = '\033[1A'

class VTTMapping():
    def __init__(self, path_tmp=None, vtt_scrapper=None, mapping_obj=None):
        if path_tmp is None:
            return None
        self.path_tmp = path_tmp
        self.vtt_test_cases_debug_pre_string = []
        self.vtt_test_cases_debug = []
        self.vtt_tc_info = self.create_mapping_links(vtt_scrapper, mapping_obj)
    
    def get_title_origin(self, item, regex):
        """
        Retorna un diccionario con 'title' y 'regex' basado en el elemento proporcionado.
        """
        if item.get('title'):
            title = item['title']
            pattern_hex_end = re.compile(regex)
            match = pattern_hex_end.search(title)
            regex_match = match.group(0) if match else None
            return {"title": title, "regex": regex_match}
        return {"title": None, "regex": None}

    def traverse(self, node, path, tcs, vtt_mapping):
        """
        Recorre recursivamente la estructura de datos y construye el campo 'origin' 
        como una lista de diccionarios con 'label', 'index', 'title' y 'regex'.
        """
        if isinstance(node, dict):
            for key, value in node.items():
                if key in vtt_mapping['TC_Labels']:
                    # Procesar las entradas que están en vtt_mapping['TC_Labels']
                    if isinstance(value, list):
                        for index, sub_value in enumerate(value):
                            # Obtener la información de title y regex
                            title_info = self.get_title_origin(sub_value, vtt_mapping['title_regex'])
                            
                            # Construir el diccionario de origen
                            origin_entry = {
                                "label": key,
                                "index": index,
                                "title": title_info['title'],
                                "regex": title_info['regex']
                            }
                            
                            # Crear una nueva ruta agregando el diccionario de origen
                            new_path = path + [origin_entry]
                            
                            # Asignar 'origin' y '0_type' al sub_value
                            sub_value['origin'] = new_path.copy()
                            sub_value['0_type'] = vtt_mapping['TC_Labels'][key]
                            
                            # Agregar el sub_value a la lista de casos de prueba
                            tcs.append(sub_value)
                    else:
                        # Si no es una lista, simplemente agregar la clave al camino
                        title_info = self.get_title_origin(value, vtt_mapping['title_regex'])
                        
                        origin_entry = {
                            "label": key,
                            "index": None,  # No hay índice en este caso
                            "title": title_info['title'],
                            "regex": title_info['regex']
                        }
                        
                        new_path = path + [origin_entry]
                        value['origin'] = new_path.copy()
                        value['0_type'] = vtt_mapping['TC_Labels'][key]
                        tcs.append(value)
                else:
                    if isinstance(value, list):
                        for index, item in enumerate(value):
                            # Obtener la información de title y regex
                            title_info = self.get_title_origin(item, vtt_mapping['title_regex'])
                            
                            # Construir el diccionario de origen
                            origin_entry = {
                                "label": key,
                                "index": index,
                                "title": title_info['title'],
                                "regex": title_info['regex']
                            }
                            
                            # Crear una nueva ruta agregando el diccionario de origen
                            new_path = path + [origin_entry]
                            
                            # Continuar la recursión con la nueva ruta
                            self.traverse(item, new_path, tcs, vtt_mapping)
                    else:
                        # Continuar la recursión agregando el label sin índice
                        origin_entry = {
                            "label": key,
                            "index": None,
                            "title": None,
                            "regex": None
                        }
                        new_path = path + [origin_entry]
                        self.traverse(value, new_path, tcs, vtt_mapping)
        elif isinstance(node, list):
            for index, item in enumerate(node):
                # Obtener la información de title y regex
                title_info = self.get_title_origin(item, vtt_mapping['title_regex'])
                
                # Construir el diccionario de origen
                origin_entry = {
                    "label": None,  # Puedes asignar un valor predeterminado si es necesario
                    "index": index,
                    "title": title_info['title'],
                    "regex": title_info['regex']
                }
                
                # Crear una nueva ruta agregando el diccionario de origen
                new_path = path + [origin_entry]
                
                # Continuar la recursión con la nueva ruta
                self.traverse(item, new_path, tcs, vtt_mapping)
            
    def sort_dict_recursive(self, node):
        if isinstance(node, dict):
            # Creamos un nuevo diccionario ordenado por las llaves
            sorted_dict = {key: self.sort_dict_recursive(value) for key, value in sorted(node.items())}
            return sorted_dict
        elif isinstance(node, list):
            # Si es una lista, la recorremos y ordenamos recursivamente los elementos dentro
            return [self.sort_dict_recursive(item) for item in node]
        else:
            # Si es un valor que no necesita ordenarse (como un int, str, etc.), lo devolvemos tal cual
            return node    
    
    def get_first_regex(self, origin):
        """
        Retorna el primer valor de 'regex' que no sea None en una lista de diccionarios.

        :param origin: Lista de diccionarios con las claves 'label', 'index', 'title' y 'regex'.
        :return: El primer valor de 'regex' que no sea None, o None si no se encuentra ninguno.
        """
        for entry in origin:
            regex = entry.get('regex')
            if regex is not None:
                return regex
        return None

    def create_mapping_links(self, vtt_scrapper, mapping_obj):
        mapping_links = mapping_obj.mapping_links
        vtt_tc = []
        self.vtt_test_cases_debug_pre_string = []
        self.vtt_test_cases_debug = []
        if len(vtt_scrapper.filtered_paragraphs) == 0:
            self.traverse(vtt_scrapper.paragraphs, [], vtt_tc, mapping_links["VTTMapping"])
        else:
            self.traverse(vtt_scrapper.filtered_paragraphs, [], vtt_tc, mapping_links["VTTMapping"])
        # Prefix for the Test Case Title
        for tc_element in vtt_tc:
            tc = copy.deepcopy(tc_element)
            tc = copy_dict_key(tc, 'name', '0_title')
            tc = copy_dict_key(tc, 'title', '0_title')
            tc = remove_dict_key(tc, 'name')
            tc = remove_dict_key(tc, 'title')
            tc = copy_dict_key(tc, '0_title', 'title')
            tc = remove_dict_key(tc, '0_title')
            tc = move_at_beginning_of_dict(tc, '0_title')
            tc = move_at_beginning_of_dict(tc, 'active', 'true')
            tc = remove_dict_key(tc, 'active')
            tc = move_at_beginning_of_dict(tc, 'tcid')
            tc = move_at_beginning_of_dict(tc, '0_type')
            # tc = subarrays_to_dicts(tc)
            # tc = convert_deepest_arrays_to_strings(tc)
            tc = convert_keys_to_dict(tc, mapping_links["VTTMapping"]["Arrays_to_dicts"], "step")
            tc = convert_keys_to_strings(tc, mapping_links["VTTMapping"]["Dicts_to_strings"])
            stringed_tc = copy.deepcopy(tc)
            stringed_tc = convert_keys_to_strings_new(stringed_tc, mapping_links["VTTMapping"]["Dicts_to_strings_new_1"])
            stringed_tc = convert_keys_to_strings_new(stringed_tc, mapping_links["VTTMapping"]["Dicts_to_strings_new_2"])
            stringed_tc = transform_values(stringed_tc)
            self.vtt_test_cases_debug_pre_string.append(tc)
            self.vtt_test_cases_debug.append(stringed_tc)
        llaves = obtener_llaves_primer_nivel(self.vtt_test_cases_debug)
        new_llaves = evaluar_llaves(self.vtt_test_cases_debug)
        self.vtt_test_cases_debug.append(llaves)
        self.vtt_test_cases_debug.append(new_llaves)
        # self.vtt_test_cases_debug = self.sort_dict_recursive(self.vtt_test_cases_debug)
        save_tc_in_json(self.path_tmp, "vtt_test_cases_debug", self.vtt_test_cases_debug)
        os.system(f"code -n {self.path_tmp}/vtt_test_cases_debug.json")
        self.vtt_test_cases_debug = join_string_arrays(self.vtt_test_cases_debug)
        # remover los ultimos 2 elementos de la lista ¿why?
        self.vtt_test_cases_debug = self.vtt_test_cases_debug[:-2]

        title_prefix_input = input(f"Do you want to add a prefix to the title of the Test Cases? (Default: '{mapping_links["VTTMapping"]["title_regex"]}'): ")
        vtt_tc_mapped = []
        for element in self.vtt_test_cases_debug:
            if title_prefix_input != "":
                separator = mapping_links["VTTMapping"]["title_separator"]
                title_prefix = title_prefix_input.strip() + separator
            else:
                title_prefix = self.get_first_regex(element["origin"]) + mapping_links["VTTMapping"]["title_separator"]
            title = element["title"]
            description = element["tcid"]
            vtt_tc_mapped.append(mapping_obj.generate_mapped_link(element, "VTT", title, description, title_prefix))
        
        # Saving a Copy of the mapping links filled
        with open(f"{self.path_tmp}/mapping_links_filled.json", 'w', encoding="utf-8") as file:
            json.dump(vtt_tc_mapped, file, indent=4, ensure_ascii=False)
        return vtt_tc_mapped
