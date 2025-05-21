import ipywidgets as widgets
import os

from xiaolxl_jupyter_controller.ui_scripts.tools.utils.component_registry import *
from xiaolxl_jupyter_controller.ui_scripts.tools.utils.json_config_manager2 import * 
from xiaolxl_jupyter_controller.ui_scripts.tools.utils.print_tool import * 
from xiaolxl_jupyter_controller.ui_scripts.tools.utils.json_fetcher import * 
from xiaolxl_jupyter_controller.ui_scripts.tools.utils.xiaolxl_jupyter_controller_version import * 
from xiaolxl_jupyter_controller.ui_scripts.tools.utils.config_tool import * 

import xiaolxl_jupyter_controller.ui_scripts.scripts.autodl.AboutUi as AboutUi, \
    xiaolxl_jupyter_controller.ui_scripts.scripts.autodl.DownloadUi as DownloadUi, \
    xiaolxl_jupyter_controller.ui_scripts.scripts.autodl.SpeedUi as SpeedUi, \
    xiaolxl_jupyter_controller.ui_scripts.scripts.autodl.UpdataUi as UpdataUi, \
    xiaolxl_jupyter_controller.ui_scripts.scripts.autodl.ToolUi as ToolUi

def show(data, cmd_run):
    default_config = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ui_scripts/data/autodl', 'default_config.json')  # 获取默认配置路径
    uiConfig = JsonConfigManager(data['config_file'], default_config, debug=data['debug'])  # 配置链

    logOut = LogController(enable_output=data['debug'])  # 调试输出类
    jsonFetcher = JsonFetcher(timeout=data['jsonFetcherTimeout'], fetch_from_network=data['jsonFetcherNetwork'], debug=data['debug'])  # JSON获取类
    versionController = VersionController(debug=data['debug'])  # 启动器版本类

    controllers = {'uiConfig': uiConfig, 'logOut': logOut, 'jsonFetcher': jsonFetcher, 'versionController': versionController}

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
