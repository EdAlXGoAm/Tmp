import getpass
from heppy.connection import Connection
from heppy.base.business_unit_suffixes import BUSuffix
from heppy.context_factories.global_configuration_context_factory import GlobalConfigurationContextFactory
from heppy.context_factories.local_qm_configuration_context_factory import LocalQMConfigurationContextFactory
from TC_Common.SelectorCmd import CMDSelector
import time

def get_bu_suffixKey(bu_suffix):
    return [item for item in BUSuffix if item.value == bu_suffix][0]

def get_user():
    return input("User: ")

def get_password():
    return getpass.getpass("Password: ")

class JazzConnection:
    def connect_to_etm(inServerAddress, inBu_suffix):
        bu_suffixKey = get_bu_suffixKey(inBu_suffix)
        try:
            connection = Connection(
                server=inServerAddress,
                business_unit_suffix=bu_suffixKey,
                username=get_user(),
                password=get_password()
            )
            return connection
        except:
            return None

    def get_context_factory(connection, project_area, component, configuration, qm_project_area, gc_stream_name):
        try:
            print(f"--- qm_project_area: {qm_project_area}")
            if (qm_project_area == ""):
                return GlobalConfigurationContextFactory(
                    connection,
                    gc_project_area_name=project_area,
                    gc_component_name=component,
                    gc_config_name=configuration,
                    recurse_into_sub_configurations=True
                )
            else:
                return LocalQMConfigurationContextFactory(
                    connection,
                    qm_project_area_name=qm_project_area,
                    local_qm_stream_name=gc_stream_name
                )
        except:
            return None
    
    
    def get_qm_context(context_factory, qm_project_area, stream_name):
        try:
            candidate_contexts = [
                qm_context
                for qm_context in context_factory.qm_contexts()
                ]
            for context in candidate_contexts:
                if context.local_configuration_name() == stream_name:
                    return context
            if qm_project_area == "":
                selector = CMDSelector()
                selector.title = "Select the stream context:"
                selector.options = [
                    context.local_configuration_name()
                    for context in candidate_contexts
                ]
                stream_name = selector.select()
                for context in candidate_contexts:
                    if context.local_configuration_name() == stream_name:
                        return context

        except:
            return None