from TC_Common.SelectorCmd import cmd_colors
from TC_Common.SelectorCmd import CMDSelector
import os
import json
import time


def save_tc_in_json(path, file, dict_data):
    def obj_dict(obj):
        return obj.__dict__
    
    json_string = json.dumps(dict_data, default=obj_dict, indent=4, ensure_ascii=False)
    filename = f"{path}/{file}.json"
    with open(filename, "w+", encoding="utf-8") as fl:
        fl.write(json_string)

def val_field(field):
    if field is not None and field != "":
        return True
    else:
        return False

def etm_create_process(qm_context, test_cases_info, path_tmp, log_object, recycle=False):
    os.system('cls')
    tp_title_obj = test_cases_info.get_t_ps_id_or_name("TP", qm_context)
    if tp_title_obj is None:
        return "Cancel"
    ts_title_obj = test_cases_info.get_t_ps_id_or_name("TS", qm_context)
    if ts_title_obj is None:
        return "Cancel"
    for index, test_case in enumerate(test_cases_info.test_cases):
        test_case.tp_obj = tp_title_obj
        test_case.ts_obj = ts_title_obj
    test_cases_info.save_tc_in_json(path_tmp, "test_cases")
    # Open JSON in VSCode
    os.system(f"code -n {path_tmp}/test_cases.json")
    selection = CMDSelector()
    selection.title = "--- Review the JSON File\nif ALL is OK, press Enter to continue..."
    selection.options = ["Continue", "Add More Info", "Cancel"]
    key_to_continue = selection.select()
    if key_to_continue == "Continue":
        os.system('cls')
        log_object.print_and_log(f"************************* CREATING TEST CASES IN ETM *************************")
        # Create Test Cases in ETM
        for local_test_case in test_cases_info.test_cases:
            log_object.print_and_log(f"{cmd_colors.GREEN}CREATING.{cmd_colors.END} Test Case:\n\tTitle: {cmd_colors.CYAN}{local_test_case.title}{cmd_colors.END}\n")
            # Create Test Case in ETM
            remote_test_case = test_cases_info.etm_new_test_case(qm_context, id=local_test_case.tcid if recycle and val_field(local_test_case.tcid) else None, title=local_test_case.title, print_prefix="\t")
            remote_test_case = test_cases_info.etm_set_title(qm_context, local_test_case, remote_test_case, print_prefix="\t")
            remote_test_case = test_cases_info.etm_set_t_sp(qm_context, "TS", local_test_case, remote_test_case, print_prefix="\t")
            remote_test_case = test_cases_info.etm_set_t_sp(qm_context, "TP", local_test_case, remote_test_case, print_prefix="\t")
            remote_test_case = test_cases_info.etm_fill_test_case(qm_context, local_test_case, remote_test_case, print_prefix="\t")
            log_object.print_and_log("\n")
            if remote_test_case is None:
                log_object.print_message("ABORTED", "Create Test Case in ETM", "Process could not be completed.", print_prefix="\t")
                log_object.print_and_log("\n")
                continue
            log_object.print_message("SUCCESS", "Create Test Case in ETM", "Test Case created in ETM.", print_prefix="\t")
            log_object.print_and_log("\n")
            return "Success"
    elif key_to_continue == "Add More Info":
        tmp_copy = test_cases_info.get_tc_from_json(f"{path_tmp}/test_cases.json")
        return "Cancel"

    else:
        log_object.print_and_log("ABORTED", "Creating Test Cases in ETM", "You aborted the process.")
        time.sleep(.2)
        return "Cancel"