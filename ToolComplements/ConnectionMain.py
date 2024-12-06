import os
import time
import threading
from tqdm import tqdm
from configparser import ConfigParser
from ConnectionJazz import JazzConnection
from TC_Common.TestCasesActions import TestCasesActions
from TC_Common.SelectorCmd import cmd_colors
from TC_Common.SelectorCmd import CMDSelector

enable_etm_connection = False
debug_in_console = False

# ************ TestCasesActions INITIALIZATION ************
test_cases_obj = TestCasesActions(debug_in_console)
if test_cases_obj is None:
    print(f"--- {cmd_colors.RED}ERROR:{cmd_colors.END} Test Cases actions could not be initialized.")
    exit()
# • • • • • • • ♦ ♦ ♦ ♦ ♦ ♦ ♦ ♦ ♦ ♦ ♦ • • • • • • •

def getIniFiles():
    ini_files = []
    files = os.listdir(f"{os.path.dirname(__file__)}/INI_Server_files")
    for file in files:
        if file.endswith(".ini"):
            ini_files.append(file)
    return ini_files

def selectIniFile(ini_files):
    ini_file = f"{os.path.dirname(__file__)}/INI_Server_files"
    ini_file_selector = CMDSelector()
    ini_file_selector.title = "Select INI file for Connection to ETM:"
    ini_file_selector.options = ini_files
    in_file = ini_file_selector.select()
    ini_file += "\\" + in_file
    if not os.path.isfile(ini_file):
        print(f"--- {cmd_colors.RED}ERROR:{cmd_colors.END} INI file {cmd_colors.RED}{ini_file}{cmd_colors.END} not found.\n")
        exit()
    else:
        print(f"--- {cmd_colors.GREEN}SUCCESS:{cmd_colors.END} INI file {cmd_colors.GREEN}{ini_file}{cmd_colors.END} found.\n")
    return ini_file

def get_connection(inServerAddress, inBu_suffix):
    print(f"--- {cmd_colors.BLUE}Connecting to ETM {inServerAddress}...{cmd_colors.END}")
    connection = JazzConnection.connect_to_etm(inServerAddress, inBu_suffix)
    if connection:
        print(f"--- {cmd_colors.GREEN}SUCCESS:{cmd_colors.END} Connection to ETM {cmd_colors.GREEN}{inServerAddress}{cmd_colors.END} established.\n")
    else:
        print(f"--- {cmd_colors.RED}ERROR:{cmd_colors.END} Connection to ETM {cmd_colors.RED}{inServerAddress}{cmd_colors.END} failed.\n")
        exit()
    return connection

def get_project_context(config, connection):
    print(f"--- {cmd_colors.BLUE}Creating Context Factory...{cmd_colors.END}")
    project_area = config.get('jazz_configuration', 'gc_project_area_name')
    component = config.get('jazz_configuration', 'gc_component_name')
    configuration = config.get('jazz_configuration', 'gc_config_name')
    stream_name = config.get('jazz_configuration', 'gc_stream_name')
    qm_project_area = config.get('jazz_configuration', 'qm_project_area_name')
    context_factory = JazzConnection.get_context_factory(connection, project_area, component, configuration, qm_project_area, stream_name)
    if context_factory:
        print(f"--- {cmd_colors.GREEN}SUCCESS:{cmd_colors.END} Context Factory {cmd_colors.GREEN}{project_area}{cmd_colors.END} created.\n")
    else:
        print(f"--- {cmd_colors.RED}ERROR:{cmd_colors.END} Context Factory {cmd_colors.RED}{project_area}{cmd_colors.END} not created.\n")
        exit()
    return context_factory

def get_stream_qm_context(context_factory):
    print(f"--- {cmd_colors.BLUE}Getting Stream Context...{cmd_colors.END}")
    qm_project_area = config.get('jazz_configuration', 'qm_project_area_name')
    stream_name = config.get('jazz_configuration', 'gc_stream_name')
    qm_context = [None]  # Usamos una lista para poder modificarla dentro del hilo
    
    # Función para ejecutar en un hilo separado
    def fetch_context():
        qm_context[0] = JazzConnection.get_qm_context(context_factory, qm_project_area, stream_name)
    
    # Crear y arrancar el hilo
    thread = threading.Thread(target=fetch_context)
    thread.start()
    
    # Mostrar barra de progreso mientras el hilo trabaja (90 segundos)
    with tqdm(total=90, desc="Loading Stream Context", bar_format="{l_bar}{bar} [time left: {remaining}]", ncols=100) as pbar:
        for _ in range(90):
            if not thread.is_alive():
                # Si el hilo termina antes de los 90 segundos, terminamos la barra
                pbar.update(90 - pbar.n)
                break
            time.sleep(1)
            pbar.update(1)
    
    # Esperar que el hilo termine (en caso de que todavía esté corriendo)
    thread.join()
    
    # Verifica el resultado y muestra el mensaje correspondiente
    if qm_context[0]:
        print(f"--- {cmd_colors.GREEN}SUCCESS:{cmd_colors.END} Stream Context {cmd_colors.GREEN}{stream_name}{cmd_colors.END} found.\n")
    else:
        print(f"--- {cmd_colors.RED}ERROR:{cmd_colors.END} Stream Context {cmd_colors.RED}{stream_name}{cmd_colors.END} not found.\n")
        exit()
    
    return qm_context[0]

def stream_context_validation(context_factory, qm_context):
    if qm_context:
        print(f"--- {cmd_colors.GREEN}SUCCESS:{cmd_colors.END} Streams found in {cmd_colors.GREEN}{config.get('jazz_configuration', 'gc_project_area_name')}{cmd_colors.END} project:")
        for qm_context_stream in context_factory.qm_contexts():
            print(f"--- {cmd_colors.CYAN}{qm_context_stream.local_configuration_name()}{cmd_colors.END}")
    else:
        print(f"--- {cmd_colors.RED}ERROR:{cmd_colors.END} Streams not found in {cmd_colors.RED}{config.get('jazz_configuration', 'gc_project_area_name')}{cmd_colors.END} project.")
        exit()

def select_action(qm_context, config, context_factory):
    exit = False
    while not exit:
        action_selector = CMDSelector()
        action_selector.title = "Select Action:"
        action_selector.options = test_cases_obj.actions
        action = action_selector.select()
        if action == "Exit":
            exit = True
        else:
            test_cases_obj.action(action, qm_context, config, context_factory)
    

os.system('cls')
print(f"************************* INI FILE SELECTION *************************")
ini_files = getIniFiles()
ini_file = selectIniFile(ini_files)

config = ConfigParser()
config.read(ini_file)

#Connect to ETM
os.system('cls')
print(f"************************* CONNECTION to ETM *************************")
connection = None
if enable_etm_connection:
    connection = get_connection(config.get('jazz_configuration', 'jazz_server'), config.get('jazz_configuration', 'bu_suffix'))

# Get Project Context
context_factory = None
if enable_etm_connection:
    context_factory = get_project_context(config, connection)

# Get Stream QM Context
qm_context = None
if enable_etm_connection:
    qm_context = get_stream_qm_context(context_factory)

key_to_continue = input("Press Enter to continue...")

# Stream Context Validation
os.system('cls')
print(f"************************* CONTEXT VALIDATION *************************")
# stream_context_validation(context_factory, qm_context)

os.makedirs(f"{os.path.dirname(__file__)}/tmp", exist_ok=True)

select_action(qm_context, config, context_factory)

time.sleep(5)
print("---")
