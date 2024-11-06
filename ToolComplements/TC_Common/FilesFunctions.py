from TC_Common.SelectorCmd import cmd_colors
from TC_Common.SelectorCmd import CMDSelector
import os
import json

def get_files_for_selector(path, extension, recursive):
    files_names = []
    files_paths = []
    for file in os.listdir(path):
        if file.endswith(extension):
            files_names.append(file)
            files_paths.append(f"{path}/{file}")
    if recursive:
        # Recursive search
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith(extension):
                    files_names.append(file)
                    files_paths.append(f"{root}/{file}")
    dict_files = dict(zip(files_names, files_paths))
    return dict_files

def select_file(path, extension, type_file, recursive=False):
    if isinstance(extension, str):
        files_dic = get_files_for_selector(path, extension, recursive)
    elif isinstance(extension, list):
        files_dic = {}
        for element in extension:
            files_dic.update(get_files_for_selector(path, element, recursive))
    files = list(files_dic.keys())
    file_selector = CMDSelector()
    file_selector.title = f"Select the {type_file} file:"
    file_selector.options = files + ["Cancel"]
    file = file_selector.select()
    print(f"--- Selected {type_file} file: {cmd_colors.CYAN}{file}{cmd_colors.END}\n")
    if file == "Cancel":
        return "Cancel"
    return files_dic[file]