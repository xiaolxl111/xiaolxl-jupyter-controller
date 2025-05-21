import os
from xiaolxl_jupyter_controller.ui_scripts.tools.utils.json_config_manager2 import JsonConfigManager
from xiaolxl_jupyter_controller.ui_scripts.tools.utils.print_tool import LogController
from xiaolxl_jupyter_controller.ui_scripts.tools.utils.json_fetcher import JsonFetcher
from xiaolxl_jupyter_controller.ui_scripts.tools.utils.xiaolxl_jupyter_controller_version import VersionController
from xiaolxl_jupyter_controller.ui_scripts.tools.utils.component_registry import ComponentRegistry

def initialize_common_services(data: dict, cmd_run: object, ui_specific_default_config_path: str) -> dict:
    """
    Initializes common services used by both AutoDlMain and WebUiMain.
    """
    logOut = LogController(enable_output=data['debug'])
    jsonFetcher = JsonFetcher(timeout=data['jsonFetcherTimeout'], fetch_from_network=data['jsonFetcherNetwork'], debug=data['debug'])
    versionController = VersionController(debug=data['debug'])
    uiRegistry = ComponentRegistry(debug=data['debug'])
    uiConfig = JsonConfigManager(user_config_path=data['config_file'], default_config_path=ui_specific_default_config_path, debug=data['debug'])

    return {
        'uiConfig': uiConfig,
        'logOut': logOut,
        'jsonFetcher': jsonFetcher,
        'versionController': versionController,
        'uiRegistry': uiRegistry
    }
