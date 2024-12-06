import getpass
from heppy.connection import Connection
from heppy.base.business_unit_suffixes import BUSuffix
from heppy.context_factories.global_configuration_context_factory import GlobalConfigurationContextFactory
from TC_Common.SelectorCmd import CMDSelector
import time

def get_bu_suffixKey(bu_suffix):
    return [item for item in BUSuffix if item.value == bu_suffix][0]

class JazzConnection:
    def connect_to_etm(inServerAddress, inBu_suffix, inUser, inPassword):
        bu_suffixKey = get_bu_suffixKey(inBu_suffix)
        try:
            connection = Connection(
                server=inServerAddress,
                business_unit_suffix=bu_suffixKey,
                username=inUser,
                password=inPassword
            )
            return connection
        except:
            return None

    def get_context_factory(connection, project_area, component, configuration):
        try:
            return GlobalConfigurationContextFactory(
                connection,
                gc_project_area_name=project_area,
                gc_component_name=component,
                gc_config_name=configuration,
                recurse_into_sub_configurations=True
            )
        except:
            return None
    
    
    def get_qm_context(context_factory, stream_name):
        try:
            candidate_contexts = [
                qm_context
                for qm_context in context_factory.qm_contexts()
                ]
            for context in candidate_contexts:
                if context.local_configuration_name() == stream_name:
                    return context
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