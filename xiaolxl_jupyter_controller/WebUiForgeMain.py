import ipywidgets as widgets
import os

from xiaolxl_jupyter_controller.ui_scripts.tools.utils.component_registry import *
from xiaolxl_jupyter_controller.ui_scripts.tools.utils.json_config_manager2 import * 
from xiaolxl_jupyter_controller.ui_scripts.tools.utils.print_tool import * 
from xiaolxl_jupyter_controller.ui_scripts.tools.utils.json_fetcher import * 
from xiaolxl_jupyter_controller.ui_scripts.tools.utils.xiaolxl_jupyter_controller_version import * 
from xiaolxl_jupyter_controller.ui_scripts.tools.utils.config_tool import * 

import xiaolxl_jupyter_controller.ui_scripts.scripts.autodl_webui_forge.AboutUi as AboutUi, \
    xiaolxl_jupyter_controller.ui_scripts.scripts.autodl_webui_forge.DownloadUi as DownloadUi, \
    xiaolxl_jupyter_controller.ui_scripts.scripts.autodl_webui_forge.SpeedUi as SpeedUi, \
    xiaolxl_jupyter_controller.ui_scripts.scripts.autodl_webui_forge.UpdataUi as UpdataUi, \
    xiaolxl_jupyter_controller.ui_scripts.scripts.autodl_webui_forge.ToolUi as ToolUi, \
    xiaolxl_jupyter_controller.ui_scripts.scripts.autodl_webui_forge.StartUi as StartUi, \
    xiaolxl_jupyter_controller.ui_scripts.scripts.autodl_webui_forge.ProjectUi as ProjectUi

def show(data, cmd_run):
    uiRegistry = ComponentRegistry(debug=data['debug'])  # ui注册链

    default_config = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ui_scripts/data/autodl_webui_forge', 'default_config.json')  # 获取默认配置路径
    uiConfig = JsonConfigManager(data['config_file'], default_config, debug=data['debug'])  # 配置链

    env_path = uiConfig.get_run_config_index_item("env_path")
    if env_path != "":
        os.environ["PATH"] = env_path + os.environ["PATH"]
    
    logOut = LogController(enable_output=data['debug'])  # 调试输出类
    jsonFetcher = JsonFetcher(timeout=data['jsonFetcherTimeout'], fetch_from_network=data['jsonFetcherNetwork'], debug=data['debug'])  # JSON获取类
    versionController = VersionController(debug=data['debug'])  # 启动器版本类

    controllers = {'uiRegistry': uiRegistry, 'uiConfig': uiConfig, 'logOut': logOut, 'jsonFetcher': jsonFetcher, 'versionController': versionController}

    # 使用字典结构将tab_titles和children结合起来
    ui_components = {
        '下载器': DownloadUi.getUi(data, cmd_run, controllers),
        '更新管理': UpdataUi.getUi(data, cmd_run, controllers),
        '工具箱': ToolUi.getUi(data, cmd_run, controllers),
        '关于启动器': AboutUi.getUi(data, cmd_run, controllers),
        '关于镜像项目': ProjectUi.getUi(data, cmd_run, controllers),
        '启动SD-WebUi': StartUi.getUi(data, cmd_run, controllers)
    }
    tab = widgets.Tab()
    tab.children = list(ui_components.values())  # 将字典的值转化为列表作为子组件
    for i, title in enumerate(ui_components.keys()):
        tab.set_title(i, title)  # 将字典的键作为标签标题

    SpeedUi.show(data, cmd_run, controllers)
    display(tab)

