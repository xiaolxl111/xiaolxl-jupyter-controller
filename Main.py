import os
import importlib
import json

# 数据配置
data = {
    "debug": False,                             # 是否开启全局调试  (一般开发者或询问报错时使用)  [True/False]
    "jsonFetcherTimeout": 5,                    # 网络获取超时设置  (一般开发者或询问报错时使用)  [整数(单位秒)]
    "jsonFetcherNetwork": True,                 # 是否开启网络获取  (一般开发者或询问报错时使用)  [True/False]
    "branch": "main"                            # 当前分支         (一般开发者或询问报错时使用)  [分支名字(main/dev)]
}

# UI 配置字典
project_configs = {
    "autodl_comfyui": {
        "dir": "ComfyUI",
        "module": "xiaolxl_jupyter_controller.ComfyUiMain",
        "default": True,
        "config_file": "/root/autodl-tmp/comfyui_ui.json"  # 配置文件位置
    },
    "autodl_sdwebui": {
        "dir": "stable-diffusion-webui",
        "module": "xiaolxl_jupyter_controller.WebUiMain",
        "default": True,
        "config_file": "/root/autodl-tmp/ui.json"  # 配置文件位置
    },
    "casdao_webui": {
        "dir": "stable-diffusion-webui",
        "module": "xiaolxl_jupyter_controller.CasdaoWebUIMain",
        "default": False,
        "config_file": "/home/tom/fssd/casdao_webui.json"  # 配置文件位置
    },
    "autodl_sdwebui_forge": {
        "dir": "stable-diffusion-webui-forge",
        "module": "xiaolxl_jupyter_controller.WebUiForgeMain",
        "default": True,
        "config_file": "/root/autodl-tmp/ui_forge.json"  # 配置文件位置
    }
}

def read_project_config():
    try:
        with open("../ServerConfig.json", 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        if data['debug']:
            print(f"读取镜像配置文件ServerConfig.json时,未找到文件")
        return None
    except json.JSONDecodeError:
        if data['debug']:
            print(f"读取镜像配置文件ServerConfig.json时,json转换失败")
        return None
    except Exception as e:
        if data['debug']:
            print(f"读取镜像配置文件ServerConfig.json时,发生未知错误: {e}")
        return None

def check_if_directory_exists(directory_name):
    dir_path = f'../{directory_name}'
    exists = os.path.exists(dir_path) and os.path.isdir(dir_path)
    if data['debug']:
        print(f"检查镜像中项目目录 {directory_name}: {'存在' if exists else '不存在'}")
    return exists

def select_ui(cmd_run):
    project_config = read_project_config()
    if project_config:
        config_file_path = project_configs[project_config["project_name"]]["config_file"]
        data['config_file'] = config_file_path  # 设置config_file的路径
        module_path = project_configs[project_config["project_name"]]["module"]
        UiMain = importlib.import_module(module_path)
        UiMain.show(data, cmd_run)
    else:
        for project_name, project_info in project_configs.items():
            if check_if_directory_exists(project_info["dir"]) and project_info["default"]:
                config_file_path = project_info["config_file"]
                data['config_file'] = config_file_path  # 设置config_file的路径
                module_path = project_info["module"]
                UiMain = importlib.import_module(module_path)
                UiMain.show(data, cmd_run)
                return
        # 如果没有找到匹配的项目，使用默认的UI并设置默认的config_file路径
        UiMain = importlib.import_module("xiaolxl_jupyter_controller.AutoDlMain") # 无对应UI的默认UI
        data['config_file'] = "/root/autodl-tmp/default_ui.json"  # 无对应UI的默认配置路径
        UiMain.show(data, cmd_run)
        print("没有找到你需要的UI, 已加载默认的AutoDlMainUI")

def show(cmd_run):
    select_ui(cmd_run)