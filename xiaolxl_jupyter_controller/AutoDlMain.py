import ipywidgets as widgets
import os

from .core.services import initialize_common_services
# from xiaolxl_jupyter_controller.ui_scripts.tools.utils.component_registry import * # Removed
# from xiaolxl_jupyter_controller.ui_scripts.tools.utils.json_config_manager2 import * # Removed
# from xiaolxl_jupyter_controller.ui_scripts.tools.utils.print_tool import * # Removed
# from xiaolxl_jupyter_controller.ui_scripts.tools.utils.json_fetcher import * # Removed
# from xiaolxl_jupyter_controller.ui_scripts.tools.utils.xiaolxl_jupyter_controller_version import * # Removed
from xiaolxl_jupyter_controller.ui_scripts.tools.utils.config_tool import * 

import xiaolxl_jupyter_controller.ui_scripts.scripts.autodl.AboutUi as AboutUi, \
    xiaolxl_jupyter_controller.ui_scripts.scripts.autodl.DownloadUi as DownloadUi, \
    xiaolxl_jupyter_controller.ui_scripts.scripts.autodl.SpeedUi as SpeedUi, \
    xiaolxl_jupyter_controller.ui_scripts.scripts.autodl.UpdataUi as UpdataUi, \
    xiaolxl_jupyter_controller.ui_scripts.scripts.autodl.ToolUi as ToolUi

def show(data: dict, cmd_run: object) -> None:
    ui_specific_default_config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ui_scripts/data/autodl', 'default_config.json')  # 获取默认配置路径
    # uiConfig = JsonConfigManager(data['config_file'], default_config, debug=data['debug'])  # 配置链 # Removed

    # logOut = LogController(enable_output=data['debug'])  # 调试输出类 # Removed
    # jsonFetcher = JsonFetcher(timeout=data['jsonFetcherTimeout'], fetch_from_network=data['jsonFetcherNetwork'], debug=data['debug'])  # JSON获取类 # Removed
    # versionController = VersionController(debug=data['debug'])  # 启动器版本类 # Removed

    # controllers = {'uiConfig': uiConfig, 'logOut': logOut, 'jsonFetcher': jsonFetcher, 'versionController': versionController} # Removed
    controllers = initialize_common_services(data, cmd_run, ui_specific_default_config_path)

    ui_elements = {
        '下载器': DownloadUi.getUi(data, cmd_run, controllers),
        '更新管理': UpdataUi.getUi(data, cmd_run, controllers),
        '工具箱': ToolUi.getUi(data, cmd_run, controllers),
        '关于启动器': AboutUi.getUi(data, cmd_run, controllers)
    }

    tab = widgets.Tab()
    tab.children = list(ui_elements.values())  # 子元素列表
    for i, title in enumerate(ui_elements.keys()):  # 使用枚举函数来获取索引和标题
        tab.set_title(i, title)

    SpeedUi.show(data, cmd_run, controllers)
    display(tab)
