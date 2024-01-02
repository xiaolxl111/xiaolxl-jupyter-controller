from component_registry import *
from json_config_manager import * 
from print_tool import * 
from json_fetcher import * 
from xiaolxl_jupyter_controller_version import * 

import ipywidgets as widgets
import os

import AboutUi, DownloadUi, SpeedUi, UpdataUi, ToolUi, StartUi

def show(data,cmd_run):
    uiRegistry = ComponentRegistry(debug=data['debug']) # ui注册链

    default_config = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'default_config.json')
    uiConfig = JsonConfigManager(data['config_file'], default_config, debug=data['debug']) # 配置链
    
    logOut = logOut = LogController(enable_output=data['debug']) # 调试输出类
    jsonFetcher = JsonFetcher(timeout=data['jsonFetcherTimeout'],fetch_from_network=data['jsonFetcherNetwork'],debug=data['debug']) # JSON获取类
    versionController = VersionController(debug=data['debug']) # 启动器版本类

    controllers = {'uiRegistry': uiRegistry, 'uiConfig': uiConfig, 'logOut': logOut, 'jsonFetcher': jsonFetcher, 'versionController': versionController}

    tab_titles = ['下载器','更新管理','工具箱','关于启动器','启动SD-WebUi']
    children = [DownloadUi.getUi(data,cmd_run,controllers),UpdataUi.getUi(data,cmd_run,controllers),ToolUi.getUi(data,cmd_run,controllers),AboutUi.getUi(data,cmd_run,controllers),StartUi.getUi(data,cmd_run,controllers)]
    
    tab = widgets.Tab()
    tab.children = children
    for i in range(len(tab_titles)):
        tab.set_title(i, tab_titles[i])

    SpeedUi.show(data,cmd_run,controllers)
    display(tab)