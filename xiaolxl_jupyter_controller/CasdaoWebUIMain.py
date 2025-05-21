import ipywidgets as widgets
import os

from xiaolxl_jupyter_controller.ui_scripts.tools.utils.component_registry import *
from xiaolxl_jupyter_controller.ui_scripts.tools.utils.json_config_manager2 import * 
from xiaolxl_jupyter_controller.ui_scripts.tools.utils.print_tool import * 
from xiaolxl_jupyter_controller.ui_scripts.tools.utils.json_fetcher import * 
from xiaolxl_jupyter_controller.ui_scripts.tools.utils.xiaolxl_jupyter_controller_version import * 
from xiaolxl_jupyter_controller.ui_scripts.tools.utils.config_tool import * 

import xiaolxl_jupyter_controller.ui_scripts.scripts.casdao_webui.AboutUi as AboutUi, \
    xiaolxl_jupyter_controller.ui_scripts.scripts.casdao_webui.DownloadUi as DownloadUi, \
    xiaolxl_jupyter_controller.ui_scripts.scripts.casdao_webui.SpeedUi as SpeedUi, \
    xiaolxl_jupyter_controller.ui_scripts.scripts.casdao_webui.UpdataUi as UpdataUi, \
    xiaolxl_jupyter_controller.ui_scripts.scripts.casdao_webui.ToolUi as ToolUi, \
    xiaolxl_jupyter_controller.ui_scripts.scripts.casdao_webui.StartUi as StartUi, \
    xiaolxl_jupyter_controller.ui_scripts.scripts.casdao_webui.ProjectUi as ProjectUi

def show(data, cmd_run):
    uiRegistry = ComponentRegistry(debug=data['debug'])  # ui注册链

    default_config = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ui_scripts/data/casdao_webui', 'default_config.json')  # 获取默认配置路径
    uiConfig = JsonConfigManager(data['config_file'], default_config, debug=data['debug'])  # 配置链

    env_path = uiConfig.get_run_config_index_item("env_path")
    if env_path != "":
        os.environ["PATH"] = env_path + os.environ["PATH"]

    logOut = LogController(enable_output=data['debug'])  # 调试输出类
    jsonFetcher = JsonFetcher(timeout=data['jsonFetcherTimeout'], fetch_from_network=data['jsonFetcherNetwork'], debug=data['debug'])  # JSON获取类
    versionController = VersionController(debug=data['debug'])  # 启动器版本类

    controllers = {'uiRegistry': uiRegistry, 'uiConfig': uiConfig, 'logOut': logOut, 'jsonFetcher': jsonFetcher, 'versionController': versionController}

    # 使用列表将 tab_titles 和 children 组合在一起
    tabs = [
        ('下载器', DownloadUi.getUi(data, cmd_run, controllers)),
        ('更新管理', UpdataUi.getUi(data, cmd_run, controllers)),
        ('工具箱', ToolUi.getUi(data, cmd_run, controllers)),
        ('关于启动器', AboutUi.getUi(data, cmd_run, controllers)),
        ('关于镜像项目', ProjectUi.getUi(data, cmd_run, controllers)),
        ('启动SD-WebUi', StartUi.getUi(data, cmd_run, controllers))
    ]

    tab_widget = widgets.Tab()
    tab_widget.children = [tab[1] for tab in tabs]  # 子组件列表
    for i, tab in enumerate(tabs):
        tab_widget.set_title(i, tab[0])  # 设置每个标签的标题

    # SpeedUi.show(data, cmd_run, controllers)
    display(tab_widget)
